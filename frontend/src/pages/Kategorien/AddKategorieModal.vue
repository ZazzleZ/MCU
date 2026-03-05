<script setup>
import { ref, watch } from "vue";

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
});

const emit = defineEmits(["update:modelValue", "created"]);

const kategoriename = ref("");
const errorMessage = ref("");
const isSubmitting = ref(false);

watch(
  () => props.modelValue,
  (isOpen) => {
    if (!isOpen) {
      return;
    }
    kategoriename.value = "";
    errorMessage.value = "";
    isSubmitting.value = false;
  },
);

const close = () => {
  emit("update:modelValue", false);
};

const createKategorie = async () => {
  const name = kategoriename.value.trim();
  if (!name) {
    errorMessage.value = "Bitte einen Kategorienamen eingeben.";
    return;
  }

  errorMessage.value = "";
  isSubmitting.value = true;

  try {
    const response = await fetch("http://localhost:8000/kategorien", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name,
        aussagenpaare: [],
      }),
    });

    if (!response.ok) {
      let message = `Kategorie konnte nicht erstellt werden (${response.status})`;
      try {
        const body = await response.json();
        if (typeof body?.detail === "string") {
          message = body.detail;
        }
      } catch {
        // ignore invalid JSON responses
      }
      throw new Error(message);
    }

    emit("created");
    close();
  } catch (error) {
    errorMessage.value = error?.message ?? "Unbekannter Fehler beim Erstellen.";
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<template>
  <div
    v-if="modelValue"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 px-4"
  >
    <div class="w-full max-w-md rounded-2xl bg-white p-6 shadow-lg">
      <h2 class="mb-4 text-lg font-semibold text-grey-text">Kategorie erstellen</h2>

      <label for="kategoriename-input" class="mb-1 block text-sm font-medium text-grey-text">
        Kategoriename
      </label>
      <input
        id="kategoriename-input"
        v-model="kategoriename"
        type="text"
        class="w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-sm outline-none transition focus:border-blue-500"
        placeholder="Kategoriename eingeben..."
        @keyup.enter="createKategorie"
      />

      <p v-if="errorMessage" class="mt-2 text-sm text-accent-red">
        {{ errorMessage }}
      </p>

      <div class="mt-5 flex justify-end gap-3">
        <button
          type="button"
          class="rounded-xl border border-accent-red bg-accent-red px-4 py-2 text-sm font-semibold text-white transition hover:bg-hover-red"
          :disabled="isSubmitting"
          @click="close"
        >
          Abbrechen
        </button>
        <button
          type="button"
          class="rounded-xl border border-main-blue bg-main-blue px-4 py-2 text-sm font-semibold text-white transition hover:brightness-95 disabled:cursor-not-allowed disabled:opacity-60"
          :disabled="isSubmitting"
          @click="createKategorie"
        >
          Erstellen
        </button>
      </div>
    </div>
  </div>
</template>

