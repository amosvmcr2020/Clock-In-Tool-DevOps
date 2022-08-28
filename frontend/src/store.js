import { writable } from "svelte/store"

const stored = localStorage.getItem('current_user_id')

export const current_user_id = writable(stored || 0);

current_user_id.subscribe((value) => localStorage.current_user_id = value)