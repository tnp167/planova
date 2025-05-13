import { createApp } from "vue";
import { createRouter, createWebHistory } from "vue-router";
import "./index.css";
import App from "./App.vue";
import { clerkPlugin } from "@clerk/vue";

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
  ],
});

const PUBLISHABLE_KEY = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY;
if (!PUBLISHABLE_KEY) {
  throw new Error("Add your Clerk Publishable Key to the .env file");
}

const app = createApp(App);
app.use(router);
app.use(clerkPlugin, { publishableKey: PUBLISHABLE_KEY });
app.mount("#app");
