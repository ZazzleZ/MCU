<script setup>
import { computed, onMounted, ref } from "vue";
import Table from "../components/Table.vue";
import BenutzerAnlegenModel from "../components/popus/BenutzerAnlegenModel.vue";

onMounted(() => {
  fetchUser()
})

const fetchUser = async () => {
  try {
    const response = await fetch("http://localhost:8000/users") // GET Request
    if (!response.ok) throw new Error("Fehler beim Laden der User")

    const data = await response.json()
    allRows.value = data       // Array mit Userdaten füllen
    console.log("User geladen:", allRows.value)
  } catch (err) {
    console.error(err)
  } finally {
    
  }
}

const columns = [
  { displayName: "Email", key: "email" },
  { displayName: "", key: "actions" },
];

const allRows = ref([]);

const selectedRows = ref([]);
const searchInput = ref("");
const appliedSearchText = ref("");

let showAddUserPopup = ref(false);

const filteredRows = computed(() =>
  allRows.value.filter((row) => {
    const query = appliedSearchText.value.trim().toLowerCase();
    return !query || row.email.toLowerCase().includes(query);
  }),
);

const applySearch = () => {
  appliedSearchText.value = searchInput.value;
};

const addUserButton = () => {
  showAddUserPopup.value = true;
};

const resetUser = async (row) => {
  try {
    const response = await fetch(`http://localhost:8000/users/${row.id}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({  
        id: row.id,
        email: row.email,
        password: row.password,
        is_admin: row.is_admin,
        needs_pw_change: true
      }),
    });

    if (!response.ok) throw new Error("Fehler beim Setzen von 'needs_pw_change'");

    // Frontend aktualisieren
    const updatedUser = await response.json();
    allRows.value = allRows.value.map((item) =>
      item.id === updatedUser.id ? updatedUser : item
    );

    console.log(`Benutzer ${row.email} muss nun Passwort ändern`);
  } catch (err) {
    console.error(err);
    alert("Fehler beim Aktualisieren des Benutzers");
  }
};

const deleteRow = (row) => {
  if (!confirm(`Benutzer ${row.email} wirklich löschen?`)) return;
  deleteUser(row)
};

const deleteSelectedRows = () => {
  if (!confirm(`wirklich alle löschen?`)) return;
  for (const row of selectedRows.value) {
    deleteUser(row)
  }

  const selectedIds = new Set(selectedRows.value.map((row) => row.id));
  allRows.value = allRows.value.filter((item) => !selectedIds.has(item.id));
  selectedRows.value = [];
};

const confirmAddUser = () => {
  console.log("Confirm")
  showAddUserPopup.value = false
  fetchUser()
}

const cancelAddUser = () => {
  console.log("Cancel")
  showAddUserPopup.value = false
}

const deleteUser = async (row) => {
  try {
    const response = await fetch(`http://localhost:8000/users/${row.id}`, {
      method: "DELETE",
    });

    if (!response.ok) throw new Error("Fehler beim Löschen des Benutzers");

    // Frontend aktualisieren
    allRows.value = allRows.value.filter((item) => item.id !== row.id);
    selectedRows.value = selectedRows.value.filter((item) => item.id !== row.id);

    console.log(`Benutzer ${row.email} gelöscht`);
  } catch (err) {
    console.error(err);
    alert("Fehler beim Löschen des Benutzers");
  }
};
</script>

<template>
  <BenutzerAnlegenModel v-if="showAddUserPopup" @confirm="confirmAddUser" @cancel="cancelAddUser" />
  <div class="m-15 flex flex-col gap-10 text-grey-text">
    <div class="flex flex-row justify-between gap-5">
      <div class="flex margin-bottom-20 gap-2">
        <div class="flex items-center gap-2">
          <input
            v-model="searchInput"
            type="text"
            placeholder="Suche..."
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
      </div>

      <div class="flex justify-end gap-3">
        <button
          type="button"
          class="inline-flex size-10.5 items-center justify-center text-xl cursor-pointer rounded-xl border border-main-blue bg-main-blue font-semibold text-white transition hover:brightness-95"
          aria-label="Benutzer hinzufuegen"
          title="Benutzer hinzufuegen"
          @click="addUserButton"
        >
          +
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
            aria-label="Benutzer zuruecksetzen"
            title="Benutzer zuruecksetzen"
            @click="resetUser(row)"
          >
            <svg class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true">
              <path d="M3 11a9 9 0 0 1 15.36-6.36L21 7" stroke-linecap="round" stroke-linejoin="round" />
              <path d="M21 13a9 9 0 0 1-15.36 6.36L3 17" stroke-linecap="round" stroke-linejoin="round" />
              <path d="M21 7h-5" stroke-linecap="round" />
              <path d="M3 17h5" stroke-linecap="round" />
            </svg>
          </button>
          <button
            type="button"
            class="inline-flex h-8 w-8 items-center justify-center rounded-md border border-accent-red text-accent-red transition hover:bg-accent-red hover:text-white cursor-pointer"
            aria-label="Benutzer loeschen"
            title="Benutzer loeschen"
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
