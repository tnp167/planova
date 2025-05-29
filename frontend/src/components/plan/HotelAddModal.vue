<script setup lang="ts">
import { ref, computed } from "vue";
import {
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import type { MapboxFeature } from "@/lib/types";
import type { DateRange } from "reka-ui";
import { Input } from "@/components/ui/input";
import axios from "axios";
import type {
  HotelResponse,
  Hotel,
  AddressResponse,
  Address,
  StayLocation,
} from "@/lib/types";
import { useAuth } from "@clerk/vue";
import { watch, onMounted, onUnmounted } from "vue";
import { X } from "lucide-vue-next";
import TripDateRangePicker from "@/components/ui/date-range-picker/DateRangePicker.vue";
import Map from "@/components/plan/Map.vue";

const props = defineProps<{
  selected: MapboxFeature | null;
  dateRange: DateRange;
  country: string | undefined;
  onSave: (hotel: { name: string; checkin: string; checkout: string }) => void;
  onClose: () => void;
}>();

const query = ref<string>("");
const suggestions = ref<HotelResponse>([]);
const selected = ref<StayLocation | null>(null);
let debounceTimeout: number | undefined;
const dropdownRef = ref<HTMLElement | null>(null);
const { getToken } = useAuth();
const showAddAddress = ref<boolean>(false);
const address = ref<AddressResponse | null>(null);
const hasText = ref(false);
const stayRange = ref<DateRange>(props.dateRange);
watch([query], async ([newVal]) => {
  clearTimeout(debounceTimeout);

  debounceTimeout = window.setTimeout(async () => {
    const token = await getToken.value();

    if (!newVal || newVal.length < 2 || !props.country) {
      suggestions.value = [];
      address.value = null;
      return;
    }

    hasText.value = newVal.length > 0;
    try {
      if (!showAddAddress.value) {
        const res = await axios.get<HotelResponse>(
          `${import.meta.env.VITE_API_URL}/api/location/hotel-autocomplete/`,
          {
            params: {
              q: newVal,
              countryCode: props.country,
            },
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        suggestions.value = res.data;
      } else {
        const res = await axios.get<AddressResponse>(
          `${import.meta.env.VITE_API_URL}/api/location/address-autocomplete/`,
          {
            params: { q: newVal, countryCode: props.country },
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        address.value = res.data;
      }
    } catch (err) {
      console.error("Autocomplete error:", err);
      suggestions.value = [];
    }
  }, 300);
});

const handleSave = () => {
  if (!selected.value || !stayRange.value.start || !stayRange.value.end) return;

  props.onSave({
    name: selected.value.name,
    checkin: props.dateRange.start?.toString() || "",
    checkout: props.dateRange.end?.toString() || "",
  });
  props.onClose();
};

const handleClickOutside = (event: MouseEvent) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target as Node)) {
    suggestions.value = [];
    address.value = null;
  }
};

onMounted(() => {
  document.addEventListener("click", handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener("click", handleClickOutside);
});

function selectHotel(hotel: Hotel) {
  selected.value = {
    id: hotel.id.toString(),
    name: hotel.name,
    checkin: props.dateRange.start?.toString() || "",
    checkout: props.dateRange.end?.toString() || "",
    coordinates: {
      latitude: hotel.geoCode.latitude,
      longitude: hotel.geoCode.longitude,
    },
  };
  query.value = hotel.name;
  handleClickOutside(new MouseEvent("click"));
}

const selectAddress = (address: Address) => {
  selected.value = {
    id: address.properties.mapbox_id,
    name: address.properties.full_address,
    checkin: props.dateRange.start?.toString() || "",
    checkout: props.dateRange.end?.toString() || "",
    coordinates: {
      latitude: address.geometry.coordinates[1],
      longitude: address.geometry.coordinates[0],
    },
  };
  query.value = address.properties.full_address;
  handleClickOutside(new MouseEvent("click"));
};

const clearQuery = () => {
  query.value = "";
  selected.value = null;
  hasText.value = false;
};
</script>

<template>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Add Hotel</DialogTitle>
    </DialogHeader>
    <div class="space-y-4 py-4">
      <div class="space-y-2">
        <label class="text-sm font-medium"
          >{{ !showAddAddress ? "Hotel Name" : "Accommodation Address" }}
        </label>
        <div
          ref="dropdownRef"
          class="relative w-full max-w-sm items-center"
          v-if="!showAddAddress"
        >
          <button
            v-if="hasText"
            type="button"
            @click="clearQuery"
            class="absolute right-2 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-primary"
          >
            <X class="w-4 h-4" />
          </button>
          <Input v-model="query" placeholder="Enter hotel name" />
          <ul
            v-if="!showAddAddress && suggestions.length"
            class="absolute z-10 w-full border mt-1 rounded shadow-lg max-h-64 overflow-auto"
          >
            <li
              v-for="(place, index) in suggestions"
              :key="place.id"
              class="px-4 py-2 cursor-pointer bg-background text-foreground hover:bg-accent hover:text-accent-foreground border-b border-border transition-colors duration-200 ease-in-out"
              :class="{
                'rounded-t-md border-0': index === 0,
                'rounded-b-md border-0': index === suggestions.length - 1,
                'bg-muted': selected?.id === place.id.toString(),
              }"
              @click="selectHotel(place)"
            >
              {{ place.name }}, {{ place.address.cityName }},
              {{ place.address.countryCode }}
            </li>
          </ul>
        </div>
        <div
          ref="dropdownRef"
          class="relative w-full max-w-sm items-center"
          v-else-if="showAddAddress"
        >
          <button
            v-if="hasText"
            type="button"
            @click="clearQuery"
            class="absolute right-2 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-primary"
          >
            <X class="w-4 h-4" />
          </button>
          <Input v-model="query" placeholder="Enter address" />
          <ul
            v-if="address?.features.length"
            class="absolute z-10 w-full border mt-1 rounded shadow-lg max-h-64 overflow-auto"
          >
            <li
              v-for="(place, index) in address.features"
              :key="place.properties.mapbox_id"
              class="px-4 py-2 cursor-pointer bg-background text-foreground hover:bg-accent hover:text-accent-foreground border-b border-border transition-colors duration-200 ease-in-out"
              :class="{
                'rounded-t-md border-0': index === 0,
                'rounded-b-md border-0': index === address.features.length - 1,
                'bg-muted': selected?.id === place.properties.mapbox_id,
              }"
              @click="selectAddress(place)"
            >
              {{ place.properties.full_address }}
            </li>
          </ul>
        </div>

        <p
          class="text-xs text-primary underline cursor-pointer"
          @click="
            () => {
              showAddAddress = !showAddAddress;
              clearQuery();
            }
          "
        >
          {{
            showAddAddress
              ? "Prefer to search by hotel name instead?"
              : "Can't find hotel? Add address manually"
          }}
        </p>
      </div>
      <div class="space-y-2">
        <label class="block text-sm font-medium">Check-in and Check-out</label>
        <TripDateRangePicker
          v-model="stayRange"
          :default-value="props.dateRange"
          :min-value="props.dateRange.start"
          :max-value="props.dateRange.end"
        />
      </div>
      <div class="space-y-2 mt-4">
        <label class="text-sm font-medium">Hotel Location</label>
        <Map v-if="selected" :location="selected" />
      </div>
    </div>
    <div class="flex justify-end gap-3">
      <Button variant="outline" @click="props.onClose">Cancel</Button>
      <Button @click="handleSave" :disabled="!selected">Save</Button>
    </div>
  </DialogContent>
</template>
