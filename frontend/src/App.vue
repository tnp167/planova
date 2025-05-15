<script setup lang="ts">
import Header from "@/components/Header.vue";
import Footer from "@/components/Footer.vue";
import { useUser, useClerk } from "@clerk/vue";
import { useRouter } from "vue-router";
import { watch } from "vue";

const { isSignedIn, isLoaded } = useUser();
const router = useRouter();

watch([isSignedIn, isLoaded], ([newIsSignedIn, newIsLoaded]) => {
  if (newIsLoaded) {
    const currentRoute = router.currentRoute.value.path;
  }
});
</script>

<template>
  <Header v-if="$route.path !== '/sign-in' && $route.path !== '/sign-up'" />
  <router-view></router-view>
  <Footer v-if="$route.path !== '/sign-in' && $route.path !== '/sign-up'" />
</template>
