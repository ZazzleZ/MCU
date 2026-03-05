<script setup>
import { computed, onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import Table from "../components/Table.vue";
import KategorieDeleteConfirmModal from "./Kategorien/KategorieDeleteConfirmModal.vue";

const router = useRouter();

const columns = [
  { displayName: "Kategorie", key: "kategorie" },
  { displayName: "Anz. Aussagenpaare", key: "anzAussagenpaare" },
  { displayName: "", key: "actions" },
];

const allRows = ref([]);

const selectedRows = ref([]);
const searchInput = ref("");
const appliedSearchText = ref("");
const showAddKategorieModal = ref(false);
const showDeleteConfirmModal = ref(false);
const deleteMode = ref("single");
const rowToDelete = ref(null);
const kategorienameInput = ref("");
const createKategorieError = ref("");
const isCreatingKategorie = ref(false);

const filteredRows = computed(() => {
  const query = appliedSearchText.value.trim().toLowerCase();

  return allRows.value.filter((row) => {
    if (!query) {
      return true;
    }

    return row.kategorie.toLowerCase().includes(query);
  });
});

const applySearch = () => {
  appliedSearchText.value = searchInput.value;
};

const mapKategorieToRow = (item) => ({
  id: item.id,
  kategorie: item.name ?? "",
  anzAussagenpaare: Array.isArray(item.aussagenpaare) ? item.aussagenpaare.length : 0,
});

const loadKategorien = async () => {
  try {
    const response = await fetch("http://localhost:8000/kategorien");
    if (!response.ok) {
      throw new Error(`Fehler beim Laden der Kategorien (${response.status})`);
    }
    const data = await response.json();
    allRows.value = Array.isArray(data) ? data.map(mapKategorieToRow) : [];
  } catch (error) {
    console.error("Kategorien konnten nicht geladen werden:", error);
    allRows.value = [];
  }
};

const openAddKategorieModal = () => {
  createKategorieError.value = "";
  kategorienameInput.value = "";
  showAddKategorieModal.value = true;
};

const closeAddKategorieModal = () => {
  showAddKategorieModal.value = false;
  createKategorieError.value = "";
  kategorienameInput.value = "";
};

const createKategorie = async () => {
  const kategoriename = kategorienameInput.value.trim();
  if (!kategoriename) {
    createKategorieError.value = "Bitte einen Kategorienamen eingeben.";
    return;
  }

  isCreatingKategorie.value = true;
  createKategorieError.value = "";

  try {
    const response = await fetch("http://localhost:8000/kategorien", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: kategoriename,
        aussagenpaare: [],
      }),
    });

    if (!response.ok) {
      let message = `Kategorie konnte nicht erstellt werden (${response.status})`;
      try {
        const errorBody = await response.json();
        if (errorBody?.detail) {
          message = typeof errorBody.detail === "string" ? errorBody.detail : message;
        }
      } catch {
        // ignore json parse errors for non-json responses
      }
      throw new Error(message);
    }

    closeAddKategorieModal();
    await loadKategorien();
  } catch (error) {
    createKategorieError.value = error?.message ?? "Unbekannter Fehler beim Erstellen.";
  } finally {
    isCreatingKategorie.value = false;
  }
};

const openDeleteSelectedRowsModal = () => {
  if (selectedRows.value.length === 0) {
    return;
  }
  deleteMode.value = "selected";
  rowToDelete.value = null;
  showDeleteConfirmModal.value = true;
};

const openDeleteRowModal = (row) => {
  deleteMode.value = "single";
  rowToDelete.value = row;
  showDeleteConfirmModal.value = true;
};

const closeDeleteConfirmModal = () => {
  showDeleteConfirmModal.value = false;
  rowToDelete.value = null;
};

const deleteKategorieById = async (id) => {
  const response = await fetch(`http://localhost:8000/kategorien/${id}`, {
    method: "DELETE",
  });

  if (!response.ok) {
    throw new Error(`Kategorie konnte nicht geloescht werden (${response.status})`);
  }
};

const confirmDelete = async () => {
  try {
    if (deleteMode.value === "selected") {
      const ids = selectedRows.value.map((row) => row.id);
      for (const id of ids) {
        await deleteKategorieById(id);
      }
      selectedRows.value = [];
    } else if (rowToDelete.value?.id) {
      await deleteKategorieById(rowToDelete.value.id);
    }

    closeDeleteConfirmModal();
    await loadKategorien();
  } catch (error) {
    console.error("Kategorien konnten nicht geloescht werden:", error);
  }
};

const getDeleteConfirmText = () => {
  if (deleteMode.value === "selected") {
    return "Ausgewaehlte Kategorien loeschen?";
  }

  return "Kategorie ";
};

const getDeleteConfirmDetail = () => {
  if (deleteMode.value === "selected") {
    return "";
  }

  return rowToDelete.value?.kategorie ?? "";
};

const deleteSelectedRows = () => {
  openDeleteSelectedRowsModal();
};

const deleteRow = (row) => {
  openDeleteRowModal(row);
};

const openAussagenpaareByKategorie = (row) => {
  router.push({
    path: "/aussagenpaare",
    query: { kategorie: row.kategorie },
  });
};

onMounted(() => {
  loadKategorien();
});
</script>

<template>
  <div class="m-15 flex flex-col gap-10 text-grey-text">
    <div class="flex flex-row justify-between gap-5">
      <div class="flex margin-bottom-20 gap-2">
        <input
          v-model="searchInput"
          type="text"
          placeholder="Kategorie suchen..."
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

      <div class="flex justify-end gap-3">
        <button
          type="button"
          class="inline-flex size-10.5 items-center justify-center text-xl cursor-pointer rounded-xl border border-main-blue bg-main-blue font-semibold text-white transition hover:brightness-95"
          @click="openAddKategorieModal"
        >
          +
        </button>
        <button
          v-if="selectedRows.length > 0"
          type="button"
          class="inline-flex h-10.5 items-center justify-center rounded-xl border border-accent-red bg-accent-red px-4 text-sm font-semibold text-white transition hover:bg-hover-red cursor-pointer"
          @click="deleteSelectedRows"
        >
          Ausgewählte Löschen
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
            aria-label="Zur Kategorie in Aussagenpaaren"
            title="Zur Kategorie in Aussagenpaaren"
            @click="openAussagenpaareByKategorie(row)"
          >
            <svg class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <path d="M14 3v2h3.59L7 15.59 8.41 17 19 6.41V10h2V3z" />
              <path d="M5 5h5V3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2v-5h-2v5H5z" />
            </svg>
          </button>
          <button
            type="button"
            class="inline-flex h-8 w-8 items-center justify-center rounded-md border border-accent-red text-accent-red transition hover:bg-accent-red hover:text-white cursor-pointer"
            aria-label="Kategorie loeschen"
            title="Kategorie loeschen"
            @click="deleteRow(row)"
          >
            <svg class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <path d="M9 4h6l1 1h4v2H4V5h4l1-1Zm-2 3h10a1 1 0 0 1 1 1v11a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2V8a1 1 0 0 1 1-1Z" />
            </svg>
          </button>
        </div>
      </template>
    </Table>

    <div
      v-if="showAddKategorieModal"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 px-4"
    >
      <div class="w-full max-w-md rounded-2xl bg-white p-6 shadow-lg">
        <h2 class="mb-4 text-lg font-semibold text-grey-text">Kategorie erstellen</h2>

        <label for="kategoriename-input" class="mb-1 block text-sm font-medium text-grey-text">
          Kategoriename
        </label>
        <input
          id="kategoriename-input"
          v-model="kategorienameInput"
          type="text"
          class="w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-sm outline-none transition focus:border-blue-500"
          placeholder="Kategoriename eingeben..."
          @keyup.enter="createKategorie"
        />

        <p v-if="createKategorieError" class="mt-2 text-sm text-accent-red">
          {{ createKategorieError }}
        </p>

        <div class="mt-5 flex justify-end gap-3">
          <button
            type="button"
            class="rounded-xl border border-accent-red bg-accent-red px-4 py-2 text-sm font-semibold text-white transition hover:bg-hover-red"
            @click="closeAddKategorieModal"
            :disabled="isCreatingKategorie"
          >
            Abbrechen
          </button>
          <button
            type="button"
            class="rounded-xl border border-main-blue bg-main-blue px-4 py-2 text-sm font-semibold text-white transition hover:brightness-95 disabled:cursor-not-allowed disabled:opacity-60"
            @click="createKategorie"
            :disabled="isCreatingKategorie"
          >
            Erstellen
          </button>
        </div>
      </div>
    </div>

    <KategorieDeleteConfirmModal
      v-model="showDeleteConfirmModal"
      :title="getDeleteConfirmText()"
      :detail="getDeleteConfirmDetail()"
      @confirm="confirmDelete"
      @update:modelValue="closeDeleteConfirmModal"
    />
  </div>
</template>
