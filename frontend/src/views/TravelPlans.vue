<script setup lang="ts">
import { ref, onMounted, watch } from "vue";
import { useRouter } from "vue-router";
import Globe from "@/components/travel-plans/Globe.vue";
import {
  Card,
  CardContent,
  CardDescription,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import axios from "axios";
import { useAuth } from "@clerk/vue";
import { Calendar, Users, Pencil, Trash, Plus, MapPin } from "lucide-vue-next";
import { Progress } from "@/components/ui/progress";
import { Vue3Lottie } from "vue3-lottie";
import AttractionsJSON from "@/assets/lottie/attractions.json";
import { RainbowButton } from "@/components/ui/rainbow-button";
import { getTrips } from "@/lib/apis";
import type { Trip } from "@/lib/types";
import { formatTripDates } from "@/lib/utils";
import defaultLandscape from "@/assets/images/default-landscape.avif";

const labels = ref<
  {
    lat: number;
    lng: number;
    text: string;
    color: string;
  }[]
>([]);

const trips = ref<Trip[]>([]);
const isLoading = ref(true);
const router = useRouter();

const { getToken } = useAuth();

const fetchImages = async () => {
  const token = await getToken.value();
  for (const trip of trips.value) {
    try {
      const res = await axios.get(
        `${
          import.meta.env.VITE_API_URL
        }/api/location/city-image/?q=${encodeURIComponent(trip.location_name)}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      trip.image_url = res.data.imageUrl || "/default-image.jpg";
    } catch (e) {
      console.error("Image fetch failed", e);
      trip.image_url = defaultLandscape;
    }
  }
};

const loadTrips = async () => {
  try {
    isLoading.value = true;
    trips.value = await getTrips();
    labels.value = trips.value.map((trip) => ({
      lat: trip.latitude,
      lng: trip.longitude,
      text: trip.location_name.split(",")[0],
      color: getRandomColor(),
    }));
    await fetchImages();
  } catch (error) {
    console.error("Error loading trips:", error);
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  loadTrips();
});

const getRandomColor = () => {
  const colors = [
    "deepskyblue",
    "gold",
    "orange",
    "limegreen",
    "tomato",
    "hotpink",
  ];
  return colors[Math.floor(Math.random() * colors.length)];
};
</script>

<template>
  <div
    class="relative w-full h-screen bg-background text-foreground overflow-hidden flex flex-col lg:flex-row"
  >
    <!--  Globe -->
    <div class="hidden lg:block absolute w-full z-10">
      <Globe :labels="labels" />
    </div>

    <!--  Sidebar Plan List -->
    <div
      class="relative z-20 w-full lg:max-w-[650px] h-full bg-white/80 dark:bg-black/30 backdrop-blur-sm px-4 sm:px-6 py-8 overflow-y-auto pt-24"
    >
      <div class="flex justify-between items-center mb-8">
        <h1
          class="text-2xl font-bold"
          :class="{ 'mx-auto': trips.length === 0 }"
        >
          My Travel Plans
        </h1>
        <Button
          class="text-md"
          v-if="trips.length > 0"
          @click="router.push('/plan')"
        >
          <Plus class="w-4 h-4" /> Create New Plan
        </Button>
      </div>

      <div v-if="isLoading" class="flex justify-center items-center h-64">
        <div
          class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"
        ></div>
      </div>

      <div
        v-else-if="trips.length === 0"
        class="flex flex-col items-center justify-center"
      >
        <Vue3Lottie
          :animationData="AttractionsJSON"
          :height="320"
          :width="320"
          :speed="0.5"
          class="block sm:hidden mb-10"
        />
        <Vue3Lottie
          :animationData="AttractionsJSON"
          :height="400"
          :width="400"
          :speed="0.5"
          class="hidden sm:block mb-10"
        />
        <div class="flex flex-col items-center justify-center gap-6 mt-10">
          <p class="text-center text-xl">
            You don't have any travel plans yet. Let's create one!
          </p>
          <RainbowButton
            class="text-md cursor-pointer"
            @click="router.push('/plan')"
          >
            <Plus class="w-4 h-4 mr-2" /> Create your first travel plan
          </RainbowButton>
        </div>
      </div>

      <div v-else class="space-y-4">
        <Card
          v-for="trip in trips"
          :key="trip.id"
          class="flex w-full rounded-xl transition hover:shadow-lg backdrop-blur-sm py-0 overflow-hidden"
        >
          <CardContent class="flex flex-col sm:flex-row gap-4 p-4 w-full">
            <img
              :src="trip.image_url"
              :alt="trip.name"
              class="w-full sm:w-48 object-cover rounded-xl flex-shrink-0"
            />

            <Progress :model-value="33" class="w-full sm:hidden" />

            <div class="flex flex-col justify-between flex-1 min-w-0">
              <div class="min-w-0">
                <span class="text-lg font-semibold block truncate">{{
                  trip.name
                }}</span>

                <div class="mt-1 text-sm text-gray-500 flex flex-col gap-1.5">
                  <div class="flex items-center gap-2">
                    <MapPin class="w-4 h-4 flex-shrink-0" />
                    <span class="truncate">{{
                      trip.location_name.split(",")[0] +
                      (trip.country_code
                        ? ", " + trip.country_code.toUpperCase()
                        : "")
                    }}</span>
                  </div>
                  <div class="flex items-center gap-2">
                    <Calendar class="w-4 h-4 flex-shrink-0" />
                    <span class="truncate">{{
                      formatTripDates(trip.start_date, trip.end_date)
                    }}</span>
                  </div>
                  <div class="flex items-center gap-2">
                    <Users class="w-4 h-4 flex-shrink-0" />
                    <span class="truncate">
                      {{ trip.num_adults }} adult<span
                        v-if="trip.num_adults > 1"
                        >s</span
                      >
                      <span v-if="trip.num_children"
                        >, {{ trip.num_children }} child<span
                          v-if="trip.num_children > 1"
                          >ren</span
                        ></span
                      >
                      <span v-if="trip.num_infants"
                        >, {{ trip.num_infants }} infant<span
                          v-if="trip.num_infants > 1"
                          >s</span
                        ></span
                      >
                    </span>
                  </div>
                </div>
              </div>

              <!-- Progress + Buttons -->
              <div
                class="flex flex-col gap-3 mt-3 w-full sm:w-auto sm:flex-row sm:items-center sm:justify-end"
              >
                <Progress :model-value="33" class="hidden sm:block w-full" />
                <Button
                  variant="outline"
                  size="icon"
                  class="rounded-full w-full sm:size-9"
                  aria-label="Edit"
                >
                  <Pencil class="w-4 h-4" />
                  <span class="block sm:hidden">Edit</span>
                </Button>
                <Button
                  variant="destructive"
                  size="icon"
                  class="rounded-full w-full sm:size-9"
                  aria-label="Delete"
                >
                  <Trash class="w-4 h-4" />
                  <span class="block sm:hidden">Delete</span>
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  </div>
</template>
