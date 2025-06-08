<script setup lang="ts">
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import {
  FilePen,
  Pencil,
  Trash,
  Calendar,
  MapPin,
  Users,
  User,
  Heart,
  Smile,
  Home,
} from "lucide-vue-next";
import { formatTripDates } from "@/lib/utils";
import defaultLandscape from "@/assets/images/default-landscape.avif";
import type { Trip } from "@/lib/types";
import { deleteTrip } from "@/lib/apis";
import { toast } from "vue3-toastify";
import {
  TooltipProvider,
  Tooltip,
  TooltipTrigger,
  TooltipContent,
} from "@/components/ui/tooltip";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";

const props = defineProps<{ trip: Trip; token: string }>();
const emit = defineEmits(["select", "delete"]);

const iconMap = {
  solo: User,
  couple: Heart,
  family: Home,
  friends: Smile,
};

const handleDelete = async () => {
  const toastId = toast.loading("Deleting trip...");
  try {
    await deleteTrip(props.token, props.trip.slug);
    emit("delete", props.trip.slug);
    toast.update(toastId, {
      render: "Trip deleted successfully",
      type: "success",
      isLoading: false,
      autoClose: 2000,
      theme: "auto",
    });
  } catch (error) {
    console.error("Error deleting trip:", error);
    toast.update(toastId, {
      render: "Error deleting trip",
      type: "error",
      isLoading: false,
      autoClose: 2000,
      theme: "auto",
    });
  }
};
</script>

<template>
  <Card
    @click="$emit('select', trip.slug)"
    class="flex w-full rounded-xl hover:shadow-lg backdrop-blur-sm py-0 overflow-hidden hover:cursor-pointer hover:bg-muted/50 hover:scale-102 transition-transform duration-300 ease-in-out"
  >
    <CardContent class="flex flex-col sm:flex-row gap-4 p-4 w-full">
      <img
        :src="trip.image_url || defaultLandscape"
        :alt="trip.name || 'Default Landscape'"
        class="w-full sm:w-48 object-cover rounded-xl flex-shrink-0"
      />

      <Badge
        v-if="trip.status === 'draft'"
        variant="outline"
        class="absolute top-2 left-2 bg-yellow-500 border-none py-1.5 sm:py-1 dark:text-black shadow-lg"
      >
        <FilePen class="w-4 h-4" />
        Draft
      </Badge>

      <Progress :model-value="33" class="w-full sm:hidden" />

      <div class="flex flex-col justify-between flex-1 min-w-0">
        <div class="min-w-0">
          <span class="text-lg font-semibold block truncate">{{
            trip.name
          }}</span>

          <div class="my-2.5 text-sm text-gray-500 grid grid-cols-2 gap-4">
            <!-- Location & Dates -->
            <div class="flex flex-col gap-2 min-w-0">
              <div class="flex items-center gap-2 min-w-0">
                <MapPin class="w-4 h-4 flex-shrink-0" />
                <div class="flex min-w-0 items-center gap-1">
                  <span class="truncate" :title="trip.location_name">
                    {{
                      trip.location_name
                        ? trip.location_name.split(",")[0] + ", "
                        : "N/A"
                    }}
                  </span>
                  <span
                    v-if="trip.country_code"
                    class="flex-shrink-0 font-semibold uppercase"
                  >
                    {{ trip.country_code.toUpperCase() }}
                  </span>
                </div>
              </div>

              <div class="flex items-center gap-2 min-w-0">
                <Calendar class="w-4 h-4 flex-shrink-0" />
                <span class="truncate min-w-0">
                  {{
                    trip.start_date && trip.end_date
                      ? formatTripDates(trip.start_date, trip.end_date)
                      : "N/A"
                  }}
                </span>
              </div>
            </div>

            <!-- Travelers & Trip Type -->
            <div class="flex flex-col gap-2 min-w-0">
              <div class="flex items-center gap-2 min-w-0">
                <Users class="w-4 h-4 flex-shrink-0" />
                <TooltipProvider>
                  <Tooltip>
                    <TooltipTrigger>
                      <span
                        class="min-w-0 truncate cursor-help border-b pb-0.5 border-dotted border-gray-500"
                      >
                        {{
                          trip.num_adults + trip.num_children + trip.num_infants
                        }}
                        traveler<span
                          v-if="
                            trip.num_adults +
                              trip.num_children +
                              trip.num_infants >
                            1
                          "
                          >s</span
                        >
                      </span>
                    </TooltipTrigger>
                    <TooltipContent>
                      <span class="min-w-0 truncate">
                        {{ trip.num_adults }} adult<span
                          v-if="trip.num_adults > 1"
                          >s</span
                        >
                        <span v-if="trip.num_children">
                          · {{ trip.num_children }} child<span
                            v-if="trip.num_children > 1"
                            >ren</span
                          >
                        </span>
                        <span v-if="trip.num_infants">
                          · {{ trip.num_infants }} infant<span
                            v-if="trip.num_infants > 1"
                            >s</span
                          >
                        </span>
                      </span>
                    </TooltipContent>
                  </Tooltip>
                </TooltipProvider>
              </div>

              <div
                v-if="trip.trip_type"
                class="flex items-center gap-2 min-w-0 truncate"
                :title="trip.trip_type"
              >
                <component
                  :is="iconMap[trip.trip_type] || User"
                  class="w-4 h-4 text-gray-500 flex-shrink-0"
                />
                <span class="truncate capitalize">{{ trip.trip_type }}</span>
              </div>
            </div>
          </div>
        </div>

        <div
          class="flex flex-col gap-3 w-full sm:w-auto sm:flex-row sm:items-center sm:justify-end"
        >
          <Progress :model-value="33" class="hidden sm:block w-full" />
          <Button
            variant="outline"
            size="icon"
            class="rounded-full w-full sm:size-9"
            aria-label="Edit"
            v-if="trip.status === 'completed'"
          >
            <Pencil class="w-4 h-4" />
            <span class="block sm:hidden">Edit</span>
          </Button>
          <AlertDialog>
            <AlertDialogTrigger as-child>
              <Button
                variant="destructive"
                size="icon"
                class="rounded-full w-full sm:size-9"
                aria-label="Delete"
                @click.stop
              >
                <Trash class="w-4 h-4" />
                <span class="block sm:hidden">Delete</span>
              </Button>
            </AlertDialogTrigger>
            <AlertDialogContent>
              <AlertDialogHeader>
                <AlertDialogTitle>
                  Delete Trip:
                  <span
                    class="font-semibold truncate text-red-500"
                    :title="trip.name"
                    >{{ trip.name }}</span
                  >
                </AlertDialogTitle>
                <AlertDialogDescription>
                  Are you sure you want to delete the trip
                  <strong>{{ trip.name }}</strong>
                  ? This action cannot be undone and will permanently remove all
                  related data.
                </AlertDialogDescription>
              </AlertDialogHeader>
              <AlertDialogFooter>
                <AlertDialogCancel>Cancel</AlertDialogCancel>
                <AlertDialogAction
                  @click="handleDelete"
                  class="bg-red-500 hover:bg-red-600"
                >
                  Delete
                </AlertDialogAction>
              </AlertDialogFooter>
            </AlertDialogContent>
          </AlertDialog>
        </div>
      </div>
    </CardContent>
  </Card>
</template>
