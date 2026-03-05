<script setup>
defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
  title: {
    type: String,
    default: "Kategorie wirklich loeschen?",
  },
  detail: {
    type: String,
    default: "",
  },
});

const emit = defineEmits(["update:modelValue", "confirm"]);

const close = () => {
  emit("update:modelValue", false);
};

const confirm = () => {
  emit("confirm");
};
</script>

<template>
  <div
    v-if="modelValue"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 px-4"
  >
    <div class="w-full max-w-md rounded-2xl bg-white p-6 shadow-lg">
      <h2 class="mb-2 text-lg font-normal text-grey-text">
        <template v-if="detail">
          {{ title }}
          <span class="font-semibold">{{ detail }}</span>
          loeschen?
        </template>
        <template v-else>
          {{ title }}
        </template>
      </h2>

      <div class="mt-5 flex justify-end gap-3">
        <button
          type="button"
          class="rounded-xl border border-slate-300 bg-white px-4 py-2 text-sm font-semibold text-slate-700 transition hover:bg-slate-100"
          @click="close"
        >
          Abbrechen
        </button>
        <button
          type="button"
          class="rounded-xl border border-accent-red bg-accent-red px-4 py-2 text-sm font-semibold text-white transition hover:bg-hover-red"
          @click="confirm"
        >
          Loeschen
        </button>
      </div>
    </div>
  </div>
</template>
