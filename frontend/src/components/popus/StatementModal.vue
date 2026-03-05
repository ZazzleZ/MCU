<template>
  <div v-if="modelValue" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
    <div class="w-[420px] rounded-2xl border-4 border-[#538fc6]/90 bg-white p-6">

      <!-- Feedback Banner -->
      <div v-if="feedback.message" class="mb-4">
        <div
          :class="[
            'rounded-xl px-4 py-3 text-sm',
            feedback.type === 'success' ? 'bg-green-50 text-green-700 border border-green-300' : '',
            feedback.type === 'error' ? 'bg-red-50 text-red-700 border border-red-300' : ''
          ]"
        >
          {{ feedback.message }}
        </div>
      </div>

      <!-- Aussagen -->
      <div v-for="(item, index) in localStatements" :key="index" class="mb-4">
        <div class="mb-2 flex items-center justify-between font-semibold">
          <span>Aussage {{ index + 1 }}</span>

          <label class="flex items-center gap-2">
            korrekt?
            <input type="checkbox" v-model="item.correct" class="h-5 w-5 accent-red-500" />
          </label>
        </div>

        <textarea
          v-model="item.text"
          class="h-24 w-full rounded-xl border-2 border-[#538fc6]/90 bg-white p-3 text-white placeholder:text-gray-500/70"
          placeholder="Hier kannst du deine Aussage hinzufügen..."
        ></textarea>
      </div>

      <!-- Kommentar -->
      <div class="mb-4">
        <div class="mb-2 font-semibold">Kommentar</div>
        <textarea
          v-model="kommentar"
          class="h-24 w-full rounded-xl border-2 border-[#538fc6]/90 bg-white p-3 text-white placeholder:text-gray-500/70"
          placeholder="Hier kannst du einen Kommentar hinzufügen..."
        ></textarea>
      </div>

      <!-- Kategorie Auswahl -->
      <div class="mb-4">
        <label class="font-semibold">Kategorie</label>
        <select v-model="kategorie" class="w-full cursor-pointer p-2 border rounded-xl">
          <option disabled value="">Bitte auswählen</option>
          <option v-for="cat in kategorien" :key="cat.id" :value="cat.name">
            {{ cat.name }}
          </option>
        </select>
      </div>

      <!-- Grafik Upload -->
      <div class="mb-4">
        <label class="font-semibold">Grafik</label>
        <input type="file" @change="uploadGraphic" />
        <div v-if="grafik_url" class="mt-2 text-xs text-gray-500 truncate">Gespeichert: {{ grafik_url }}</div>
      </div>

      <!-- Footer -->
      <div class="flex justify-between">
        <button class="rounded-lg bg-[#dd4d4d] px-6 py-2 text-white" @click="close" :disabled="saving">
          Abbrechen
        </button>

        <button
          class="rounded-lg bg-[#538fc6] px-6 py-2 text-white inline-flex items-center gap-2 disabled:opacity-60"
          @click="save"
          :disabled="saving"
        >
          <svg v-if="saving" class="h-4 w-4 animate-spin" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="white" stroke-width="4" fill="none"/>
            <path class="opacity-75" fill="white" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"/>
          </svg>
          <span>{{ saving ? 'Speichere…' : 'Speichern' }}</span>
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from "vue";

const props = defineProps({
  modelValue: { type: Boolean, required: true },
  statements: {
    type: Array,
    default: () => [{ correct: false, text: "" }, { correct: false, text: "" }]
  }
});

const emit = defineEmits(["update:modelValue", "save", "saved"]); // "saved" = optionales Erfolgs-Event

// lokale Kopie
const localStatements = reactive(
  JSON.parse(JSON.stringify(props.statements)).map(s => ({ text: s.text || "", correct: !!s.correct }))
);

const kommentar = ref("");
const kategorie = ref("");
const grafik_url = ref(localStorage.getItem("uploadedGraphic") || "");
const kategorien = ref([]);

const saving = ref(false);
const feedback = reactive({ type: "", message: "" }); // type: 'success' | 'error'

// Kategorien laden
onMounted(async () => {
  try {
    const res = await fetch("http://localhost:8000/kategories");
    if (!res.ok) throw new Error(`Kategorien konnten nicht geladen werden (${res.status})`);
    kategorien.value = await res.json();
  } catch (e) {
    feedback.type = "error";
    feedback.message = e.message || "Fehler beim Laden der Kategorien.";
  }
});

// Grafik Upload → URL speichern (hier als Blob-URL + LocalStorage, alternativ: echter Upload an Backend)
function uploadGraphic(event) {
  const file = event.target.files[0];
  if (!file) return;
  const url = URL.createObjectURL(file);
  grafik_url.value = url;
  localStorage.setItem("uploadedGraphic", url);
}

const close = () => emit("update:modelValue", false);

async function save() {
  feedback.type = "";
  feedback.message = "";

  // einfache Validierung
  if (!kategorie.value) {
    feedback.type = "error";
    feedback.message = "Bitte eine Kategorie auswählen.";
    return;
  }
  if (localStatements.some(s => !s.text?.trim())) {
    feedback.type = "error";
    feedback.message = "Bitte alle Aussagen ausfüllen.";
    return;
  }

  const payload = {
    aussagen: localStatements.map((s, idx) => ({
      id: `${Date.now()}-${idx}`,     // falls Backend ID generiert, kannst du das weglassen
      aussage: s.text,
      loesung: !!s.correct
    })),
    kategorie: [kategorie.value],      // dein Backend erwartet eine Liste
    bearbeiter: "Mostafa",
    grafik_url: grafik_url.value || "",
    kommentar: kommentar.value || ""
  };

  saving.value = true;
  try {
    const res = await fetch("http://localhost:8000/aussagepaare", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    // Versuche Fehlermeldung vom Backend sauber anzuzeigen
    let data = null;
    try { data = await res.json(); } catch {}

    if (!res.ok) {
      const msg = (data && (data.detail || data.message)) || `Speichern fehlgeschlagen (HTTP ${res.status}).`;
      throw new Error(msg);
    }

    // Erfolg
    feedback.type = "success";
    feedback.message = "Erfolgreich gespeichert.";
    emit("save", payload);  // falls Elternkomponente noch etwas braucht
    emit("saved", data || payload);

    // Modal nach kurzer Zeit schließen (anpassbar)
    setTimeout(() => close(), 900);

  } catch (err) {
    feedback.type = "error";
    feedback.message = err?.message || "Unbekannter Fehler beim Speichern.";
  } finally {
    saving.value = false;
  }
}
</script>
