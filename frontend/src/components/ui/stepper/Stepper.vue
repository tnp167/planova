<script setup lang="ts">
import { ref, watch } from "vue";

const props = defineProps<{
  modelValue: number;
  min?: number;
  max?: number;
}>();

const emit = defineEmits(["update:modelValue"]);

const count = ref(props.modelValue);
const min = props.min ?? 0;
const max = props.max ?? 10;

watch(
  () => props.modelValue,
  (val) => {
    count.value = val;
  }
);

const increment = () => {
  if (count.value < max) {
    count.value++;
    emit("update:modelValue", count.value);
  }
};

const decrement = () => {
  if (count.value > min) {
    count.value--;
    emit("update:modelValue", count.value);
  }
};
</script>

<template>
  <div class="flex items-center gap-2">
    <button
      class="px-3 py-1 rounded border text-sm disabled:opacity-30"
      @click="decrement"
      :disabled="count <= min"
    >
      −
    </button>

    <span class="min-w-[2rem] text-center font-medium">{{ count }}</span>

    <button
      class="px-3 py-1 rounded border text-sm disabled:opacity-30"
      @click="increment"
      :disabled="count >= max"
    >
      +
    </button>
  </div>
</template>
