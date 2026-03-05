<script setup>
const props = defineProps({
  scoreText: {
    type: String,
    required: true,
  },
  isKlausur: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["retry", "switch-to-uebung"]);
</script>

<template>
  <article class="mx-auto w-full max-w-xl rounded-2xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8">
    <div class="space-y-2 text-center">
      <p class="text-2xl font-medium text-slate-700">{{ props.scoreText }}</p>
      <p class="text-base font-medium text-slate-700">Richtig</p>
    </div>

    <div class="mt-6 flex flex-col items-center gap-3">
      <button
        type="button"
        class="min-w-56 rounded-lg border border-main-blue bg-main-blue px-4 py-2.5 text-sm font-semibold text-white transition hover:brightness-95 md:cursor-pointer"
        @click="emit('retry')"
      >
        Wiederholen
      </button>
      <button
        v-if="props.isKlausur"
        type="button"
        class="min-w-56 rounded-lg border border-main-blue bg-white px-4 py-2.5 text-sm font-semibold text-main-blue transition hover:bg-main-blue hover:text-white md:cursor-pointer"
        @click="emit('switch-to-uebung')"
      >
        Zum Übungsmodus
      </button>
    </div>
  </article>
</template>
