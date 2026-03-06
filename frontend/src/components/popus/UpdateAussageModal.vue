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
              : feedback.type === 'warn'
                ? 'bg-amber-50 text-amber-800 border border-amber-300'
                : 'bg-red-50 text-red-700 border border-red-300'
          ]"
        >
          {{ feedback.message }}
        </div>
      </div>

      <!-- Hinweis, falls pairId fehlt (nur Hinweis; kein Blocker) -->
      <div
        v-if="!effectivePairId"
        class="mb-4 rounded-xl border border-amber-300 bg-amber-50 px-4 py-3 text-amber-800 text-sm"
      >
        Es ist keine <strong>pairId</strong> gesetzt. Aussagen werden gespeichert,
        das <strong>Paar</strong> wird jedoch <u>nicht</u> aktualisiert.
      </div>

      <!-- Aussagen -->
      <div v-for="(item, index) in localStatements" :key="index" class="mb-4">
        <div class="mb-2 flex items-center justify-between font-semibold">
          <span>
            Aussage {{ index + 1 }}
            <span v-if="!item.id" class="ml-2 text-xs text-amber-600">(ohne ID – wird neu angelegt)</span>
          </span>
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

      <!-- Grafik Upload (Drop/Click) -->
      <div class="mb-2">
        <label class="font-semibold">Grafik</label>

        <label
          class="mt-2 flex flex-col items-center justify-center w-full h-32
                 border-2 border-dashed border-[#538fc6] rounded-xl cursor-pointer
                 hover:border-blue-400 hover:bg-blue-50/30 transition group"
        >
          <div class="flex flex-col items-center gap-2 pointer-events-none px-4">
            <!-- Upload Icon -->
            <svg
              class="w-10 h-10 text-[#538fc6] group-hover:text-blue-500 transition"
              fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round"
                d="M12 16V4m0 0l-4 4m4-4l4 4M6 20h12a2 2 0 002-2v-4a2 2 0 00-2-2H6a2 2 0 00-2 2v4a2 2 0 002 2z" />
            </svg>

            <span class="text-sm text-gray-600 group-hover:text-blue-600 transition text-center">
              Klicke zum Auswählen oder Datei hierher ziehen
            </span>

            <!-- Dateiname/URL -->
            <span v-if="grafik_url" class="text-xs text-gray-500 truncate max-w-[280px]">
              {{ shortUrl(grafik_url) }}
            </span>
          </div>

          <!-- Hidden Input -->
          <input type="file" accept="image/*" class="hidden" @change="uploadGraphic" />
        </label>

        <!-- Vorschau -->
        <div v-if="grafik_url" class="mt-3">
          grafik_url
        </div>

        <!-- Grafik löschen -->
        <div v-if="grafik_url" class="mt-2">
          <button @click="removeGraphic" class="text-xs text-red-600 hover:underline">Grafik entfernen</button>
        </div>
      </div>

      <!-- Aktionen -->
      <div class="flex justify-between mt-6">
        <button class="rounded-lg bg-[#dd4d4d] px-6 py-2 text-white" @click="close" :disabled="saving">
          Abbrechen
        </button>

        <!-- WICHTIG: nicht mehr disabled, wenn pairId fehlt -->
        <button
          class="rounded-lg bg-[#538fc6] px-6 py-2 text-white inline-flex items-center gap-2 disabled:opacity-60"
          @click="save"
          :disabled="saving || hasEmptyTexts"
          title="Speichert Aussagen (und das Paar, falls pairId vorhanden ist)."
        >
          <svg v-if="saving" class="h-4 w-4 animate-spin" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="white" stroke-width="4" fill="none"/>
            <path class="opacity-75" fill="white" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"/>
          </svg>
          <span>{{ saving ? 'Aktualisiere…' : 'Aktualisieren' }}</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted, watch, computed } from "vue";

const props = defineProps({
  modelValue: { type: Boolean, default: false },
  /** Erwartet: [{ id: '...', text: '...', correct: true/false }, ...] */
  statements: { type: Array, default: () => [] },
  /** ID des zu aktualisierenden Aussagenpaars */
  pairId: { type: String, default: "" },
  /** Optional: Metadaten (kategorie[], grafik_url, kommentar, bearbeiter) */
  pair: { type: Object, default: null },
});

const emit = defineEmits(["update:modelValue", "saved"]);

// In prod ggf. aus .env
const API_BASE = "http://127.0.0.1:8000";

/* ------------------------------ Lokale States ------------------------------ */
const localStatements = reactive([]); // [{id, text, correct}]
const kommentar = ref("");
const kategorie = ref("");
const grafik_url = ref("");
const kategorien = ref([]);

const saving = ref(false);
const feedback = reactive({ type: "", message: "" });

/* ------------------------------ Computed / Hilfen ------------------------------ */
const effectivePairId = computed(() => props.pairId || props.pair?.id || "");

// Nur noch Blocker: leere Texte
const hasEmptyTexts = computed(() => localStatements.some(s => !s.text || !s.text.trim()));

// Kürzere Anzeige
function shortUrl(u) {
  if (!u) return "";
  if (u.startsWith("data:")) return "eingebettete Bilddaten";
  if (u.length <= 48) return u;
  return u.slice(0, 22) + "…" + u.slice(-22);
}

/* ------------------------------ HTTP Helper ------------------------------ */
async function patchJson(url, body) {
  const res = await fetch(url, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body)
  });
  let data = null;
  try { data = await res.json(); } catch {}
  if (!res.ok) {
    const t = data?.detail || data?.message || `Fehler (HTTP ${res.status})`;
    throw new Error(typeof t === "string" ? t : JSON.stringify(t));
  }
  return data;
}

async function postJson(url, body) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body)
  });
  let data = null;
  try { data = await res.json(); } catch {}
  if (!res.ok) {
    const t = data?.detail || data?.message || `Fehler (HTTP ${res.status})`;
    throw new Error(typeof t === "string" ? t : JSON.stringify(t));
  }
  return data;
}

/* ------------------------------ Kategorien laden ------------------------------ */
onMounted(async () => {
  try {
    const res = await fetch(`${API_BASE}/kategorien`);
    const parsed = await res.json();
    kategorien.value = Array.isArray(parsed) ? parsed : [];
  } catch (err) {
    console.error("Fehler beim Laden der Kategorien:", err);
    kategorien.value = [];
  }
});

/* ------------------------------ Props → lokale States sync ------------------------------ */
function syncFromProps() {
  // Aussagen übernehmen (inkl. evtl. leerer IDs → werden erstellt)
  localStatements.splice(
    0,
    localStatements.length,
    ...props.statements.map(s => ({
      id: s.id ?? "",
      text: s.text ?? "",
      correct: !!s.correct
    }))
  );

  // Paar-Metadaten (falls bereitgestellt)
  if (props.pair) {
    kommentar.value = props.pair.kommentar ?? kommentar.value;
    // Kategorie: falls nicht gewählt, nimm erste aus Pair
    if (!kategorie.value && Array.isArray(props.pair.kategorie) && props.pair.kategorie.length) {
      kategorie.value = props.pair.kategorie[0];
    }
    // Grafik: echte URL übernehmen (keine blob:)
    if (props.pair.grafik_url && !props.pair.grafik_url.startsWith("blob:")) {
      grafik_url.value = props.pair.grafik_url;
    }
  }
}

watch(() => props.modelValue, (open) => {
  if (open) {
    feedback.type = "";
    feedback.message = "";
    syncFromProps();
  }
}, { immediate: true });

watch(() => props.statements, () => {
  if (props.modelValue) syncFromProps();
});

watch(() => props.pair, () => {
  if (props.modelValue) syncFromProps();
});

/* ------------------------------ Grafik Upload ------------------------------ */
function fileToDataUrl(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onerror = () => reject(new Error("Datei konnte nicht gelesen werden."));
    reader.onload = () => resolve(reader.result);
    reader.readAsDataURL(file);
  });
}

async function uploadGraphic(evt) {
  const file = evt.target.files?.[0];
  if (!file) return;

  // Für Vorschau – optional: direkt DataURL (besser für spätere Persistenz als blob:)
  try {
    const dataUrl = await fileToDataUrl(file);
    grafik_url.value = dataUrl;
  } catch {
    // Fallback: ObjectURL (nur Preview)
    const objectUrl = URL.createObjectURL(file);
    grafik_url.value = objectUrl;
  }
}

function removeGraphic() {
  grafik_url.value = "";
}

/* ------------------------------ API: Aussagen Upsert ------------------------------ */
/**
 * Erstellt eine Aussage (POST /aussagen).
 * Erwartet vom Backend eine Antwort mit { id, aussage, loesung, ... }.
 */
async function createStatement(statement) {
  const payload = {
    aussage: statement.text,
    loesung: !!statement.correct,
    erstellungsdatum: new Date().toISOString()
  };
  return await postJson(`${API_BASE}/aussagen`, payload);
}

/**
 * Aktualisiert eine Aussage (PATCH /aussagen/{aussage_id})
 */
async function patchStatement(statement) {
  const payload = {
    aussage: statement.text,
    loesung: !!statement.correct,
    aenderungsdatum: new Date().toISOString()
  };
  return await patchJson(`${API_BASE}/aussagen/${statement.id}`, payload);
}

/**
 * Upsert: wenn id vorhanden → PATCH, sonst → POST
 * Gibt stets die finale ID zurück.
 */
async function upsertStatement(s) {
  if (s.id) {
    const res = await patchStatement(s);
    return res?.id || s.id;
  } else {
    const res = await createStatement(s);
    return res?.id;
  }
}

/* ------------------------------ API: Paar PATCH ------------------------------ */
async function patchPair(pairId, statementsIds) {
  const payload = {
    id: pairId,
    aussagen: statementsIds,
    kategorie: kategorie.value ? [kategorie.value] : (props.pair?.kategorie ?? []),
    bearbeiter: (props.pair?.bearbeiter ?? "Mostafa"),
    grafik_url: grafik_url.value ?? props.pair?.grafik_url ?? "",
    kommentar: kommentar.value ?? props.pair?.kommentar ?? ""
  };
  return await patchJson(`${API_BASE}/aussagenpaare/${pairId}`, payload);
}

/* ------------------------------ SPEICHERN ------------------------------ */
async function save() {
  feedback.message = "";
  feedback.type = "";

  // Nur blocken, wenn Texte leer sind
  if (hasEmptyTexts.value) {
    feedback.type = "error";
    feedback.message = "Bitte alle Aussagen ausfüllen.";
    return;
  }

  saving.value = true;

  try {
    // 1) Alle Aussagen upserten (ohne ID → POST, mit ID → PATCH)
    const finalIds = [];
    for (const s of localStatements) {
      const id = await upsertStatement(s);
      if (!id) {
        throw new Error("Backend lieferte keine ID für eine Aussage zurück.");
      }
      s.id = id; // local state aktualisieren (neu erstellte IDs setzen)
      finalIds.push(id);
    }

    // 2) Paar patchen, falls pairId vorhanden
    let updatedPair = null;
    if (effectivePairId.value) {
      updatedPair = await patchPair(effectivePairId.value, finalIds);

      feedback.type = "success";
      feedback.message = "Aussagen und Paar erfolgreich aktualisiert.";
    } else {
      // Kein Paar-Update möglich → trotzdem Erfolg für Aussagen
      feedback.type = "warn";
      feedback.message = "Aussagen gespeichert. Paar nicht aktualisiert (keine pairId).";
    }

    // Emit nach außen (neue IDs sind gesetzt)
    emit("saved", {
      pair: updatedPair,
      statements: localStatements.map(s => ({ id: s.id, text: s.text, correct: s.correct }))
    });

    // Bei Erfolg Modal schließen (kurz warten, damit Nutzer Feedback sieht)
    setTimeout(close, 900);
  } catch (err) {
    feedback.type = "error";
    feedback.message = err?.message || "Unbekannter Fehler beim Speichern.";
    console.error("Speichern fehlgeschlagen:", err);
  } finally {
    saving.value = false;
  }
}

/* ------------------------------ Schließen ------------------------------ */
const close = () => emit("update:modelValue", false);
</script>