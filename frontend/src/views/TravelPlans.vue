<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import Globe from "@/components/travel-plans/Globe.vue";
import { Button } from "@/components/ui/button";
import { Plus } from "lucide-vue-next";
import { Vue3Lottie } from "vue3-lottie";
import AttractionsJSON from "@/assets/lottie/attractions.json";
import { RainbowButton } from "@/components/ui/rainbow-button";
import type { Trip } from "@/lib/types";
import { getTrips } from "@/lib/apis";
import { useAuth } from "@clerk/vue";
import TripCard from "@/components/travel-plans/TripCard.vue";
import { Dialog, DialogContent, DialogTrigger } from "@/components/ui/dialog";
import TripCreateForm from "@/components/travel-plans/TripCreateForm.vue";

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
const token = ref<string | null>(null);

const loadTrips = async (token: string) => {
  try {
    const set = new Set();
    isLoading.value = true;
    trips.value = await getTrips(token);
    labels.value = trips.value
      .filter((trip) => trip.latitude && trip.longitude && trip.location_name)
      .map((trip) => ({
        lat: trip.latitude || 0,
        lng: trip.longitude || 0,
        text: trip.location_name?.split(",")[0] || "",
        color: getRandomColor(trip.location_name?.split(",")[0] || ""),
      }))
      .filter((label) => {
        const key = `${label.text}-${label.lat}-${label.lng}`;
        if (set.has(key)) return false;
        set.add(key);
        return true;
      });
  } catch (error) {
    console.error("Error loading trips:", error);
  } finally {
    isLoading.value = false;
  }
};

onMounted(async () => {
  token.value = await getToken.value();
  if (!token.value) {
    router.push("/sign-in");
  }
  loadTrips(token.value!);
});

const getRandomColor = (text: string) => {
  const colors = [
    "deepskyblue",
    "gold",
    "orange",
    "lavender",
    "limegreen",
    "hotpink",
    "teal",
    "purple",
    "tomato",
    "coral",
  ];
  let hash = 0;
  for (let i = 0; i < text.length; i++) {
    hash = text.charCodeAt(i) + ((hash << 5) - hash);
  }
  return colors[Math.abs(hash) % colors.length];
};

const handleDelete = async (slug: string) => {
  const tripToRemove = trips.value.find((trip) => trip.slug === slug);

  if (!tripToRemove) return;

  trips.value = trips.value.filter((trip) => trip.slug !== slug);

  labels.value = labels.value.filter(
    (label) =>
      label.text !== tripToRemove.location_name?.split(",")[0] ||
      label.lat !== tripToRemove.latitude ||
      label.lng !== tripToRemove.longitude
  );
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
      class="relative z-20 w-full lg:max-w-[680px] h-full bg-white/80 dark:bg-black/30 backdrop-blur-sm px-4 sm:px-6 py-8 pt-24 flex flex-col"
    >
      <div class="flex justify-between items-center mb-8 shrink-0">
        <h1
          class="text-2xl font-bold"
          :class="{ 'mx-auto': trips.length === 0 }"
        >
          My Travel Plans
        </h1>

        <Dialog>
          <DialogTrigger>
            <Button class="text-md" v-if="trips.length > 0">
              <Plus class="w-4 h-4" /> Create New Plan
            </Button>
          </DialogTrigger>

          <DialogContent class="sm:max-w-md">
            <TripCreateForm />
          </DialogContent>
        </Dialog>
      </div>

      <div class="flex-1 overflow-y-auto space-y-4">
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
            <Dialog>
              <DialogTrigger>
                <RainbowButton class="text-md cursor-pointer">
                  <Plus class="w-4 h-4 mr-2" /> Create your first travel plan
                </RainbowButton>
              </DialogTrigger>
              <DialogContent class="max-w-lg w-full">
                <TripCreateForm @created="loadTrips(token!)" />
              </DialogContent>
            </Dialog>
          </div>
        </div>

        <div v-else class="space-y-4">
          <TripCard
            v-for="trip in trips"
            :key="trip.slug"
            :trip="trip"
            :token="token!"
            @select="(slug) => router.push(`/plan/${slug}`)"
            @delete="handleDelete"
          />
        </div>
      </div>
    </div>
  </div>
</template>
