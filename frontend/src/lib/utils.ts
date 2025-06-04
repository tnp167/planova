import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";
import { format, getMonth, parseISO } from "date-fns";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatTripDates(startDate: string, endDate: string) {
  const startDateObj = parseISO(startDate);
  const endDateObj = parseISO(endDate);
  if (startDateObj.getMonth() === endDateObj.getMonth()) {
    return `${format(startDateObj, "d")}–${format(endDateObj, "d MMM yyyy")}`;
  }

  return `${format(startDateObj, "d MMM")}–${format(endDateObj, "d MMM yyyy")}`;
}
