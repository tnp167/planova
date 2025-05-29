<script setup lang="ts">
import { onMounted, ref } from "vue";
import mapboxgl from "mapbox-gl";
import type { StayLocation } from "@/lib/types";

const props = defineProps<{
  location: StayLocation;
}>();

const mapContainer = ref<HTMLDivElement | null>(null);

onMounted(() => {
  console.log(props.location);
  if (!props.location) return;

  mapboxgl.accessToken = import.meta.env.VITE_MAPBOX_ACCESS_TOKEN;

  const map = new mapboxgl.Map({
    container: mapContainer.value!,
    style: "mapbox://styles/mapbox/streets-v12",
    center: [
      props.location.coordinates.longitude,
      props.location.coordinates.latitude,
    ],
    zoom: 14,
  });

  new mapboxgl.Marker()
    .setLngLat([
      props.location.coordinates.longitude,
      props.location.coordinates.latitude,
    ])
    .addTo(map);
});
</script>

<template>
  <div class="rounded border overflow-hidden" style="height: 300px">
    <div ref="mapContainer" class="w-full h-full" />
  </div>
</template>
