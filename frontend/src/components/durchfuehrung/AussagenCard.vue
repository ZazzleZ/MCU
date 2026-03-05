<script setup>
import { computed, ref, watch } from "vue";
import { getAussageText, getCorrectValueForPair } from "./aussagenpaarUtils";

const props = defineProps({
  aussagenpaar: {
    type: Object,
    required: true,
  },
  selectedValue: {
    type: Number,
    default: null,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  isKlausur: {
    type: Boolean,
    default: false,
  },
  buttonLabels: {
    type: Array,
    default: () => ["0", "1", "2", "3"],
  },
  cardClass: {
    type: String,
    default: "",
  },
});

const emit = defineEmits(["select"]);

const internalSelectedValue = ref(props.selectedValue);

watch(
  () => props.selectedValue,
  (value) => {
    internalSelectedValue.value = value;
  },
);

const aussageEins = computed(() => {
  if (props.aussagenpaar?.aussage_eins) {
    return props.aussagenpaar.aussage_eins;
  }

  if (Array.isArray(props.aussagenpaar?.aussagen) && props.aussagenpaar.aussagen[0]) {
    return getAussageText(props.aussagenpaar.aussagen[0]);
  }

  return "";
});

const aussageZwei = computed(() => {
  if (props.aussagenpaar?.aussage_zwei) {
    return props.aussagenpaar.aussage_zwei;
  }

  if (Array.isArray(props.aussagenpaar?.aussagen) && props.aussagenpaar.aussagen[1]) {
    return getAussageText(props.aussagenpaar.aussagen[1]);
  }

  return "";
});

const correctValue = computed(() => getCorrectValueForPair(props.aussagenpaar));
const kategorien = computed(() =>
  Array.isArray(props.aussagenpaar?.kategorie) ? props.aussagenpaar.kategorie : [],
);

const values = [0, 1, 2, 3];

function getButtonClass(value) {
  const selected = internalSelectedValue.value;

  if (selected === null || selected === undefined) {
    return "border-slate-300 bg-white text-slate-700 hover:border-main-blue hover:text-main-blue";
  }

  if (selected !== value) {
    return "border-slate-300 bg-white text-slate-700";
  }

  if (props.isKlausur) {
    return "border-main-blue bg-main-blue text-white";
  }

  if (selected === correctValue.value) {
    return "border-emerald-600 bg-emerald-600 text-white";
  }

  return "border-accent-red bg-accent-red text-white";
}

function selectValue(value) {
  if (props.disabled) {
    return;
  }

  internalSelectedValue.value = value;

  emit("select", {
    value,
    aussagenpaar: props.aussagenpaar,
    isCorrect: value === correctValue.value,
    correctValue: correctValue.value,
  });
}
</script>

<template>
  <article
    class="w-full rounded-2xl border border-slate-200 bg-white p-4 shadow-sm sm:p-5"
    :class="cardClass"
  >
    <div v-if="kategorien.length > 0" class="mb-3 flex flex-wrap gap-2">
      <span
        v-for="kategorie in kategorien"
        :key="kategorie"
        class="inline-flex items-center rounded-full border border-main-blue/30 bg-main-blue/10 px-2.5 py-1 text-xs font-medium text-main-blue"
      >
        {{ kategorie }}
      </span>
    </div>

    <div class="space-y-3">
      <p class="rounded-xl bg-slate-50 px-3 py-3 text-sm leading-relaxed text-slate-800 sm:text-base">
        {{ aussageEins }}
      </p>
      <p class="rounded-xl bg-slate-50 px-3 py-3 text-sm leading-relaxed text-slate-800 sm:text-base">
        {{ aussageZwei }}
      </p>
      <p
        v-if="!isKlausur && internalSelectedValue !== null && internalSelectedValue !== undefined && aussagenpaar?.kommentar"
        class="px-1 pt-1 text-xs leading-relaxed text-slate-500 sm:text-sm"
      >
        {{ aussagenpaar.kommentar }}
      </p>
    </div>

    <div class="mt-4 grid grid-cols-4 gap-2">
      <button
        v-for="(value, index) in values"
        :key="value"
        type="button"
        class="min-h-11 rounded-lg border text-sm font-semibold transition active:scale-[0.98] md:cursor-pointer disabled:cursor-not-allowed disabled:opacity-60"
        :class="getButtonClass(value)"
        :aria-pressed="internalSelectedValue === value"
        :disabled="disabled"
        @click="selectValue(value)"
      >
        {{ buttonLabels[index] ?? value }}
      </button>
    </div>
  </article>
</template>
