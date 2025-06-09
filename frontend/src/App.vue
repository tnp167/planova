<script setup lang="ts">
import Header from "@/components/Header.vue";
import Footer from "@/components/Footer.vue";
import { useRoute } from "vue-router";

const route = useRoute();
</script>

<template>
  <Header v-if="!['/sign-in', '/sign-up'].includes(route.path)" />
  <router-view></router-view>
  <Footer v-if="!['/sign-in', '/sign-up'].includes(route.path)" />
</template>
