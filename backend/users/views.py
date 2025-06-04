import json
import logging
import os
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from django.contrib.auth import get_user_model
from svix.webhooks import Webhook
from svix.exceptions import WebhookVerificationError
from .models import UserProfile  

logger = logging.getLogger(__name__)
load_dotenv()


@csrf_exempt  
def clerk_webhook_handler(request):
    if request.method == 'POST':
        WEBHOOK_SECRET = os.getenv('CLERK_WEBHOOK_SIGNING_SECRET')
        logger.info(f"Webhook secret present: {bool(WEBHOOK_SECRET)}")

        body = request.body
        headers = {
            'svix-id': request.headers.get('Svix-Id'),
            'svix-timestamp': request.headers.get('Svix-Timestamp'),
            'svix-signature': request.headers.get('Svix-Signature')
        }
        logger.info(f"Received headers: {headers}")

        if not all(headers.values()):
            logger.error("Missing required headers")
            return HttpResponse(status=400, content="Error: Missing required headers")

        try:
            # Verify the webhook
            wh = Webhook(WEBHOOK_SECRET)
            evt = wh.verify(body, headers)

            # Get the event type and data from the dictionary
            event_type = evt.get('type')
            user_data = evt.get('data', {})

            clerk_user_id = user_data.get('id')
            email_addresses = user_data.get('email_addresses', [])
            email = email_addresses[0].get('email_address') if email_addresses else None
            first_name = user_data.get('first_name', '')
            last_name = user_data.get('last_name', '')
            picture = user_data.get('image_url')

            User = get_user_model()

            if event_type == 'user.created':
                user, created = User.objects.get_or_create(
                    username=clerk_user_id,
                    defaults={
                        'email': email or '',
                        'first_name': first_name or '',
                        'last_name': last_name or '',
                    }
                )
                if created:
                    logger.info("New user created in database")
                else:
                    logger.info("User already exists in database")
                    user.email = email or user.email
                    user.first_name = first_name or user.first_name
                    user.last_name = last_name or user.last_name
                    user.save()
                
                UserProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'clerk_user_id': clerk_user_id,
                        'picture': picture or ''
                    }
                )
            elif event_type == 'user.updated':
                try:
                    user = User.objects.get(username=clerk_user_id)
                    user.email = email
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save()
                    UserProfile.objects.update_or_create(
                        user=user,
                        defaults={'clerk_user_id': clerk_user_id, 'picture': picture}
                    )
                except User.DoesNotExist:
                    pass
            elif event_type == 'user.deleted':
                try:
                    user = User.objects.get(username=clerk_user_id)
                    user.delete()
                    UserProfile.objects.filter(user=user).delete()
                except User.DoesNotExist:
                    pass

            return HttpResponse(status=200, content="Webhook received and processed")

        except WebhookVerificationError as e:
            logger.error(f"Webhook verification failed: {e}")
            return HttpResponse(status=400, content=f"Error verifying webhook: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            logger.exception("Full traceback:")
            return HttpResponse(status=500, content="Internal server error")
    else:
        return HttpResponse(status=405, content="Method Not Allowed")

