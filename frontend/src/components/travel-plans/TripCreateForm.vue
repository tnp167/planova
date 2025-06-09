<script setup lang="ts">
import { watch } from "vue";
import { useForm } from "vee-validate";
import { toTypedSchema } from "@vee-validate/zod";
import { tripDetailsSchema } from "@/lib/schemas";
import {
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { toast } from "vue3-toastify";
import { createNewTrip } from "@/lib/apis";
import { useRouter } from "vue-router";
import { useAuth } from "@clerk/vue";

const form = useForm({
  validationSchema: toTypedSchema(tripDetailsSchema),
});
const router = useRouter();
const { getToken } = useAuth();

const onSubmit = form.handleSubmit(async (values) => {
  const token = await getToken.value();
  if (!token) return router.push("/sign-in");

  const toastId = toast.loading("Creating trip...");
  try {
    const newTrip = await createNewTrip(token, values.name, values.description);
    toast.update(toastId, {
      render: "Trip created",
      type: "success",
      isLoading: false,
      autoClose: 2000,
      theme: "auto",
    });
    router.push(`/plan/${newTrip!.slug}`);
  } catch (e) {
    toast.update(toastId, {
      render: "Error creating trip",
      type: "error",
      isLoading: false,
      autoClose: 2000,
      theme: "auto",
    });
  }
});
</script>

<template>
  <form @submit="onSubmit" class="space-y-4">
    <h2 class="text-lg font-semibold">Create New Trip</h2>
    <FormField v-slot="{ componentField }" name="name">
      <FormItem>
        <FormLabel>Trip Name</FormLabel>
        <FormControl>
          <Input placeholder="e.g. Europe 2025" v-bind="componentField" />
        </FormControl>
        <FormMessage class="text-red-500/80" />
      </FormItem>
    </FormField>

    <FormField v-slot="{ componentField }" name="description">
      <FormItem>
        <FormLabel>Description</FormLabel>
        <FormControl>
          <Textarea
            placeholder="e.g. Backpacking through Europe"
            class="resize-none max-h-40"
            v-bind="componentField"
          />
        </FormControl>
        <FormMessage class="text-red-500/80" />
      </FormItem>
    </FormField>

    <div class="flex justify-end">
      <Button type="submit">Continue</Button>
    </div>
  </form>
</template>
