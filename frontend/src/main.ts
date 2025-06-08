import { createApp } from "vue";
import { createRouter, createWebHistory } from "vue-router";
import "./index.css";
import App from "./App.vue";
import { clerkPlugin } from "@clerk/vue";
import Vue3Lottie from "vue3-lottie";
import "mapbox-gl/dist/mapbox-gl.css";
import { MotionPlugin } from "@vueuse/motion";
import Vue3Toastify, { type ToastContainerOptions } from "vue3-toastify";
import "vue3-toastify/dist/index.css";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", component: () => import("./views/Home.vue") },
    { path: "/about", component: () => import("./views/About.vue") },
    {
      path: "/sign-in/:catchAll(.*)*",
      component: () => import("./views/Signin.vue"),
    },
    {
      path: "/sign-up/:catchAll(.*)*",
      component: () => import("./views/Signup.vue"),
    },
    {
      path: "/plan",
      component: () => import("./layouts/ProtectedView.vue"),
      children: [
        {
          path: "",
          component: () => import("./views/Plan.vue"),
        },
      ],
    },
    {
      path: "/travel-plans",
      component: () => import("./layouts/ProtectedView.vue"),
      children: [
        {
          path: "",
          component: () => import("./views/TravelPlans.vue"),
        },
      ],
    },
  ],
});

const PUBLISHABLE_KEY = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY;
if (!PUBLISHABLE_KEY) {
  throw new Error("Add your Clerk Publishable Key to the .env file");
}

const app = createApp(App);
app.use(MotionPlugin);
app.use(router);
app.use(clerkPlugin, { publishableKey: PUBLISHABLE_KEY });
app.use(Vue3Lottie, { name: "LottieAnimation" });
app.use(Vue3Toastify, {
  autoClose: 2000,
  style: {
    opacity: "1",
    userSelect: "initial",
  },
} as ToastContainerOptions);

app.mount("#app");
