<script setup lang="ts">
import TripJSON from "@/assets/lottie/trip.json";
import { Vue3Lottie } from "vue3-lottie";
</script>

<template>
  <div
    class="mx-5 min-h-[calc(100vh-100px)] px-4 grid md:grid-cols-2 md:gap-28 gap-6 py-16 lg:py-18 xl:flex-row justify-center items-center"
  >
    <div class="flex flex-col gap-8 items-center justify-center">
      <h1 class="text-4xl lg:text-5xl font-bold tracking-wider text-center">
        Effortless Trip Planning, Unforgettable Experiences
      </h1>
      <p class="text-center text-gray-500">
        From discovering the perfect destinations and hidden gems to crafting
        your ideal daily itinerary, we make travel planning simple. Choose your
        place, explore curated local spots, and map out your adventure, your way
      </p>
      <div class="relative group mt-3">
        <button
          class="relative inline-block p-px font-semibold leading-6 text-white cursor-pointer rounded-xl shadow-zinc-900 transition-transform duration-300 ease-in-out hover:scale-105 active:scale-95"
        >
          <span
            class="absolute inset-0 rounded-xl bg-gradient-to-r from-teal-400 via-blue-500 to-purple-500 p-[2px] opacity-0 transition-opacity duration-500 group-hover:opacity-100"
          ></span>

          <span
            class="relative z-10 block px-6 py-3 rounded-xl bg-primary dark:bg-black"
          >
            <span>Get started</span>
          </span>
        </button>
      </div>
    </div>
    <Vue3Lottie
      :animationData="TripJSON"
      :height="500"
      :width="500"
      class="hidden sm:block"
    />
    <Vue3Lottie
      :animationData="TripJSON"
      :height="400"
      :width="400"
      class="block sm:hidden"
    />
  </div>
</template>
