<script setup>
import { computed, ref } from "vue";
import Table from "../components/Table.vue";

const columns = [{ displayName: "Kategorie", key: "kategorie" }, { displayName: "Aussage 1", key: "aussage_eins" }, { displayName: "Aussage 2", key: "aussage_zwei" }, { displayName: "Kommentar", key: "kommentar" }, { displayName: "Grafik", key: "grafik_url" }, { displayName: "", key: "actions" }];

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

const editRow = (row) => {
  console.log("Edit row:", row);
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
    <div class="flex flex-col gap-10 text-grey-text m-15">
        <div class="flex flex-row justify-between">
            <div class="flex margin-bottom-20 gap-5">
                <div class="relative">
                    <select
                        name="kategorie"
                        id="kategorie-select"
                        v-model="selectedKategorie"
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
                        name="bearbeiter"
                        id="bearbeiter-select"
                        v-model="selectedBearbeiter"
                        class="min-w-52 appearance-none rounded-xl border border-slate-300 bg-white pl-4 pr-11 py-2.5 text-sm font-medium outline-none transition focus:border-blue-500 shadow-sm"
                    >
                        <option value="" class="bg-white">Alle Bearbeiter</option>
                        <option v-for="option in getOptionsBy('bearbeiter')" :key="option" :value="option">{{ option }}</option>
                    </select>
                    <span class="pointer-events-none absolute inset-y-0 right-3 flex items-center">
                        <svg class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                            <path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 0 1 1.06.02L10 11.12l3.71-3.9a.75.75 0 1 1 1.08 1.04l-4.25 4.46a.75.75 0 0 1-1.08 0L5.21 8.27a.75.75 0 0 1 .02-1.06Z" clip-rule="evenodd" />
                        </svg>
                    </span>
                </div>
            </div>
            <div v-if="selectedRows.length == 0" class="flex justify-end gap-5">
                <button class="min-w-22 cursor-pointer rounded-lg border border-main-blue bg-white px-4 py-2 font-semibold text-main-blue transition hover:bg-main-blue hover:text-white">
                    Importieren
                </button>
                <button  class="min-w-22 cursor-pointer rounded-lg border border-main-blue bg-main-blue px-4 py-2 font-semibold text-white transition hover:brightness-95">
                    Aussagenpaar hinzufügen
                </button>
            </div>
            <div v-else class="flex justify-end gap-5">
                <button  class="min-w-22 cursor-pointer rounded-lg border border-main-blue bg-main-blue px-4 py-2 font-semibold text-white transition hover:brightness-95">
                    Übung erstellen
                </button>
                <button  class="min-w-22 cursor-pointer rounded-lg border border-accent-red bg-accent-red px-4 py-2 font-semibold text-white transition hover:bg-hover-red">
                    Löschen
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
        </Table>
    </div>
</template>
