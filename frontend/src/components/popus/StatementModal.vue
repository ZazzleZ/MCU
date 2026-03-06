<template>
  <div v-if="modelValue" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
    <div class="w-[420px] rounded-2xl border-4 border-[#538fc6]/90 bg-white p-6">

      <!-- Feedback Banner -->
      <div v-if="feedback.message" class="mb-4">
        <div
          :class="[
            'rounded-xl px-4 py-3 text-sm',
            feedback.type === 'success'
              ? 'bg-green-50 text-green-700 border border-green-300'
              : 'bg-red-50 text-red-700 border border-red-300'
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
          class="h-24 w-full rounded-xl border-2 border-[#538fc6]/90 bg-white p-3 text-black"
          placeholder="Hier kannst du deine Aussage hinzufügen..."
        ></textarea>
      </div>

      <!-- Kommentar -->
      <div class="mb-4">
        <div class="mb-2 font-semibold">Kommentar</div>
        <textarea
          v-model="kommentar"
          class="h-24 w-full rounded-xl border-2 border-[#538fc6]/90 bg-white p-3 text-black"
          placeholder="Hier kannst du einen Kommentar hinzufügen..."
        ></textarea>
      </div>

      <!-- Kategorie Auswahl -->
      <div class="mb-4">
        <label class="font-semibold">Kategorie</label>
        <select v-model="kategorie" class="w-full cursor-pointer p-2 border rounded-xl">
          <option disabled value="">Bitte auswählen</option>
          <option v-for="cat in kategorien" :key="cat.id" :value="cat.id">
            {{ cat.name }}
          </option>
        </select>

        <div v-if="!kategorien.length" class="mt-1 text-xs text-gray-500">
          (Keine Kategorien geladen – bitte Backend prüfen)
        </div>
      </div>

      <!-- Grafik Upload (modernes Design) -->
      <div class="mb-4">
        <label class="font-semibold">Grafik</label>

        <!-- Click/Drop Zone -->
        <label
          class="mt-2 flex flex-col items-center justify-center w-full h-32
                 border-2 border-dashed border-[#538fc6] rounded-xl cursor-pointer
                 hover:border-blue-400 hover:bg-blue-50/30 transition group"
        >
          <div class="flex flex-col items-center gap-2 pointer-events-none px-4">
            <!-- Upload Icon -->
            <svg class="w-10 h-10 text-[#538fc6] group-hover:text-blue-500 transition" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round"
                d="M12 16V4m0 0l-4 4m4-4l4 4M6 20h12a2 2 0 002-2v-4a2 2 0 00-2-2H6a2 2 0 00-2 2v4a2 2 0 002 2z" />
            </svg>

            <span class="text-sm text-gray-600 group-hover:text-blue-600 transition text-center">
              Klicke zum Auswählen oder Datei hierher ziehen
            </span>

            <!-- Dateiname/URL -->
            <span v-if="grafik_url" class="text-xs text-gray-500 truncate max-w-[280px]">
              {{ grafik_url }}
            </span>
          </div>

          <!-- Hidden Input -->
          <input type="file" accept="image/*" class="hidden" @change="uploadGraphic" />
        </label>

        <!-- Vorschau -->
        <div v-if="grafik_url" class="mt-3">
          grafik_url
        </div>
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
  modelValue: Boolean,
  statements: Array
});
const emit = defineEmits(["update:modelValue", "save", "saved"]);

const API_BASE = "http://127.0.0.1:8000";

/* ------------------------------ Lokale Aussagenliste ------------------------------ */
const localStatements = reactive(
  JSON.parse(JSON.stringify(props.statements)).map(s => ({
    text: s.text || "",
    correct: !!s.correct
  }))
);

/* ------------------------------ Form States ------------------------------ */
const kommentar = ref("");
const kategorie = ref("");
const grafik_url = ref(localStorage.getItem("uploadedGraphic") || "");
const kategorien = ref([]);

const saving = ref(false);
const feedback = reactive({ type: "", message: "" });

/* ------------------------------ Helpers ------------------------------ */
async function postJson(url, body) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body)
  });

  let data = null;
  try { data = await res.json(); } catch {}

  if (!res.ok) {
    const msg = data?.detail || data?.message || `Fehler (HTTP ${res.status})`;
    throw new Error(typeof msg === "string" ? msg : JSON.stringify(msg));
  }
  return data;
}

async function patchJson(url, body) {
  const res = await fetch(url, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body)
  });

  let data = null;
  try { data = await res.json(); } catch {}

  if (!res.ok) {
    // Detail-Text ausgeben, damit man Schema-Fehler sieht
    let detail = "";
    try { detail = await res.text(); } catch {}
    throw new Error(detail || `Fehler (HTTP ${res.status})`);
  }
  return data;
}

/* ------------------------------ Kategorien laden ------------------------------ */
onMounted(async () => {
  try {
    const res = await fetch(`${API_BASE}/kategorien`);
    kategorien.value = await res.json();
  } catch (err) {
    console.error("Fehler beim Laden der Kategorien:", err);
  }
});

/* ------------------------------ Grafik Upload ------------------------------ */
function uploadGraphic(evt) {
  const file = evt.target.files[0];
  if (!file) return;

  const url = URL.createObjectURL(file);
  grafik_url.value = url;
  localStorage.setItem("uploadedGraphic", url);
}

/* ------------------------------ Modal schließen ------------------------------ */
const close = () => emit("update:modelValue", false);

/* ------------------------------ Paar-Update: PATCH mit kompletter Ressource ------------------------------ */
/** 
 * Dein Backend verlangt im PATCH-Body: id, kategorie, bearbeiter, grafik_url, kommentar, aussagen
 * (siehe 422-Detail in deiner Konsole).
 * Deshalb senden wir HIER die komplette Ressource mit den neuen aussagen-IDs.
 */
async function updatePairAussagenMitVollerRessource(pairId, aussagenIds, pairSnapshot) {
  // pairSnapshot ist die Antwort vom Create; falls dort etwas fehlt, nehmen wir die aktuellen Form-Werte.
  const fullPayload = {
    id: pairId,
    aussagen: aussagenIds, // NUR IDs!
    kategorie: Array.isArray(pairSnapshot?.kategorie) && pairSnapshot.kategorie.length
      ? pairSnapshot.kategorie
      : [kategorie.value],
    bearbeiter: pairSnapshot?.bearbeiter ?? "Mostafa",
    grafik_url: pairSnapshot?.grafik_url ?? grafik_url.value,
    kommentar: pairSnapshot?.kommentar ?? kommentar.value
  };

  // Wichtig: PATCH (PUT ist bei dir 405 → nicht erlaubt)
  return await patchJson(`${API_BASE}/aussagenpaare/${pairId}`, fullPayload);
}

/* ------------------------------ SPEICHERN ------------------------------ */
async function save() {
  feedback.message = "";
  feedback.type = "";

  // Validierungen
  if (!kategorie.value) {
    feedback.type = "error";
    feedback.message = "Bitte eine Kategorie auswählen.";
    return;
  }
  if (localStatements.some(s => !s.text.trim())) {
    feedback.type = "error";
    feedback.message = "Bitte alle Aussagen ausfüllen.";
    return;
  }

  saving.value = true;
  const nowIso = new Date().toISOString();

  // 1) Paar zuerst LEER anlegen
  const pairPayload = {
    aussagen: [], // leer starten
    kategorie: [kategorie.value],
    bearbeiter: "Mostafa",
    grafik_url: grafik_url.value,
    kommentar: kommentar.value
  };

  let pairId = null;
  const createdStatementIds = [];

  try {
    /* -------- 1. Aussagenpaar erstellen -------- */
    const pairData = await postJson(`${API_BASE}/aussagenpaare`, pairPayload);
    pairId = pairData.id;
    if (!pairId) throw new Error("Fehlende ID des gespeicherten Aussagenpaars.");

    /* -------- 2. Aussagen einzeln erstellen -------- */
    for (const s of localStatements) {
      const stmt = await postJson(`${API_BASE}/aussagen`, {
        aussagenpaar_id: pairId,
        aussage: s.text.trim(),
        loesung: !!s.correct,
        aenderungsdatum: nowIso
      });

      if (!stmt?.id) throw new Error("Aussage-ID fehlt in der Antwort.");
      createdStatementIds.push(stmt.id);
    }

    /* -------- 3. Paar PATCHEN → komplette Ressource, nur aussagen=IDs -------- */
    const updatedPair = await updatePairAussagenMitVollerRessource(
      pairId,
      createdStatementIds,
      pairData
    );

    /* -------- Erfolg -------- */
    feedback.type = "success";
    feedback.message = "Erfolgreich gespeichert.";

    emit("saved", {
      pair: { ...updatedPair, aussagen: createdStatementIds },
      statements: createdStatementIds.map(id => ({ id }))
    });

    setTimeout(close, 900);

  } catch (err) {
    // Rollback: Paar löschen, wenn es existiert
    try {
      if (pairId) {
        await fetch(`${API_BASE}/aussagenpaare/${pairId}`, { method: "DELETE" });
      }
    } catch {}

    feedback.type = "error";
    // err.message kann bereits der JSON-Detail-Text (422) sein → direkt anzeigen
    feedback.message = err?.message || "Unbekannter Fehler beim Speichern.";
    console.error("Speichern fehlgeschlagen:", err);

  } finally {
    saving.value = false;
  }
}
</script>