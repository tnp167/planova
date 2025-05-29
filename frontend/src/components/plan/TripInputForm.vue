<script setup lang="ts">
import TripDateRangePicker from "@/components/ui/date-range-picker/DateRangePicker.vue";
import type { DateRange } from "reka-ui";
import { ref, computed, watch, onMounted, onUnmounted } from "vue";
import { Input } from "@/components/ui/input";
import { Search, Users } from "lucide-vue-next";
import {
  Popover,
  PopoverTrigger,
  PopoverContent,
} from "@/components/ui/popover";
import { Label } from "@/components/ui/label";
import Stepper from "@/components/ui/stepper/Stepper.vue";
import axios from "axios";
import type { MapboxFeature, MapboxResponse } from "@/lib/types";
import { useAuth } from "@clerk/vue";
import { CalendarDate, type DateValue } from "@internationalized/date";
import { Dialog, DialogContent, DialogTrigger } from "@/components/ui/dialog";
import HotelListModal from "@/components/plan/HotelListModal.vue";

const { getToken } = useAuth();
const dateRange = ref<DateRange>({
  start: new CalendarDate(
    new Date().getFullYear(),
    new Date().getMonth() + 1,
    new Date().getDate()
  ) as DateValue | undefined,
  end: new CalendarDate(
    new Date().getFullYear(),
    new Date().getMonth() + 1,
    new Date().getDate()
  ).add({ days: 20 }) as DateValue | undefined,
});

const adults = ref(2);
const children = ref(0);
const infants = ref(0);
const summaryText = computed(() => {
  return `${adults.value} Adults, ${children.value} Children, ${infants.value} Infants`;
});

const dropdownRef = ref<HTMLElement | null>(null);
const query = ref<string>("");
const suggestions = ref<MapboxFeature[]>([]);
const selected = ref<MapboxFeature | null>(null);
const country = ref<string | undefined>(undefined);
let debounceTimeout: number | undefined;

watch(query, async (newVal) => {
  clearTimeout(debounceTimeout);

  debounceTimeout = window.setTimeout(async () => {
    const token = await getToken.value();

    if (!newVal || newVal.length < 2) {
      suggestions.value = [];
      return;
    }

    try {
      const res = await axios.get<MapboxResponse>(
        `${import.meta.env.VITE_API_URL}/api/location/autocomplete/`,
        {
          params: { q: newVal },
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      suggestions.value = res.data.features;
    } catch (err) {
      console.error("Autocomplete error:", err);
      suggestions.value = [];
    }
  }, 300);
});

const handleClickOutside = (event: MouseEvent) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target as Node)) {
    suggestions.value = [];
  }
};

onMounted(() => {
  document.addEventListener("click", handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener("click", handleClickOutside);
});

function selectLocation(place: any) {
  selected.value = place;
  query.value = place.place_name;
  handleClickOutside(new MouseEvent("click"));
  country.value = place.context?.[2]?.short_code || place.properties.short_code;
}
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <div class="space-y-4">
      <div ref="dropdownRef" class="relative w-full max-w-sm items-center">
        <Input
          id="search"
          type="text"
          placeholder="Location"
          class="pl-10"
          v-model="query"
        />
        <ul
          v-if="suggestions.length"
          class="absolute z-10 w-full border mt-1 rounded shadow-lg max-h-64 overflow-auto"
        >
          <li
            v-for="(place, index) in suggestions"
            :key="place.id"
            class="px-4 py-2 cursor-pointer bg-background text-foreground hover:bg-accent hover:text-accent-foreground border-b border-border transition-colors duration-200 ease-in-out"
            :class="{
              'rounded-t-md border-0': index === 0,
              'rounded-b-md border-0': index === suggestions.length - 1,
              'bg-muted': selected?.id === place.id,
            }"
            @click="selectLocation(place)"
          >
            {{ place.place_name }}
          </li>
        </ul>
        <span
          class="absolute start-0 inset-y-0 flex items-center justify-center px-3"
        >
          <Search class="size-3.5 dark:text-white text-black" />
        </span>
      </div>
      <TripDateRangePicker v-model="dateRange" />
      <Popover>
        <PopoverTrigger
          class="relative w-full text-left px-4 py-2 rounded border cursor-pointer"
        >
          <span
            class="absolute start-0 inset-y-0 flex items-center justify-center px-3"
          >
            <Users class="size-3.5 dark:text-white text-black" />
          </span>
          <span class="ml-7 text-md">{{ summaryText }}</span>
        </PopoverTrigger>
        <PopoverContent class="p-4 w-72 space-y-4">
          <div class="flex justify-between items-center">
            <Label>Adults</Label>
            <Stepper v-model="adults" :min="1" />
          </div>
          <div class="flex justify-between items-center">
            <Label>Children</Label>
            <Stepper v-model="children" />
          </div>
          <div class="flex justify-between items-center">
            <Label>Infants</Label>
            <Stepper v-model="infants" />
          </div>
        </PopoverContent>
      </Popover>
      <div>
        <Dialog>
          <DialogTrigger
            class="w-full text-left px-4 py-2 rounded border cursor-pointer"
          >
            Hotels
          </DialogTrigger>
          <HotelListModal
            :selected="selected"
            :dateRange="dateRange"
            :country="country"
          />
        </Dialog>
      </div>
    </div>
  </div>
</template>
