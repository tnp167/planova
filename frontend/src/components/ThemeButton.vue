<script setup lang="ts">
import { Switch } from "@/components/ui/switch";
import { Icon } from "@iconify/vue";
import { useColorMode } from "@vueuse/core";
import { ref, computed } from "vue";

const mode = useColorMode();
const isDark = ref(mode.value === "dark");

const toggleTheme = () => {
  isDark.value = !isDark.value;
  mode.value = isDark.value ? "dark" : "light";
};

const themeIcon = computed(() => {
  if (mode.value === "dark") {
    return {
      current: { name: "radix-icons:moon", color: "text-blue-400" },
      opposite: {
        name: "radix-icons:sun",
        color: "text-yellow-600",
        position: "left-0.5",
      },
    };
  } else {
    return {
      current: { name: "radix-icons:sun", color: "text-yellow-500" },
      opposite: {
        name: "radix-icons:moon",
        color: "text-blue-400",
        position: "right-0.5",
      },
    };
  }
});
</script>

<template>
  <div class="flex items-center gap-3">
    <Switch
      :model-value="isDark"
      @update:model-value="toggleTheme"
      @click.stop
      class="scale-150 cursor-pointer relative"
    >
      <template #thumb>
        <Icon
          :icon="themeIcon.current.name"
          class="transition-all duration-300 ease-in-out size-2.5"
          :class="themeIcon.current.color"
        />
      </template>

      <template #icon>
        <Icon
          :icon="themeIcon.opposite.name"
          class="absolute opacity-60 transition-all duration-300 ease-in-out size-2.5"
          :class="[themeIcon.opposite.color, themeIcon.opposite.position]"
        />
      </template>
    </Switch>
  </div>
</template>
