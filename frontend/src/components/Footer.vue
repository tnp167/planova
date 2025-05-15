<script setup lang="ts">
import { AwesomeSocialButton } from "awesome-social-button";
import { useColorMode } from "@vueuse/core";
import { computed, ref } from "vue";
const mode = useColorMode();
const isDark = computed(() => mode.value === "dark");
const openInNewTab = (url: string) => {
  window.open(url, "_blank");
};
</script>

<template>
  <footer class="bg-secondary dark:bg-n-8">
    <div class="container mx-auto px-4 py-8 flex items-center justify-between">
      <p class="text-center text-sm text-gray-500 dark:text-n-1">
        &copy; {{ new Date().getFullYear() }} Planova. All rights reserved.
      </p>
      <div class="flex justify-center gap-4">
        <AwesomeSocialButton
          type="facebook"
          :dark="isDark"
          :link="{ src: 'https://facebook.com' }"
          class="cursor-pointer"
          @click="openInNewTab('https://facebook.com')"
          tooltip="Facebook"
        />
        <AwesomeSocialButton
          type="pinterest"
          :dark="isDark"
          :link="{ src: 'https://pinterest.com' }"
          class="cursor-pointer"
          @click="openInNewTab('https://pinterest.com')"
          tooltip="Pinterest"
        />
        <AwesomeSocialButton
          type="instagram"
          :dark="isDark"
          :link="{ src: 'https://instagram.com' }"
          class="cursor-pointer"
          @click="openInNewTab('https://instagram.com')"
          tooltip="Instagram"
        />
        <AwesomeSocialButton
          type="twitter"
          :dark="isDark"
          :link="{ src: 'https://twitter.com' }"
          class="cursor-pointer"
          @click="openInNewTab('https://twitter.com')"
          tooltip="Twitter"
        />
      </div>
    </div>
  </footer>
</template>
