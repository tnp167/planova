<script setup lang="ts">
import { ref } from "vue";
import { Dialog, DialogContent } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import HotelAddModal from "./HotelAddModal.vue";
import type { MapboxFeature } from "@/lib/types";
import type { DateRange } from "reka-ui";

const hotels = ref<
  {
    name: string;
    checkin: string;
    checkout: string;
  }[]
>([]);

const isAddOpen = ref(false);

const addHotel = (hotel: {
  name: string;
  checkin: string;
  checkout: string;
}) => {
  hotels.value.push(hotel);
  isAddOpen.value = false;
};

const props = defineProps<{
  selected: MapboxFeature | null;
  dateRange: DateRange;
  country: string | undefined;
}>();
</script>

<template>
  <DialogContent>
    <div>
      <h2 class="text-lg font-semibold mb-4">Your Hotels</h2>
      <ul class="space-y-2">
        <li
          v-for="(hotel, index) in hotels"
          :key="index"
          class="border p-3 rounded bg-muted"
        >
          <p class="font-medium">{{ hotel.name }}</p>
          <p class="text-sm text-muted-foreground">
            {{ hotel.checkin }} → {{ hotel.checkout }}
          </p>
        </li>
      </ul>
      <Button class="mt-4 w-full" @click="isAddOpen = true"
        >➕ Add Hotel</Button
      >

      <Dialog :open="isAddOpen" @update:open="isAddOpen = $event">
        <HotelAddModal
          :selected="props.selected"
          :dateRange="props.dateRange"
          :country="props.country"
          :onSave="addHotel"
          :onClose="() => (isAddOpen = false)"
        />
      </Dialog>
    </div>
  </DialogContent>
</template>
