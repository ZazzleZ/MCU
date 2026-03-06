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

      <!-- Hinweis, falls pairId fehlt (jetzt Blocker) -->
      <div
        v-if="!effectivePairId"
        class="mb-4 rounded-xl border border-amber-300 bg-amber-50 px-4 py-3 text-amber-800 text-sm"
      >
        Es ist keine <strong>pairId</strong> gesetzt. Speichern ist nicht möglich,
        da das Backend <code>aussagenpaar_id</code> verlangt.
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
          {{ grafik_url }}
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

        <!-- Speichern nur möglich, wenn pairId vorhanden ist -->
        <button
          class="rounded-lg bg-[#538fc6] px-6 py-2 text-white inline-flex items-center gap-2 disabled:opacity-60"
          @click="save"
          :disabled="saving || hasEmptyTexts || !effectivePairId"
          title="Speichert Aussagen (Paar-Zuordnung erforderlich)."
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
const effectivePairId = computed(() => (props.pairId || props.pair?.id || "").toString().trim());

// Blocker: leere Texte
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
      id: (s.id ?? "").toString().trim(),
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
async function uploadGraphic(evt) {
  const file = evt.target.files?.[0];
  if (!file) return;

  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch(`${API_BASE}/upload`, {
      method: "POST",
      body: formData
    });

    const data = await res.json();

    if (!data?.path) {
      throw new Error("Upload-Antwort unvollständig (path fehlt).");
    }

    // URL zum gespeicherten File
    grafik_url.value = `${API_BASE}/${data.path}`;
  } catch (err) {
    console.error("Upload Fehler:", err);
    feedback.type = "error";
    feedback.message = "Upload fehlgeschlagen: " + (err?.message || "Unbekannter Fehler");
  }
}

function removeGraphic() {
  grafik_url.value = "";
}

/* ------------------------------ API: Aussagen Upsert ------------------------------ */
function ensurePairIdOrThrow() {
  const pid = effectivePairId.value;
  if (!pid) {
    throw new Error("pairId fehlt (aussagenpaar_id ist erforderlich).");
  }
  return pid;
}

/**
 * Erstellt eine Aussage (POST /aussagen).
 */
async function createStatement(statement) {
  const pairId = ensurePairIdOrThrow();
  const payload = {
    aussage: statement.text,
    loesung: !!statement.correct,
    erstellungsdatum: new Date().toISOString(),
    // Backend verlangt: aussagenpaar_id MUSS im Body sein (nicht undefined lassen!)
    aussagenpaar_id: pairId
  };
  // Debug (optional):
  // console.debug("POST /aussagen payload", payload);
  return await postJson(`${API_BASE}/aussagen`, payload);
}

/**
 * Aktualisiert eine Aussage (PATCH /aussagen/{aussage_id})
 */
async function patchStatement(statement) {
  const pairId = ensurePairIdOrThrow();
  const sid = (statement.id ?? "").toString().trim();
  if (!sid) {
    // Harte Validierung, damit Backend nicht erneut 422 wirft
    throw new Error("Aussage-ID fehlt für PATCH (id ist im Body erforderlich).");
  }
  const payload = {
    aussage: statement.text,
    loesung: !!statement.correct,
    aenderungsdatum: new Date().toISOString(),
    // Backend verlangt id im Body (zusätzlich zur URL)
    id: sid,
    // Backend verlangt Paarbezug (muss als String vorhanden sein)
    aussagenpaar_id: pairId
  };
  // console.debug("PATCH /aussagen payload", payload);
  return await patchJson(`${API_BASE}/aussagen/${sid}`, payload);
}

/**
 * Upsert: wenn id vorhanden → PATCH, sonst → POST
 * Gibt stets die finale ID zurück.
 */
async function upsertStatement(s) {
  const hasId = !!(s.id && s.id.toString().trim().length > 0);
  if (hasId) {
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

  // Blocker: leere Texte
  if (hasEmptyTexts.value) {
    feedback.type = "error";
    feedback.message = "Bitte alle Aussagen ausfüllen.";
    return;
  }

  // Blocker: fehlende pairId (Backend verlangt aussagenpaar_id)
  if (!effectivePairId.value) {
    feedback.type = "error";
    feedback.message = "Speichern nicht möglich: Es ist keine pairId gesetzt (aussagenpaar_id ist erforderlich).";
    return;
  }

  saving.value = true;

  try {
    // 1) Alle Aussagen upserten (ohne ID → POST, mit ID → PATCH)
    const finalIds = [];
    for (const s of localStatements) {
      const id = await upsertStatement(s);
      if (!id) throw new Error("Backend lieferte keine ID für eine Aussage zurück.");
      s.id = id; // local state aktualisieren (neu erstellte IDs setzen)
      finalIds.push(id);
    }

    // 2) Paar patchen
    const updatedPair = await patchPair(effectivePairId.value, finalIds);

    feedback.type = "success";
    feedback.message = "Aussagen und Paar erfolgreich aktualisiert.";

    // Emit nach außen (neue IDs sind gesetzt)
    emit("saved", {
      pair: updatedPair,
      statements: localStatements.map(s => ({ id: s.id, text: s.text, correct: s.correct }))
    });

    // Bei Erfolg Modal schließen (kurz warten, damit Nutzer Feedback sieht)
    setTimeout(close, 900);
  } catch (err) {
    const msg = String(err?.message || "");
    feedback.type = "error";
    if (msg.includes("aussagenpaar_id")) {
      feedback.message = "Fehler: pairId fehlt (aussagenpaar_id ist erforderlich).";
    } else if (msg.includes('"id"') || msg.toLowerCase().includes("aussage-id fehlt")) {
      feedback.message = "Fehler: Backend verlangt 'id' im PATCH-Body.";
    } else {
      feedback.message = "Speichern fehlgeschlagen. Details: " + msg;
    }
    console.error("Speichern fehlgeschlagen:", err);
  } finally {
    saving.value = false;
  }
}

/* ------------------------------ Schließen ------------------------------ */
const close = () => emit("update:modelValue", false);
</script>