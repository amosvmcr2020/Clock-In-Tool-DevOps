import { writable } from "svelte/store";

const stored = localStorage.getItem("current_user_id");

export const current_user_id = writable(stored || null);

current_user_id.subscribe((value) => {
  if (value === null) {
    localStorage.removeItem("current_user_id");
  } else {
    localStorage.current_user_id = value;
  }
});
