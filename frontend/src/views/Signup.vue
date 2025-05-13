<script setup lang="ts">
import { SignUp } from "@clerk/vue";
import WavyBackground from "@/components/WavyBackground.vue";
</script>

<template>
  <WavyBackground class="mx-auto max-w-4xl">
    <div class="h-screen w-full grid place-content-center">
      <SignUp />
    </div>
  </WavyBackground>
</template>
