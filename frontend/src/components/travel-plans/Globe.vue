<script setup lang="ts">
import { onMounted, ref, watch } from "vue";
import Globe from "globe.gl";
import { useDark } from "@vueuse/core";

const isDark = useDark();
const globeContainer = ref<HTMLDivElement | null>(null);

const props = defineProps<{
  labels: {
    lat: number;
    lng: number;
    text: string;
    color: string;
  }[];
}>();

const world = ref<any>(null);

const initGlobe = () => {
  world.value = new Globe(globeContainer.value!)
    .globeImageUrl(
      isDark.value
        ? "//unpkg.com/three-globe/example/img/earth-night.jpg"
        : "//unpkg.com/three-globe/example/img/earth-blue-marble.jpg"
    )
    .backgroundColor(isDark.value ? "#000000" : "#ffffff")
    .labelText("text")
    .labelLat("lat")
    .labelLng("lng")
    .labelColor("color")
    .labelSize(1.2)
    .labelAltitude(0.02)
    .labelDotRadius(0.3)
    .labelDotOrientation(() => "top")
    .globeOffset([325, 30]);
};

onMounted(() => {
  initGlobe();

  // Set initial labels if available
  if (props.labels.length) {
    world.value?.labelsData(props.labels);
    world.value?.pointOfView({ lat: 54.0, lng: 10.0, altitude: 2 }, 3000);
  }
});

// Dark mode toggle
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

// Watch for label changes
watch(
  () => props.labels,
  (newLabels) => {
    if (world.value && newLabels.length > 0) {
      world.value.labelsData(newLabels);
    }
  },
  { immediate: true }
);
</script>

<template>
  <div ref="globeContainer" class="w-full h-full" />
</template>
