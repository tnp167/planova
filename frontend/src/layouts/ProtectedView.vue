<script setup lang="ts">
import { useUser } from "@clerk/vue";
import { useRouter } from "vue-router";
import { ref, watchEffect } from "vue";

const { isLoaded, isSignedIn } = useUser();
const router = useRouter();
const show = ref(false);

watchEffect(() => {
  if (isLoaded.value) {
    if (!isSignedIn.value) {
      router.push("/sign-in");
    } else {
      show.value = true;
    }
  }
});
</script>

<template>
  <router-view v-if="show" />
</template>
