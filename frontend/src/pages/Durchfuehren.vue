<script setup>
import { computed, ref, watch } from "vue";
import { useRoute } from "vue-router";
import AussagenCard from "../components/durchfuehrung/AussagenCard.vue";
import EndCard from "../components/durchfuehrung/EndCard.vue";
import InfoButton from "../components/durchfuehrung/InfoButton.vue";
import {
  buildShuffledKlausurPairs,
  getCorrectValueForPair,
} from "../components/durchfuehrung/aussagenpaarUtils";
import testData from "../assets/test.json";

const BUTTON_LABELS = ["0", "1", "2", "3"];
const route = useRoute();

const requestedUebungId = computed(() => {
  const idFromParam = route.params.uebungId;
  return typeof idFromParam === "string" ? idFromParam : "";
});

const loadedUebung = computed(() => {
  return requestedUebungId.value === "aufgabe0001" ? testData : null;
});
const originalAussagenpaare = computed(() =>
  Array.isArray(loadedUebung.value?.aussagenpaare) ? loadedUebung.value.aussagenpaare : [],
);
const isKlausur = ref(false);
const isFinished = ref(false);
const selectedValuesByPairId = ref({});
const activeAussagenpaare = ref([]);
const hasValidUebung = computed(() => Boolean(loadedUebung.value));

function refreshPairsForMode() {
  activeAussagenpaare.value = isKlausur.value
    ? buildShuffledKlausurPairs(originalAussagenpaare.value)
    : originalAussagenpaare.value;
}

watch(
  loadedUebung,
  (uebung) => {
    selectedValuesByPairId.value = {};
    isFinished.value = false;
    isKlausur.value = Boolean(uebung?.is_klausur);
    refreshPairsForMode();
  },
  { immediate: true },
);

const totalCount = computed(() => activeAussagenpaare.value.length);
const correctCount = computed(() =>
  activeAussagenpaare.value.reduce((count, aussagenpaar) => {
    const selected = selectedValuesByPairId.value[aussagenpaar.id];
    if (selected === undefined || selected === null) {
      return count;
    }
    return selected === getCorrectValueForPair(aussagenpaar) ? count + 1 : count;
  }, 0),
);
const scoreText = computed(() => `${correctCount.value}/${totalCount.value}`);

function handleSelection(payload) {
  const pairId = payload?.aussagenpaar?.id;
  if (!pairId) {
    return;
  }
  selectedValuesByPairId.value[pairId] = payload.value;
  console.log("Selected:", payload);
}

function finishSession() {
  isFinished.value = true;
}

function restartSession() {
  selectedValuesByPairId.value = {};
  isFinished.value = false;
  refreshPairsForMode();
}

function switchToPracticeMode() {
  isKlausur.value = false;
  restartSession();
}

function toggleKlausurMode() {
  isKlausur.value = !isKlausur.value;
  restartSession();
}
</script>

<template>
  <div v-if="hasValidUebung" class="max-w-relative mx-auto flex w-full max-w-2xl flex-col gap-5">
    <div class="grid grid-cols-3 items-center gap-3">
      <div class="justify-self-start">
        <InfoButton v-if="!isFinished" />
      </div>
      <p
        class="justify-self-center text-center text-sm font-semibold tracking-wide text-grey-text sm:text-base"
      >
        {{ loadedUebung.aufgabenname }}
      </p>
      <button
        v-if="!isFinished"
        type="button"
        :class="[
          'col-start-3 h-10 justify-self-end rounded-lg border px-4 text-sm font-semibold transition md:cursor-pointer',
          isKlausur
            ? 'border-main-blue bg-main-blue text-white hover:brightness-95'
            : 'border-main-blue bg-white text-main-blue hover:bg-main-blue/5',
        ]"
        @click="toggleKlausurMode"
      >
        K
      </button>
    </div>

    <template v-if="!isFinished">
      <AussagenCard
        v-for="value in activeAussagenpaare"
        :key="value.id"
        :aussagenpaar="value"
        :selectedValue="selectedValuesByPairId[value.id]"
        :disabled="false"
        :isKlausur="isKlausur"
        :buttonLabels="BUTTON_LABELS"
        cardClass="my-card-class"
        @select="handleSelection"
      />
      <button
        type="button"
        class="rounded-lg border border-main-blue bg-main-blue px-4 py-2.5 text-sm font-semibold text-white transition hover:brightness-95 md:cursor-pointer"
        @click="finishSession"
      >
        Beenden
      </button>
    </template>
    <div v-else class="flex min-h-[70vh] items-center justify-center">
      <EndCard
        :scoreText="scoreText"
        :isKlausur="isKlausur"
        @retry="restartSession"
        @switch-to-uebung="switchToPracticeMode"
      />
    </div>
  </div>
  <div v-else class="mx-auto flex min-h-[70vh] max-w-2xl items-center justify-center px-6 text-center">
    <p class="text-lg font-semibold text-grey-text">
      Uebung mit ID "{{ requestedUebungId }}" wurde nicht gefunden.
    </p>
  </div>
</template>
