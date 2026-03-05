<script setup>
import { computed, ref } from "vue";
import { useRoute } from "vue-router";
import Table from "../components/Table.vue";

const route = useRoute();

const columns = [
  { displayName: "Kategorie", key: "kategorie" },
  { displayName: "Aussage 1", key: "aussage_eins" },
  { displayName: "Aussage 2", key: "aussage_zwei" },
  { displayName: "Kommentar", key: "kommentar" },
  { displayName: "Grafik", key: "grafik_url" },
  { displayName: "", key: "actions" },
];

const allRows = ref([
  { id: 1, kategorie: "Der Himmel ist blau.", aussage_eins: "Allgemein", aussage_zwei: "", bearbeiter: "Aktiv", grafik_url: "", kommentar: "" },
  { id: 2, kategorie: "Wasser friert bei 0 C.", aussage_eins: "Wissenschaft", aussage_zwei: "Allgemein", bearbeiter: "Aktiv", grafik_url: "", kommentar: "" },
  { id: 3, kategorie: "Die Erde ist flach.", aussage_eins: "Mythos", aussage_zwei: "Allgemein", bearbeiter: "Inaktiv", grafik_url: "", kommentar: "" },
]);

const selectedRows = ref([]);
const selectedKategorie = ref("");
const selectedBearbeiter = ref("");

const filteredRows = computed(() =>
  allRows.value.filter((row) => {
    const matchesKategorie = !selectedKategorie.value || row.kategorie === selectedKategorie.value;
    const matchesBearbeiter = !selectedBearbeiter.value || row.bearbeiter === selectedBearbeiter.value;
    return matchesKategorie && matchesBearbeiter;
  }),
);

const uebungsname = computed(() => {
  const id = route.params.uebungId;
  if (!id) {
    return "Uebung";
  }
  return `Uebung ${id}`;
});

const addAussagenpaar = () => {
  console.log("Aussagenpaar hinzufuegen");
};

const copyDeeplink = async () => {
  const id = route.params.uebungId;
  const link = `${window.location.origin}/durchfuehren/${id}`;
  try {
    await navigator.clipboard.writeText(link);
  } catch (error) {
    console.error("Copy failed:", error);
  }
};

const deleteSelectedRows = () => {
  const selectedIds = new Set(selectedRows.value.map((row) => row.id));
  allRows.value = allRows.value.filter((item) => !selectedIds.has(item.id));
  selectedRows.value = [];
};

const deleteRow = (row) => {
  allRows.value = allRows.value.filter((item) => item.id !== row.id);
  selectedRows.value = selectedRows.value.filter((item) => item.id !== row.id);
};

function getOptionsBy(field) {
  const options = new Set();
  allRows.value.forEach((row) => {
    if (row[field]) {
      options.add(row[field]);
    }
  });
  return Array.from(options);
}
</script>

<template>
  <div class="m-15 flex flex-col gap-10 text-grey-text">
    <div class="grid grid-cols-3 items-center gap-3">
      <RouterLink
        to="/uebungen"
        class="justify-self-start inline-flex cursor-pointer items-center gap-2 rounded-lg border border-main-blue bg-white px-4 py-2 font-semibold text-main-blue transition hover:bg-main-blue hover:text-white"
      >
        <svg class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
          <path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2Z" />
        </svg>
        Zurück
      </RouterLink>
      <h1 class="justify-self-center text-center text-sm font-semibold tracking-wide text-grey-text sm:text-base">{{ uebungsname }}</h1>
      <div class="justify-self-end flex items-center gap-3">
        <button
          type="button"
          class="inline-flex size-10.5 items-center justify-center text-xl cursor-pointer rounded-xl border border-main-blue bg-main-blue font-semibold text-white transition hover:brightness-95"
          aria-label="Aussagenpaar hinzufuegen"
          title="Aussagenpaar hinzufuegen"
          @click="addAussagenpaar"
        >
          +
        </button>
        <button
          type="button"
          class="inline-flex size-10.5 items-center justify-center rounded-xl border border-main-blue text-main-blue transition hover:bg-main-blue hover:text-white cursor-pointer"
          aria-label="Deeplink kopieren"
          title="Deeplink kopieren"
          @click="copyDeeplink"
        >
          <svg class="h-5 w-5" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
            <path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1Zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2Zm0 16H8V7h11v14Z" />
          </svg>
        </button>
        <button
          v-if="selectedRows.length > 0"
          type="button"
          class="inline-flex h-10.5 items-center justify-center rounded-xl border border-accent-red bg-accent-red px-4 text-sm font-semibold text-white transition hover:bg-hover-red cursor-pointer"
          @click="deleteSelectedRows"
        >
          Ausgewaehlte loeschen
        </button>
      </div>
    </div>

    <div class="flex flex-row justify-between">
      <div class="flex margin-bottom-20 gap-5">
        <div class="relative">
          <select
            id="kategorie-select"
            v-model="selectedKategorie"
            name="kategorie"
            class="min-w-52 appearance-none rounded-xl border border-slate-300 bg-white pl-4 pr-11 py-2.5 text-sm font-medium outline-none transition focus:border-blue-500 shadow-sm"
          >
            <option value="">Alle Kategorien</option>
            <option v-for="option in getOptionsBy('kategorie')" :key="option" :value="option">{{ option }}</option>
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
            name="bearbeiter"
            class="min-w-52 appearance-none rounded-xl border border-slate-300 bg-white pl-4 pr-11 py-2.5 text-sm font-medium outline-none transition focus:border-blue-500 shadow-sm"
          >
            <option value="">Alle Bearbeiter</option>
            <option v-for="option in getOptionsBy('bearbeiter')" :key="option" :value="option">{{ option }}</option>
          </select>
          <span class="pointer-events-none absolute inset-y-0 right-3 flex items-center">
            <svg class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
              <path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 0 1 1.06.02L10 11.12l3.71-3.9a.75.75 0 1 1 1.08 1.04l-4.25 4.46a.75.75 0 0 1-1.08 0L5.21 8.27a.75.75 0 0 1 .02-1.06Z" clip-rule="evenodd" />
            </svg>
          </span>
        </div>
      </div>
    </div>

    <Table
      :columns="columns"
      :rows="filteredRows"
      v-model:selectedRows="selectedRows"
    >
      <template #actions="{ row }">
        <button
          type="button"
          class="inline-flex h-8 w-8 items-center justify-center rounded-md border border-accent-red text-accent-red transition hover:bg-accent-red hover:text-white cursor-pointer"
          aria-label="Aussagenpaar loeschen"
          title="Aussagenpaar loeschen"
          @click="deleteRow(row)"
        >
          <svg class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
            <path d="M9 4h6l1 1h4v2H4V5h4l1-1Zm-2 3h10a1 1 0 0 1 1 1v11a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2V8a1 1 0 0 1 1-1Z" />
          </svg>
        </button>
      </template>
    </Table>
  </div>
</template>

