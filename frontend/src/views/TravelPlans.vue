<script setup lang="ts">
import { ref, onMounted } from "vue";
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
import { Calendar, Users, Pencil, Trash, Plus } from "lucide-vue-next";
import { Progress } from "@/components/ui/progress";
import { Vue3Lottie } from "vue3-lottie";
import AttractionsJSON from "@/assets/lottie/attractions.json";
import { RainbowButton } from "@/components/ui/rainbow-button";
const plans = ref([
  {
    id: 1,
    name: "UK Summer Trip",
    location: "London, UK",
    date: "16 Aug 2025 - 24 Sep 2025",
    image: "https://source.unsplash.com/featured/?london",
    duration: 7,
    travelers: {
      adults: 1,
      children: 1,
      infants: 2,
    },
  },
  {
    id: 2,
    name: "Japan Adventure",
    location: "Tokyo, Japan",
    date: "Sept 2025",
    image: "https://source.unsplash.com/featured/?tokyo",
    duration: 7,
    travelers: {
      adults: 2,
      children: 3,
      infants: 0,
    },
  },
  {
    id: 3,
    name: "US West Coast",
    location: "San Francisco, USA",
    date: "Oct 2025",
    image: "https://source.unsplash.com/featured/?san-francisco",
    duration: 7,
    travelers: {
      adults: 2,
      children: 0,
      infants: 1,
    },
  },
  {
    id: 4,
    name: "Paris, France",
    location: "Paris, France",
    date: "Nov 2025",
    image: "https://source.unsplash.com/featured/?paris",
    duration: 7,
    travelers: {
      adults: 2,
      children: 0,
      infants: 3,
    },
  },
]);

const { getToken } = useAuth();
const fetchImages = async () => {
  const token = await getToken.value();
  for (const plan of plans.value) {
    try {
      const res = await axios.get(
        `${
          import.meta.env.VITE_API_URL
        }/api/location/city-image/?q=${encodeURIComponent(plan.location)}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      plan.image = res.data.imageUrl || "/default-image.jpg";
    } catch (e) {
      console.error("Image fetch failed", e);
      plan.image = "/default-image.jpg";
    }
  }
};

onMounted(fetchImages);
</script>

<template>
  <div
    class="relative w-full h-screen bg-background text-foreground overflow-hidden flex flex-col lg:flex-row"
  >
    <!--  Globe -->
    <div class="hidden lg:block absolute w-full z-10">
      <Globe />
    </div>

    <!--  Sidebar Plan List -->
    <div
      class="relative z-20 w-full lg:max-w-[650px] h-full bg-white/80 dark:bg-black/30 backdrop-blur-sm px-4 sm:px-6 py-8 overflow-y-auto pt-24"
    >
      <div class="flex justify-between items-center mb-8">
        <h1
          class="text-2xl font-bold"
          :class="{ 'mx-auto': plans.length === 0 }"
        >
          My Travel Plans
        </h1>
        <Button class="text-md" v-if="plans.length > 0">
          <Plus class="w-4 h-4" /> Create New Plan
        </Button>
      </div>

      <div class="space-y-4">
        <div
          class="flex flex-col items-center justify-center"
          v-if="plans.length === 0"
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
            <RainbowButton class="text-md cursor-pointer">
              <Plus class="w-4 h-4 mr-2" /> Create your first travel plan
            </RainbowButton>
          </div>
        </div>
        <Card
          v-for="(plan, index) in plans"
          v-if="plans.length > 0"
          :key="plan.id"
          class="flex w-full rounded-xl transition hover:shadow-lg backdrop-blur-sm py-0 overflow-hidden"
        >
          <CardContent class="flex flex-col sm:flex-row gap-4 p-4 w-full">
            <img
              :src="plan.image"
              alt="Trip image"
              class="w-full sm:w-48 object-cover rounded-xl flex-shrink-0"
            />

            <Progress :model-value="33" class="w-full sm:hidden" />

            <div class="flex flex-col justify-between flex-1 min-w-0">
              <div class="min-w-0">
                <span class="text-lg font-semibold block truncate">{{
                  plan.name
                }}</span>

                <div class="mt-1 text-sm text-gray-500 flex flex-col gap-1.5">
                  <div class="flex items-center gap-2">
                    <Calendar class="w-4 h-4 flex-shrink-0" />
                    <span class="truncate">{{ plan.date }}</span>
                  </div>
                  <div class="flex items-center gap-2">
                    <Users class="w-4 h-4 flex-shrink-0" />
                    <span class="truncate">
                      {{ plan.travelers.adults }} adult<span
                        v-if="plan.travelers.adults > 1"
                        >s</span
                      >
                      <span v-if="plan.travelers.children"
                        >, {{ plan.travelers.children }} child<span
                          v-if="plan.travelers.children > 1"
                          >ren</span
                        ></span
                      >
                      <span v-if="plan.travelers.infants"
                        >, {{ plan.travelers.infants }} infant<span
                          v-if="plan.travelers.infants > 1"
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
                <Progress
                  :model-value="33"
                  class="w-full h-2 rounded-full hidden sm:block"
                />
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
