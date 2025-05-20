<script setup lang="ts">
import ImageCard from "@/components/ImageCard.vue";
import { destinations } from "@/data/destinations";
import { ref, computed, onMounted, onUnmounted } from "vue";
import { Icon } from "@iconify/vue";

import { Swiper, SwiperSlide } from "swiper/vue";
import { Pagination, Navigation, EffectCards } from "swiper/modules";
import "swiper/css";
import "swiper/css/pagination";
import "swiper/css/navigation";
import "swiper/css/effect-cards";

const windowWidth = ref(window.innerWidth);

const handleResize = () => {
  windowWidth.value = window.innerWidth;
};

onMounted(() => {
  window.addEventListener("resize", handleResize);
});

onUnmounted(() => {
  window.removeEventListener("resize", handleResize);
});

const isMobile = computed(() => windowWidth.value < 768);

const itemsPerPage = computed(() => {
  if (windowWidth.value < 768) return 1;
  if (windowWidth.value < 1024) return 4;
  return 6;
});

const paginatedSlides = computed(() => {
  const result = [];
  const count = itemsPerPage.value;
  for (let i = 0; i < destinations.length; i += count) {
    result.push(destinations.slice(i, i + count));
  }
  return result;
});
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <div class="h-[32px] mb-4 leading-[32px] flex justify-center">
      <div
        class="h-[1px] flex-1 border-t-[2px] border-t-primary/60 my-4 mx-[14px]"
      />
      <h4 class="text-2xl font-bold flex items-center gap-2">
        <Icon icon="mdi:star" class="text-amber-500" />
        <span class="text-2xl font-bold">Popular Destinations</span>
      </h4>
      <div
        class="h-[1px] flex-1 border-t-[2px] border-t-primary/60 my-4 mx-[14px]"
      />
    </div>
    <div
      :class="{
        'w-[300px] mx-auto': isMobile,
        'w-full': !isMobile,
      }"
    >
      <Swiper
        class="destination-swiper"
        :modules="[Pagination, Navigation, EffectCards]"
        :effect="isMobile ? 'cards' : 'slide'"
        :pagination="{ clickable: true }"
        :navigation="!isMobile"
        :space-between="24"
        :grab-cursor="true"
      >
        <template v-if="isMobile">
          <SwiperSlide
            v-for="item in destinations"
            :key="item.id"
            class="rounded-xl"
          >
            <ImageCard :img-src="item.imageUrl" class="h-[300px]">
              <h3 class="text-white text-2xl font-bold">{{ item.title }}</h3>
              <p class="text-white/90">{{ item.description }}</p>
            </ImageCard>
          </SwiperSlide>
        </template>

        <template v-else>
          <SwiperSlide v-for="(group, index) in paginatedSlides" :key="index">
            <div
              class="grid gap-6 w-full"
              :class="{
                'grid-cols-2 md:grid-rows-2': windowWidth < 1024,
                'grid-cols-3 md:grid-rows-2': windowWidth >= 1024,
              }"
            >
              <ImageCard
                v-for="item in group"
                :key="item.id"
                :img-src="item.imageUrl"
                class="h-[300px] rounded-xl"
              >
                <h3 class="text-white text-2xl font-bold">
                  {{ item.title }}
                </h3>
                <p class="text-white">{{ item.description }}</p>
              </ImageCard>
            </div>
          </SwiperSlide>
        </template>
      </Swiper>
    </div>
  </div>
</template>

<style>
.destination-swiper {
  padding: 20px 0 50px;
}

.swiper-button-next,
.swiper-button-prev {
  background-color: rgba(255, 255, 255, 0.8);
  padding: 16px;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  color: #1f2937;
}

.swiper-button-next:hover,
.swiper-button-prev:hover {
  background-color: rgba(255, 255, 255, 1);
}

.swiper-button-next:after,
.swiper-button-prev:after {
  font-size: 16px;
}

.swiper-pagination-bullet {
  background-color: hsl(221.2 83.2% 53.3%);
}

.swiper-pagination-bullet-active {
  background-color: hsl(221.2 83.2% 53.3%);
}
</style>
