<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";
import Table from "../components/Table.vue";
import StatementModal from "../components/popus/StatementModal.vue";

const API_BASE = "http://localhost:8000";
const route = useRoute();

/* =========================
   Tabellen-Definition
========================= */
const columns = [
  { displayName: "Kategorie", key: "kategorie" },
  { displayName: "Aussage 1", key: "aussage_eins" },
  { displayName: "Aussage 2", key: "aussage_zwei" },
  { displayName: "Kommentar", key: "kommentar" },
  { displayName: "Grafik", key: "grafik_url" },
  { displayName: "", key: "actions" },
];

/* =========================
   Daten-States
========================= */
const allRowsRaw = ref([]);          // Rohdaten aus /aussagenpaare (mit IDs)
const kategorien = ref([]);          // {id, name} aus /kategorien

// Map: Kategorie-ID → Name
const catMap = computed(() =>
  Object.fromEntries((kategorien.value || []).map(k => [k.id, k.name]))
);

// Denormalisierte/anzeigefertige Rows
const allRows = computed(() => {
  return (allRowsRaw.value || []).map(item => {
    const aussagen = Array.isArray(item.aussagen) ? item.aussagen : [];
    const katIds = Array.isArray(item.kategorie) ? item.kategorie : [];

    const katNamen = katIds
      .map(id => catMap.value[id] || `#${id}`) // Fallback: #ID wenn Name nicht vorhanden
      .join(", ");

    return {
      id: item.id,
      // Wichtig: Anzeige-Wert statt ID
      kategorie: katNamen,
      aussage_eins: aussagen[0]?.aussage ?? "",
      aussage_zwei: aussagen[1]?.aussage ?? "",
      bearbeiter: item.bearbeiter ?? "",
      grafik_url: item.grafik_url ?? "",
      kommentar: item.kommentar ?? "",
      // Optional: Originalwerte behalten (falls später benötigt)
      _raw: item
    };
  });
});

/* =========================
   Selektionen/Filter
========================= */
const selectedRows = ref([]);
const selectedKategorie = ref("");
const selectedBearbeiter = ref("");

const filteredRows = computed(() =>
  allRows.value.filter((row) => {
    const kategorien = String(row.kategorie ?? "")
      .split(",")
      .map((entry) => entry.trim())
      .filter(Boolean);

    const matchesKategorie =
      !selectedKategorie.value || kategorien.includes(selectedKategorie.value);

    const matchesBearbeiter =
      !selectedBearbeiter.value || row.bearbeiter === selectedBearbeiter.value;

    return matchesKategorie && matchesBearbeiter;
  })
);

// Options für Selects dynamisch aus den denormalisierten Rows
function getOptionsBy(field) {
  const options = new Set();
  allRows.value.forEach((row) => {
    if (!row[field]) return;

    if (field === "kategorie") {
      String(row[field])
        .split(",")
        .map((entry) => entry.trim())
        .filter(Boolean)
        .forEach((entry) => options.add(entry));
      return;
    }

    options.add(row[field]);
  });
  return Array.from(options);
}

/* =========================
   Modal-State (Aussagenpaar hinzufügen)
========================= */
const showStatementModal = ref(false);
const statements = ref([
  { correct: false },
  { correct: false }
]);

// Nach Speichern aus dem Modal → Liste neu laden + Modal schließen
const handleSaved = async () => {
  await loadPairs();
  showStatementModal.value = false;
};

// Falls du auf "save" (nicht "saved") hören willst:
const handleSave = (data) => {
  // Optional: Wird vom Modal beim Klick auf "Speichern" ausgelöst
  // Der tatsächliche Persist-Erfolg wird über "saved" signalisiert.
  console.log("Modal save:", data);
};

/* =========================
   CRUD/Aktionen
========================= */
const editRow = (row) => {
  // Hier könntest du dein bestehendes Edit-Modal öffnen
  console.log("Edit row:", row);
};

const deleteRow = async (row) => {
  try {
    const response = await fetch(`${API_BASE}/aussagenpaare/${row.id}`, {
      method: "DELETE",
    });
    if (!response.ok) {
      throw new Error(`Fehler beim Löschen des Aussagenpaars (${response.status})`);
    }
    // Lokal entfernen
    allRowsRaw.value = allRowsRaw.value.filter((item) => item.id !== row.id);
    selectedRows.value = selectedRows.value.filter((item) => item.id !== row.id);
  } catch (error) {
    console.error("Aussagenpaar konnte nicht gelöscht werden:", error);
    alert(error.message || "Aussagenpaar konnte nicht gelöscht werden.");
  }
};

/* =========================
   Daten laden
========================= */
async function loadCategories() {
  const res = await fetch(`${API_BASE}/kategorien`);
  if (!res.ok) throw new Error(`Kategorien HTTP ${res.status}`);
  kategorien.value = await res.json();
}

async function loadPairs() {
  const res = await fetch(`${API_BASE}/aussagenpaare`);
  if (!res.ok) throw new Error(`Aussagenpaare HTTP ${res.status}`);
  const data = await res.json();
  // Roh in State – denormalisierung geschieht in allRows (computed)
  allRowsRaw.value = Array.isArray(data) ? data : [];
}

async function loadAll() {
  try {
    await Promise.all([loadCategories(), loadPairs()]);
  } catch (err) {
    console.error("Fehler beim Laden:", err);
    allRowsRaw.value = [];
  }
}

onMounted(loadAll);

/* =========================
   URL-Filter (Query-Param)
========================= */
watch(
  () => route.query.kategorie,
  (kategorie) => {
    // Achtung: Query enthält evtl. den Name nicht die ID – wir filtern auf Namen.
    selectedKategorie.value = typeof kategorie === "string" ? kategorie : "";
  },
  { immediate: true },
);
</script>

<template>
  <div class="flex flex-col gap-10 text-grey-text m-15">
    <div class="flex flex-row justify-between">
      <!-- Filter -->
      <div class="flex margin-bottom-20 gap-5">
        <div class="relative">
          <select
            name="kategorie"
            id="kategorie-select"
            v-model="selectedKategorie"
            class="min-w-52 cursor-pointer appearance-none rounded-xl border border-slate-300 bg-white pl-4 pr-11 py-2.5 text-sm font-medium outline-none transition focus:border-blue-500 shadow-sm"
          >
            <option value="">Alle Kategorien</option>
            <option v-for="option in getOptionsBy('kategorie')" :key="option" :value="option">
              {{ option }}
            </option>
          </select>
          <span class="pointer-events-none absolute inset-y-0 right-3 flex items-center">
            <svg class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
              <path
                fill-rule="evenodd"
                d="M5.23 7.21a.75.75 0 0 1 1.06.02L10 11.12l3.71-3.9a.75.75 0 1 1 1.08 1.04l-4.25 4.46a.75.75 0 0 1-1.08 0L5.21 8.27a.75.75 0 0 1 .02-1.06Z"
                clip-rule="evenodd"
              />
            </svg>
          </span>
        </div>

        <div class="relative">
          <select
            name="bearbeiter"
            id="bearbeiter-select"
            v-model="selectedBearbeiter"
            class="min-w-52 cursor-pointer appearance-none rounded-xl border border-slate-300 bg-white pl-4 pr-11 py-2.5 text-sm font-medium outline-none transition focus:border-blue-500 shadow-sm"
          >
            <option value="" class="bg-white">Alle Bearbeiter</option>
            <option v-for="option in getOptionsBy('bearbeiter')" :key="option" :value="option">
              {{ option }}
            </option>
          </select>
          <span class="pointer-events-none absolute inset-y-0 right-3 flex items-center">
            <svg class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
              <path
                fill-rule="evenodd"
                d="M5.23 7.21a.75.75 0 0 1 1.06.02L10 11.12l3.71-3.9a.75.75 0 1 1 1.08 1.04l-4.25 4.46a.75.75 0 0 1-1.08 0L5.21 8.27a.75.75 0 0 1 .02-1.06Z"
                clip-rule="evenodd"
              />
            </svg>
          </span>
        </div>
      </div>

      <!-- Buttons rechts -->
      <div v-if="selectedRows.length == 0" class="flex justify-end gap-5">
        <button
          class="min-w-22 cursor-pointer rounded-lg border border-main-blue bg-white px-4 py-2 font-semibold text-main-blue transition hover:bg-main-blue hover:text-white"
        >
          Importieren
        </button>

        <button
          class="rounded-lg cursor-pointer border border-main-blue bg-main-blue px-4 py-2 font-semibold text-white transition hover:brightness-95"
          @click="showStatementModal = true"
        >
          Aussagenpaar hinzufügen
        </button>
      </div>

      <div v-else class="flex justify-end gap-5">
        <button
          class="min-w-22 cursor-pointer rounded-lg border border-main-blue bg-main-blue px-4 py-2 font-semibold text-white transition hover:brightness-95"
        >
          Übung erstellen
        </button>
        <button
          class="min-w-22 cursor-pointer rounded-lg border border-accent-red bg-accent-red px-4 py-2 font-semibold text-white transition hover:bg-hover-red"
        >
          Löschen
        </button>
      </div>
    </div>

    <!-- Tabelle -->
    <Table :columns="columns" :rows="filteredRows" v-model:selectedRows="selectedRows">
      <template #actions="{ row }">
        <div class="flex items-center gap-2">
          <button
            type="button"
            class="inline-flex h-8 w-8 p-0 items-center justify-center rounded-md border border-main-blue text-main-blue transition hover:bg-main-blue hover:text-white cursor-pointer"
            aria-label="Zeile bearbeiten"
            @click="editRow(row)"
          >
            <svg class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <path d="M3 17.25V21h3.75L17 10.75 13.25 7 3 17.25Zm17.75-10.3c.33-.33.33-.87 0-1.2L18.25 3.25a.85.85 0 0 0-1.2 0l-1.8 1.8 3.7 3.7 1.8-1.8Z" />
            </svg>
          </button>
          <button
            type="button"
            class="inline-flex h-8 w-8 p-0 items-center justify-center rounded-md border border-accent-red text-accent-red transition hover:bg-accent-red hover:text-white cursor-pointer"
            aria-label="Zeile löschen"
            @click="deleteRow(row)"
          >
            <svg class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <path d="M9 4h6l1 1h4v2H4V5h4l1-1Zm-2 3h10a1 1 0 0 1 1 1v11a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2V8a1 1 0 0 1 1-1Z" />
            </svg>
          </button>
        </div>
      </template>

      <!-- Optional: Wenn dein <Table> Spalten-Slots unterstützt, schöne Grafik-Anzeige -->
      <!--
      <template #cell-grafik_url="{ row }">
        <div class="flex items-center gap-2">
          <img v-if="row.grafik_url && row.grafik_url.startsWith('blob:')" :src="row.grafik_url" class" class="text-main-blue underline</template>
      -->
    </Table>

    <!-- Modal -->
    <StatementModal
      v-model="showStatementModal"
      :statements="statements"
      @save="handleSave"
      @saved="handleSaved"
      @select-category="() => console.log('Kategorie wählen')"
      @select-graphic="() => console.log('Grafik wählen')"
    />
  </div>
</template>