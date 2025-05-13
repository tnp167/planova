<script setup lang="ts">
import { useUser, useClerk } from "@clerk/vue";
import { ref } from "vue";
import { useRouter } from "vue-router";
import { Icon } from "@iconify/vue";
import { SignOutButton } from "@clerk/vue";
import UserImage from "@/assets/images/default-user.jpg";

const { isSignedIn, user } = useUser();
const router = useRouter();

const navigation = [
  { id: 1, title: "Home", url: "/" },
  { id: 2, title: "About", url: "/about" },
];

const openNavigation = ref(false);

const handleClick = () => {
  openNavigation.value = false;
};

const toggleNavigation = () => {
  openNavigation.value = !openNavigation.value;
};
</script>

<template>
  <div
    class="fixed top-0 left-0 w-full z-50 border-b border-n-6 lg:bg-n-8/90 lg:!backdrop-blur-sm"
    :class="{
      'bg-n-8': openNavigation,
      'bg-n-8/90 backdrop-blur-sm': !openNavigation,
    }"
  >
    <div
      class="flex justify-between items-center px-5 lg:px-7.5 xl:px-10 max-lg:py-4"
    >
      <router-link
        class="font-extrabold text-4xl bg-gradient-to-r from-primary to-[#8c00ff] bg-clip-text text-transparent duration-300 ease-in-out"
        to="/"
      >
        Planova
      </router-link>

      <nav
        :class="{ flex: openNavigation, hidden: !openNavigation }"
        class="fixed top-[5rem] left-0 right-0 bottom-0 bg-n-8 lg:static lg:flex lg:mx-auto lg:bg-transparent"
      >
        <div
          class="relative z-2 flex flex-col items-center justify-center m-auto lg:flex-row"
        >
          <router-link
            v-for="item in navigation"
            :key="item.id"
            :to="item.url"
            @click="handleClick"
            class="block relative !text-lg uppercase text-n-1 transition-colors cursor-pointer px-6 py-6 md:py-8 lg:-mr-0.25 lg:text-xs lg:font-semibold lg:leading-5 xl:px-12 hover:text-accent duration-300 ease-in-out"
            activeClass="text-primary text-xl hover:!text-primary"
          >
            {{ item.title }}
          </router-link>
        </div>
      </nav>

      <div class="hidden sm:flex items-center space-x-4">
        <div class="flex items-center space-x-3" v-if="isSignedIn">
          <img
            :src="user?.imageUrl || UserImage"
            class="w-8 h-8 rounded-full"
          />
          <span class="text-sm text-gray-300">
            Welcome, {{ user?.firstName || "Traveler" }}
          </span>
        </div>
        <span v-if="isSignedIn" class="text-sm text-gray-300"> </span>

        <SignOutButton
          v-if="isSignedIn"
          class="!bg-danger !text-white hover:!border-danger"
        >
          Sign Out
        </SignOutButton>

        <router-link v-if="!isSignedIn" to="/sign-up">
          <button>Sign Up</button>
        </router-link>

        <router-link v-if="!isSignedIn" to="/sign-in">
          <button class="text-white !bg-primary rounded-md hover:!border-white">
            Login
          </button>
        </router-link>
      </div>

      <button class="ml-4 lg:hidden" @click="toggleNavigation">
        <Icon icon="heroicons:bars-2-solid bg-white" class="w-6 h-6" />
      </button>
    </div>
  </div>
</template>
