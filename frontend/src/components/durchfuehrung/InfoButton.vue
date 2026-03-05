<script setup>
import { onBeforeUnmount, onMounted, ref } from "vue";

const props = defineProps({
  text: {
    type: String,
    default: "Wähle für jedes Aussagenpaar eine Antwort von 0 bis 3 und klicke danach auf Beenden.",
  },
});

const showInfoPopup = ref(false);
const infoPopupRef = ref(null);
const infoButtonRef = ref(null);

function toggleInfoPopup() {
  showInfoPopup.value = !showInfoPopup.value;
}

function handleDocumentClick(event) {
  if (!showInfoPopup.value) {
    return;
  }

  const target = event.target;
  const clickedInsidePopup = infoPopupRef.value?.contains(target);
  const clickedInfoButton = infoButtonRef.value?.contains(target);

  if (!clickedInsidePopup && !clickedInfoButton) {
    showInfoPopup.value = false;
  }
}

onMounted(() => {
  document.addEventListener("click", handleDocumentClick);
});

onBeforeUnmount(() => {
  document.removeEventListener("click", handleDocumentClick);
});
</script>

<template>
  <div class="relative">
    <button
      ref="infoButtonRef"
      type="button"
      class="inline-flex h-10 w-10 items-center justify-center rounded-lg border transition md:cursor-pointer"
      :class="
        showInfoPopup
          ? 'border-main-blue bg-main-blue text-white'
          : 'border-main-blue bg-white text-main-blue hover:bg-main-blue hover:text-white'
      "
      aria-label="Informationen anzeigen"
      @click="toggleInfoPopup"
    >
      <svg class="h-5 w-5" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
        <path d="M12 2a10 10 0 1 0 10 10A10.01 10.01 0 0 0 12 2Zm0 4.75a1.25 1.25 0 1 1-1.25 1.25A1.25 1.25 0 0 1 12 6.75Zm1.5 10.5h-3a.75.75 0 0 1 0-1.5h.75V11.5h-.75a.75.75 0 0 1 0-1.5h1.5a.75.75 0 0 1 .75.75v5h.75a.75.75 0 0 1 0 1.5Z" />
      </svg>
    </button>
    <div
      v-if="showInfoPopup"
      ref="infoPopupRef"
      class="absolute left-0 z-10 mt-2 w-72 rounded-lg border border-slate-200 bg-white p-3 text-sm text-slate-700 shadow-lg"
    >
      {{ props.text }}
    </div>
  </div>
</template>
