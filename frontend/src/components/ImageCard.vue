<script setup lang="ts">
defineProps({
  imgSrc: {
    type: String,
    required: true,
  },
});
</script>

<template>
  <div
    class="relative w-full h-[300px] overflow-hidden rounded-2xl shadow-lg group"
  >
    <img
      :src="imgSrc"
      alt="Image"
      class="w-full h-full object-cover transition-transform duration-200 group-hover:scale-110"
    />
    <div
      class="absolute inset-0 flex items-end bg-gradient-to-t from-black/60 to-transparent"
    >
      <div class="p-4 text-white w-full">
        <slot />
      </div>
    </div>
  </div>
</template>
