<script setup>
import { computed, ref } from "vue";
import { useRouter } from "vue-router";
import Table from "../components/Table.vue";

const router = useRouter();

const columns = [
  { displayName: "Name", key: "name" },
  { displayName: "Anz. Aussagenpaare", key: "anzAussagenpaare" },
  { displayName: "Kategorien", key: "kategorien" },
  { displayName: "Bearbeiter", key: "bearbeiter" },
  { displayName: "", key: "actions" },
];

const allRows = ref([
  { id: 1, name: "Uebung 1", anzAussagenpaare: 12, kategorien: "Allgemein, Wissenschaft", bearbeiter: "Max Mustermann" },
  { id: 2, name: "Uebung 2", anzAussagenpaare: 8, kategorien: "Mythen", bearbeiter: "Erika Musterfrau" },
  { id: 3, name: "Uebung 3", anzAussagenpaare: 15, kategorien: "Allgemein", bearbeiter: "Max Mustermann" },
]);

const selectedRows = ref([]);
const searchInput = ref("");
const appliedSearchText = ref("");
const selectedKategorie = ref("");
const selectedBearbeiter = ref("");

const filteredRows = computed(() =>
  allRows.value.filter((row) => {
    const query = appliedSearchText.value.trim().toLowerCase();
    const matchesSearch =
      !query ||
      row.name.toLowerCase().includes(query) ||
      row.kategorien.toLowerCase().includes(query) ||
      row.bearbeiter.toLowerCase().includes(query);
    const matchesKategorie = !selectedKategorie.value || row.kategorien.includes(selectedKategorie.value);
    const matchesBearbeiter = !selectedBearbeiter.value || row.bearbeiter === selectedBearbeiter.value;
    return matchesSearch && matchesKategorie && matchesBearbeiter;
  }),
);

const kategorienOptions = computed(() => {
  const options = new Set();
  allRows.value.forEach((row) => {
    row.kategorien
      .split(",")
      .map((entry) => entry.trim())
      .filter(Boolean)
      .forEach((entry) => options.add(entry));
  });
  return Array.from(options);
});

const bearbeiterOptions = computed(() => {
  const options = new Set();
  allRows.value.forEach((row) => {
    if (row.bearbeiter) {
      options.add(row.bearbeiter);
    }
  });
  return Array.from(options);
});

const addUebung = () => {
  console.log("Uebung hinzufuegen");
};

const applySearch = () => {
  appliedSearchText.value = searchInput.value;
};

const goToUebung = (row) => {
  router.push(`/uebungen/${row.id}`);
};

const copyDurchfuehrenLink = async (row) => {
  const link = `${window.location.origin}/durchfuehren/${row.id}`;
  try {
    await navigator.clipboard.writeText(link);
  } catch (error) {
    console.error("Copy failed:", error);
  }
};

const deleteRow = (row) => {
  allRows.value = allRows.value.filter((item) => item.id !== row.id);
  selectedRows.value = selectedRows.value.filter((item) => item.id !== row.id);
};

const deleteSelectedRows = () => {
  const selectedIds = new Set(selectedRows.value.map((row) => row.id));
  allRows.value = allRows.value.filter((item) => !selectedIds.has(item.id));
  selectedRows.value = [];
};
</script>

<template>
  <div class="m-15 flex flex-col gap-10 text-grey-text">
    <div class="flex flex-row justify-between gap-5">
      <div class="flex margin-bottom-20 gap-5">
        <div class="flex items-center gap-2">
          <input
            v-model="searchInput"
            type="text"
            placeholder="Suchen..."
            class="min-w-64 rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-sm font-medium outline-none transition focus:border-blue-500 shadow-sm"
            @keyup.enter="applySearch"
          />
          <button
            type="button"
            class="inline-flex size-10.5 items-center justify-center rounded-md border border-main-blue text-main-blue transition hover:bg-main-blue hover:text-white cursor-pointer"
            aria-label="Suche ausfuehren"
            title="Suche"
            @click="applySearch"
          >
            <svg class="h-5 w-5" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <path d="M15.5 14h-.79l-.28-.27a6 6 0 1 0-.71.71l.27.28v.79L20 21.5 21.5 20l-6-6ZM10 15a5 5 0 1 1 0-10 5 5 0 0 1 0 10Z" />
            </svg>
          </button>
        </div>
        <div class="relative">
          <select
            id="kategorie-select"
            v-model="selectedKategorie"
            class="min-w-52 cursor-pointer appearance-none rounded-xl border border-slate-300 bg-white pl-4 pr-11 py-2.5 text-sm font-medium outline-none transition focus:border-blue-500 shadow-sm"
          >
            <option value="">Alle Kategorien</option>
            <option v-for="option in kategorienOptions" :key="option" :value="option">{{ option }}</option>
          </select>
          <span class="pointer-events-none absolute inset-y-0 right-3 flex items-center">
            <svg class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
              <path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 0 1 1.06.02L10 11.12l3.71-3.9a.75.75 0 1 1 1.08 1.04l-4.25 4.46a.75.75 0 0 1-1.08 0L5.21 8.27a.75.75 0 0 1 .02-1.06Z" clip-rule="evenodd" />
            </svg>
          </span>
        </div>
        <div class="relative">
          <select
            id="bearbeiter-select"
            v-model="selectedBearbeiter"
            class="min-w-52 cursor-pointer appearance-none rounded-xl border border-slate-300 bg-white pl-4 pr-11 py-2.5 text-sm font-medium outline-none transition focus:border-blue-500 shadow-sm"
          >
            <option value="">Alle Bearbeiter</option>
            <option v-for="option in bearbeiterOptions" :key="option" :value="option">{{ option }}</option>
          </select>
          <span class="pointer-events-none absolute inset-y-0 right-3 flex items-center">
            <svg class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
              <path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 0 1 1.06.02L10 11.12l3.71-3.9a.75.75 0 1 1 1.08 1.04l-4.25 4.46a.75.75 0 0 1-1.08 0L5.21 8.27a.75.75 0 0 1 .02-1.06Z" clip-rule="evenodd" />
            </svg>
          </span>
        </div>
      </div>
      <div class="flex justify-end gap-3">
        <button
          type="button"
          class="inline-flex size-10.5 items-center justify-center text-xl cursor-pointer rounded-xl border border-main-blue bg-main-blue font-semibold text-white transition hover:brightness-95"
          @click="addUebung"
        >
          +
        </button>
        <button
          v-if="selectedRows.length > 0"
          type="button"
          class="inline-flex h-10.5 items-center justify-center rounded-xl border border-accent-red bg-accent-red px-4 text-sm font-semibold text-white transition hover:bg-hover-red cursor-pointer"
          @click="deleteSelectedRows"
        >
          Ausgewählte löschen
        </button>
      </div>
    </div>

    <Table
      :columns="columns"
      :rows="filteredRows"
      v-model:selectedRows="selectedRows"
    >
      <template #actions="{ row }">
        <div class="flex items-center gap-2">
          <button
            type="button"
            class="inline-flex h-8 w-8 items-center justify-center rounded-md border border-main-blue text-main-blue transition hover:bg-main-blue hover:text-white cursor-pointer"
            aria-label="Zur Uebung"
            title="Zur Uebung"
            @click="goToUebung(row)"
          >
            <svg class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <path d="M14 3v2h3.59L7 15.59 8.41 17 19 6.41V10h2V3z" />
              <path d="M5 5h5V3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2v-5h-2v5H5z" />
            </svg>
          </button>
          <button
            type="button"
            class="inline-flex h-8 w-8 items-center justify-center rounded-md border border-slate-400 text-slate-700 transition hover:bg-slate-200 cursor-pointer"
            aria-label="Deep Link kopieren"
            title="Deep Link kopieren"
            @click="copyDurchfuehrenLink(row)"
          >
            <svg class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1Zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2Zm0 16H8V7h11v14Z" />
            </svg>
          </button>
          <button
            type="button"
            class="inline-flex h-8 w-8 items-center justify-center rounded-md border border-accent-red text-accent-red transition hover:bg-accent-red hover:text-white cursor-pointer"
            aria-label="Uebung loeschen"
            title="Uebung loeschen"
            @click="deleteRow(row)"
          >
            <svg class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <path d="M9 4h6l1 1h4v2H4V5h4l1-1Zm-2 3h10a1 1 0 0 1 1 1v11a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2V8a1 1 0 0 1 1-1Z" />
            </svg>
          </button>
        </div>
      </template>
    </Table>
  </div>
</template>


