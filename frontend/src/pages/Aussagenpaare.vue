<template>
  <div class="flex flex-col gap-10 text-grey-text m-15">

    <!-- Filterbereich -->
    <div class="flex flex-row justify-between">

      <div class="flex margin-bottom-20 gap-5">
        <!-- Kategorie -->
        <select v-model="selectedKategorie" class="min-w-52 border rounded-xl">
          <option value="">Alle Kategorien</option>
          <option v-for="option in getOptionsBy('kategorie')" :key="option" :value="option">
            {{ option }}
          </option>
        </select>

        <!-- Bearbeiter -->
        <select v-model="selectedBearbeiter" class="min-w-52 border rounded-xl">
          <option value="">Alle Bearbeiter</option>
          <option v-for="u in users" :key="u.id" :value="u.email">{{ u.email }}</option>
        </select>
      </div>

      <!-- Buttons rechts -->
      <div v-if="selectedRows.length === 0" class="flex gap-5">
        <button class="border px-4 py-2 rounded">Importieren</button>

        <!-- HINZUFÜGEN BUTTON – FIXED -->
        <button
          class="bg-main-blue text-white px-4 py-2 rounded"
          @click="openCreateModal"
        >
          Aussagenpaar hinzufügen
        </button>
      </div>

      <div v-else class="flex gap-5">
        <button class="bg-main-blue text-white px-4 py-2 rounded">Übung erstellen</button>
        <button class="bg-accent-red text-white px-4 py-2 rounded">Löschen</button>
      </div>
    </div>

    <!-- Tabelle -->
    <Table :columns="columns" :rows="filteredRows" v-model:selectedRows="selectedRows">
      <template #actions="{ row }">
        <button @click="editRow(row)">✏️</button>
        <button @click="deleteRow(row)">🗑️</button>
      </template>
    </Table>

    <!-- CREATE MODAL -->
    <StatementModal
      v-model="showStatementModal"
      :statements="statements"
      @saved="afterCreate"
    />

    <!-- UPDATE MODAL -->
    <UpdateAussageModal
      v-if="currentRow"
      v-model="modalOpen"
      :pairId="currentRow.id"
      :pair="currentRow"
      :statements="currentRow.aussagen.map(a => ({
        id: a.id,
        text: a.aussage,
        correct: a.loesung
      }))"
      @saved="afterUpdate"
    />
  </div>
</template>

<script setup>
/* =============================================
   IMPORTS & GLOBALS
============================================= */
import { computed, onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";

import Table from "../components/Table.vue";
import StatementModal from "../components/popus/StatementModal.vue";
 import UpdateAussageModal from "../components/popus/UpdateAussageModal.vue";

const API_BASE = "http://127.0.0.1:8000";
const route = useRoute();

/* =============================================
   STATES
============================================= */
const modalOpen = ref(false);       // EDIT modal
const currentRow = ref(null);       // SELECTED pair for update

const showStatementModal = ref(false);  // CREATE modal
const statements = ref([{ correct: false }, { correct: false }]);

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
  { displayName: "Grafik", key: "grafik_url" },
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

//   for (const pair of pairs) {
//     const ids = pair.aussagen.map(a => (typeof a === "string" ? a : a.id));
//     const loaded = await Promise.all(ids.map(loadAussage));
//     pair._aussagenTexte = loaded.map(a => a?.aussage || "");
//   }
for (const pair of pairs) {

  const ids = (pair.aussagen || [])
    .filter(a => a != null)            // <-- verhindert null
    .map(a => (typeof a === "string" ? a : a.id))
    .filter(id => id != null);         // <-- verhindert undefined / null IDs

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
   TABLE MAPPED ROWS
============================================= */
const allRows = computed(() =>
  allRowsRaw.value.map(item => ({
    id: item.id,
    kategorie: item.kategorie.map(k => catMap.value[k]).join(", "),
    aussage_eins: item._aussagenTexte?.[0] ?? "",
    aussage_zwei: item._aussagenTexte?.[1] ?? "",
    kommentar: item.kommentar ?? "",
    grafik_url: item.grafik_url ?? "",
    bearbeiter: item.bearbeiter ?? "",
  }))
);

/* =============================================
   FILTERS
============================================= */
const filteredRows = computed(() =>
  allRows.value.filter(row => {
    const cats = row.kategorie.split(",").map(x => x.trim());
    const matchCat = !selectedKategorie.value || cats.includes(selectedKategorie.value);
    const matchBearbeiter = !selectedBearbeiter.value || row.bearbeiter === selectedBearbeiter.value;
    return matchCat && matchBearbeiter;
  })
);

/* =============================================
   CREATE MODE
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
   EDIT MODE
============================================= */
async function editRow(row) {
  modalOpen.value = true;

  const raw = allRowsRaw.value.find(p => p.id === row.id);
  if (!raw) return;

  currentRow.value = raw;

  const ids = raw.aussagen.map(a => (typeof a === "string" ? a : a.id));
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
   DELETE
============================================= */
async function deleteRow(row) {
  if (!confirm("Willst du dieses Aussagenpaar wirklich löschen?")) return;

  const raw = allRowsRaw.value.find(p => p.id === row.id);
  const ids = raw.aussagen.map(a => (typeof a === "string" ? a : a.id));

  await fetch(`${API_BASE}/aussagenpaare/${row.id}`, { method: "DELETE" });

  for (const id of ids) {
    await fetch(`${API_BASE}/aussagen/${id}`, { method: "DELETE" });
  }

  await loadPairs();
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
   OPTIONS HELPERS
============================================= */
function getOptionsBy(field) {
  const s = new Set();
  for (const row of allRows.value) {
    if (field === "kategorie") {
      row.kategorie.split(",").forEach(x => s.add(x.trim()));
    }
  }
  return [...s];
}
</script>