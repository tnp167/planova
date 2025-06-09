<script setup lang="ts">
import { useUser, useClerk } from "@clerk/vue";
import { ref, computed } from "vue";
import { Icon } from "@iconify/vue";
import { SignOutButton } from "@clerk/vue";
import UserImage from "@/assets/images/default-user.jpg";
import ThemeButton from "@/components/ThemeButton.vue";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";

interface NavigationItem {
  id: number;
  title: string;
  url: string;
}

const { isSignedIn, user } = useUser();

const navigation: NavigationItem[] = [
  { id: 1, title: "Home", url: "/" },
  { id: 2, title: "About", url: "/about" },
  { id: 3, title: "Travel Plans", url: "/travel-plans" },
];

const filteredNavigation = computed(() => {
  return navigation.filter(
    (item) => item.title !== "Travel Plans" || isSignedIn.value
  );
});

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
    class="fixed top-0 left-0 h-auto w-full bg-secondary z-50 border-b dark:border-n-6 lg:!backdrop-blur-sm"
    :class="{
      'bg-white dark:bg-n-8': openNavigation,
      'bg-n-8/90 backdrop-blur-sm dark:bg-n-8/90': !openNavigation,
    }"
  >
    <div
      class="flex justify-between items-center px-5 lg:px-7.5 xl:px-10 max-lg:py-4"
    >
      <router-link
        class="font-extrabold text-3xl bg-gradient-to-r from-primary to-[#8c00ff] bg-clip-text text-transparent duration-300 ease-in-out uppercase"
        to="/"
      >
        Planova
      </router-link>

      <nav
        :class="{ flex: openNavigation, hidden: !openNavigation }"
        class="fixed top-[5rem] left-0 right-0 bottom-0 lg:static lg:flex lg:mx-auto lg:bg-transparent"
      >
        <div
          class="relative z-2 flex flex-col items-center justify-center mx-auto lg:flex-row !bg-transparent"
        >
          <router-link
            v-for="item in filteredNavigation"
            :key="item.id"
            :to="item.url"
            @click="handleClick"
            class="block relative !text-lg uppercase text-black dark:text-n-1 cursor-pointer px-6 md:py-6 lg:-mr-0.25 lg:text-xs lg:font-semibold lg:leading-5 xl:px-12 hover:text-accent duration-300 ease-in-out"
            activeClass="text-primary dark:text-primary text-xl hover:!text-primary"
          >
            {{ item.title }}
          </router-link>
          <Separator class="bg-black dark:bg-white sm:hidden w-full my-5" />
          <router-link
            v-if="!isSignedIn"
            to="/sign-up"
            class="text-lg m-8 sm:mb-0 sm:text-sm uppercase sm:hidden"
            >Sign Up
          </router-link>

          <router-link v-if="!isSignedIn" to="/sign-in">
            <Button
              class="text-lg uppercase px-5.5 py-5 text-md bg-primary rounded-md hover:text-white hover:ring-white hover:!ring-1 sm:hidden"
            >
              Login
            </Button>
          </router-link>

          <Button
            v-if="isSignedIn"
            class="uppercase sm:hidden !bg-danger hover:!border-danger mt-8"
            as-child
          >
            <SignOutButton>Sign Out</SignOutButton>
          </Button>
        </div>
      </nav>

      <div class="hidden sm:flex items-center space-x-4">
        <div class="flex items-center space-x-3" v-if="isSignedIn">
          <img
            :src="user?.imageUrl || UserImage"
            class="w-8 h-8 rounded-full"
          />
          <span class="text-sm">
            Welcome, {{ user?.firstName || "Traveler" }}
          </span>
        </div>

        <Button
          v-if="isSignedIn"
          class="!bg-danger hover:!border-danger"
          as-child
        >
          <SignOutButton>Sign Out</SignOutButton>
        </Button>

        <router-link v-if="!isSignedIn" to="/sign-up" class="text-sm"
          >Sign Up
        </router-link>

        <router-link v-if="!isSignedIn" to="/sign-in">
          <Button
            class="px-5.5 py-5 text-md bg-primary rounded-md hover:text-white hover:ring-white hover:!ring-1"
          >
            Login
          </Button>
        </router-link>
        <ThemeButton class="hidden lg:block lg:ml-5" />
      </div>
      <div class="flex items-center space-x-3">
        <ThemeButton class="lg:hidden" />

        <Button
          variant="ghost"
          class="ml-2 lg:hidden flex items-center justify-center"
          @click="toggleNavigation"
        >
          <Icon
            icon="radix-icons:hamburger-menu"
            class="size-6"
            v-if="!openNavigation"
          />
          <Icon icon="radix-icons:cross-1" class="size-6" v-else />
        </Button>
      </div>
    </div>
  </div>
</template>
