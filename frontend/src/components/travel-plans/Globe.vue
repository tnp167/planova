<script setup lang="ts">
import { onMounted, ref, watch } from "vue";
import Globe from "globe.gl";
import { useDark } from "@vueuse/core";

const isDark = useDark();
const globeContainer = ref<HTMLDivElement | null>(null);

const labels = [
  {
    lat: 51.5074,
    lng: -0.1278,
    text: "London",
    color: "deepskyblue",
    size: 1.2,
    altitude: 0.02,
  },
  {
    lat: 55.9533,
    lng: -3.1883,
    text: "Edinburgh",
    color: "gold",
    size: 1,
    altitude: 0.02,
  },
  {
    lat: 40.7128,
    lng: -74.006,
    text: "New York",
    color: "red",
    size: 1,
    altitude: 0.02,
  },
];

const world = ref<any>(null);

watch(isDark, (dark) => {
  if (world.value) {
    world.value
      .globeImageUrl(
        dark
          ? "//unpkg.com/three-globe/example/img/earth-night.jpg"
          : "//unpkg.com/three-globe/example/img/earth-blue-marble.jpg"
      )
      .backgroundColor(dark ? "#000000" : "#ffffff");
  }
});

onMounted(() => {
  world.value = new Globe(globeContainer.value!)
    .globeImageUrl(
      isDark.value
        ? "//unpkg.com/three-globe/example/img/earth-night.jpg"
        : "//unpkg.com/three-globe/example/img/earth-blue-marble.jpg"
    )
    .backgroundColor(isDark.value ? "#000000" : "#ffffff")
    .labelsData(labels)
    .labelText("text")
    .labelLat("lat")
    .labelLng("lng")
    .labelColor("color")
    .labelSize("size")
    .labelAltitude("altitude")
    .labelDotRadius(0.3)
    .labelDotOrientation(() => "top")
    .globeOffset([325, 30]);

  setTimeout(() => {
    world.value?.pointOfView({ lat: 54.0, lng: 10.0, altitude: 2 }, 3000);
  }, 500);
});
</script>

<template>
  <div ref="globeContainer" class="w-full h-full" />
</template>
