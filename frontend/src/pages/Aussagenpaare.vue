<template>
  <div class="flex flex-col gap-10 text-grey-text m-15">

    <!-- FILTER -->
    <div class="flex flex-row justify-between">
      <div class="flex margin-bottom-20 gap-5">
        <!-- Kategorie -->
        <select v-model="selectedKategorie" class="min-w-52 border rounded-xl">
          <option value="">Alle Kategorien</option>
          <option
            v-for="option in getOptionsBy('kategorie')"
            :key="option"
            :value="option"
          >
            {{ option }}
          </option>
        </select>

        <!-- Bearbeiter -->
        <select v-model="selectedBearbeiter" class="min-w-52 border rounded-xl">
          <option value="">Alle Bearbeiter</option>
          <option v-for="u in users" :key="u.id" :value="u.email">
            {{ u.email }}
          </option>
        </select>
      </div>

      <!-- RIGHT BUTTONS -->
      <div v-if="selectedRows.length === 0" class="flex gap-5">
        <button class="border px-4 py-2 rounded">
          Importieren
        </button>

        <button
          class="bg-main-blue text-white px-4 py-2 rounded"
          @click="openCreateModal"
        >
          Aussagenpaar hinzufügen
        </button>
      </div>

      <div v-else class="flex gap-5">
        <button class="bg-main-blue text-white px-4 py-2 rounded">
          Übung erstellen
        </button>

        <button class="bg-accent-red text-white px-4 py-2 rounded" @click="bulkDelete">
          Löschen
        </button>
      </div>
    </div>

    <!-- TABLE -->
    <Table
      :columns="columns"
      :rows="filteredRows"
      v-model:selectedRows="selectedRows"
    >
      <!-- Bildzelle: rendert Thumbnail + Hover-Preview -->
      <template #grafik_url="{ row }">
        <div class="relative inline-block group">
          <img
            v-if="row.grafik_url"
            :src="row.grafik_url"
            alt="Grafik"
            class="w-[50px] h-[50px] object-cover rounded cursor-zoom-in"
            loading="lazy"
          />
          <img
            v-if="row.grafik_url"
            :src="row.grafik_url"
            alt="Grafik Preview"
            class="absolute right-[60px] top-0 bg-white border border-gray-200 p-1 rounded shadow-lg z-50 w-[200px] h-auto opacity-0 group-hover:opacity-100 transition-opacity"
          />
        </div>
      </template>

      <!-- ACTIONS -->
      <template #actions="{ row }">
        <button @click="editRow(row)">✏️</button>
        <button @click="deleteRow(row)">🗑️</button>
      </template>
    </Table>

    <!-- CREATE -->
    <StatementModal
      v-model="showStatementModal"
      :statements="statements"
      @saved="afterCreate"
    />

    <!-- UPDATE -->
    <UpdateAussageModal
      v-if="currentRow"
      v-model="modalOpen"
      :pairId="currentRow.id"
      :pair="currentRow"
      :statements="statements"
      @saved="afterUpdate"
    />
  </div>
</template>

<script setup>
/* =============================================
IMPORTS
============================================= */
import { computed, onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";

import Table from "../components/Table.vue";
import StatementModal from "../components/popus/StatementModal.vue";
import UpdateAussageModal from "../components/popus/UpdateAussageModal.vue";

const API_BASE = "http://127.0.0.1:8000";
const route = useRoute();

/* =============================================
STATE
============================================= */
const modalOpen = ref(false);
const currentRow = ref(null);

const showStatementModal = ref(false);

const statements = ref([
  { text: "", correct: false },
  { text: "", correct: false }
]);

const allRowsRaw = ref([]);
const kategorien = ref([]);
const users = ref([]);

const selectedRows = ref([]);
const selectedKategorie = ref("");
const selectedBearbeiter = ref("");

/* =============================================
TABLE COLUMNS
============================================= */
const columns = [
  { displayName: "Kategorie", key: "kategorie" },
  { displayName: "Aussage 1", key: "aussage_eins" },
  { displayName: "Aussage 2", key: "aussage_zwei" },
  { displayName: "Kommentar", key: "kommentar" },
  { displayName: "Grafik", key: "grafik_url" }, // wird per Slot gerendert
  { displayName: "", key: "actions" },
];

/* =============================================
CATEGORY MAP
============================================= */
const catMap = computed(() =>
  Object.fromEntries((kategorien.value || []).map(k => [k.id, k.name]))
);

/* =============================================
LOADERS
============================================= */
async function loadAussage(id) {
  const res = await fetch(`${API_BASE}/aussagen/${id}`);
  if (!res.ok) return null;
  return res.json();
}

async function loadPairs() {
  const res = await fetch(`${API_BASE}/aussagenpaare`);
  const pairs = await res.json();

  for (const pair of pairs) {
    const ids = (pair.aussagen || [])
      .filter(a => a != null)
      .map(a => (typeof a === "string" ? a : a.id));

    const loaded = await Promise.all(ids.map(loadAussage));
    pair._aussagenTexte = loaded.map(a => a?.aussage || "");
  }

  allRowsRaw.value = pairs;
}

async function loadUsers() {
  const res = await fetch(`${API_BASE}/users`);
  if (res.ok) users.value = await res.json();
}

async function loadCategories() {
  const res = await fetch(`${API_BASE}/kategorien`);
  if (res.ok) kategorien.value = await res.json();
}

onMounted(async () => {
  await Promise.all([loadCategories(), loadPairs(), loadUsers()]);
});

/* =============================================
TABLE DATA
============================================= */
const allRows = computed(() =>
  allRowsRaw.value.map(item => ({
    id: item.id,
    raw: item,
    aussagen_ids: item.aussagen,

    kategorie: (item.kategorie || [])
      .map(k => catMap.value[k])
      .filter(Boolean)
      .join(", "),

    aussage_eins: item._aussagenTexte?.[0] ?? "",
    aussage_zwei: item._aussagenTexte?.[1] ?? "",

    kommentar: item.kommentar ?? "",
    // WICHTIG: nur URL, kein HTML-String
    grafik_url: item.grafik_url ?? "",
    bearbeiter: item.bearbeiter ?? ""
  }))
);

/* =============================================
FILTERS
============================================= */
const filteredRows = computed(() =>
  allRows.value.filter(row => {
    const cats = row.kategorie.split(",").map(x => x.trim()).filter(Boolean);

    const matchCat =
      !selectedKategorie.value || cats.includes(selectedKategorie.value);

    const matchBearbeiter =
      !selectedBearbeiter.value || row.bearbeiter === selectedBearbeiter.value;

    return matchCat && matchBearbeiter;
  })
);

/* =============================================
CREATE
============================================= */
function openCreateModal() {
  statements.value = [
    { text: "", correct: false },
    { text: "", correct: false }
  ];
  showStatementModal.value = true;
}

async function afterCreate() {
  await loadPairs();
  showStatementModal.value = false;
}

/* =============================================
EDIT
============================================= */
async function editRow(row) {
  modalOpen.value = true;

  const raw = row.raw;
  currentRow.value = raw;

  const ids = (raw.aussagen || []).map(a => (typeof a === "string" ? a : a.id));

  const texte = await Promise.all(ids.map(loadAussage));

  statements.value = texte.map(a => ({
    id: a.id,
    text: a.aussage,
    correct: a.loesung
  }));
}

async function afterUpdate() {
  modalOpen.value = false;
  currentRow.value = null;
  await loadPairs();
}

/* =============================================
DELETE (einzeln / mehrere)
============================================= */
async function deleteRow(row) {
  if (!confirm("Willst du dieses Aussagenpaar wirklich löschen?")) return;

  const raw = row.raw;
  const ids = (raw.aussagen || []).map(a => (typeof a === "string" ? a : a.id));

  await fetch(`${API_BASE}/aussagenpaare/${raw.id}`, { method: "DELETE" });

  for (const id of ids) {
    await fetch(`${API_BASE}/aussagen/${id}`, { method: "DELETE" });
  }

  await loadPairs();
}

async function bulkDelete() {
  if (selectedRows.value.length === 0) return;
  if (!confirm(`Willst du ${selectedRows.value.length} Aussagenpaar(e) löschen?`)) return;

  for (const row of selectedRows.value) {
    await deleteRow(row);
  }
  selectedRows.value = [];
}

/* =============================================
URL FILTER
============================================= */
watch(
  () => route.query.kategorie,
  v => (selectedKategorie.value = v || ""),
  { immediate: true }
);

/* =============================================
OPTIONS
============================================= */
function getOptionsBy(field) {
  const s = new Set();
  for (const row of allRows.value) {
    if (field === "kategorie") {
      row.kategorie.split(",").forEach(x => {
        const v = x.trim();
        if (v) s.add(v);
      });
    }
  }
  return [...s];
}
</script>