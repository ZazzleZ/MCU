<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';

// UI-Komponenten (deine relativen Pfade stimmen)
import StatementModal from '../../components/popus/StatementModal.vue';
// import UpdateAussageModal from '../../components/popus/Aussagenpaaren/UpdateAussageModal.vue';
import StatementTable from './StatementTable.vue';
import FilterBar from './FilterBar.vue';
import ActionButtons from './ActionButtons.vue';

/* =========================================================
   Typen (du kannst sie später in /types auslagern)
========================================================= */
type ID = string | number;

interface User {
  id: ID;
  email: string;
}

interface Kategorie {
  id: ID;
  name: string;
}

interface Aussage {
  id: ID;
  aussage: string;
  loesung: boolean;
}

interface AussagenPairRaw {
  id: ID;
  kategorie: ID[];                  // Array von Kategorie-IDs
  aussagen: (ID | { id: ID })[];    // IDs oder Objekte mit ID
  kommentar?: string;
  grafik_url?: string;
  bearbeiter?: string;
  _aussagenTexte?: string[];        // wird lokal befüllt
}

interface TabellenZeile {
  id: ID;
  kategorie: string;     // schon in Namen gemappt, kommasepariert
  aussage_eins: string;
  aussage_zwei: string;
  kommentar: string;
  grafik_url: string;
  bearbeiter: string;
}

/* =========================================================
   Konstanten
========================================================= */
const API_BASE = 'http://127.0.0.1:8000';

/* =========================================================
   State
========================================================= */
const allRowsRaw = ref<AussagenPairRaw[]>([]);
const kategorien = ref<Kategorie[]>([]);
const users = ref<User[]>([]);

const selectedRows = ref<TabellenZeile[]>([]);
const selectedKategorie = ref<string>('');   // empty = alle
const selectedBearbeiter = ref<string>('');  // empty = alle

const showStatementModal = ref(false);
const modalOpen = ref(false);
const currentRow = ref<AussagenPairRaw | null>(null);

// Für StatementModal (Create) / Update
const statements = ref<{ id?: ID; text: string; correct: boolean }[]>([
  { text: '', correct: false },
  { text: '', correct: false }
]);

/* =========================================================
   Spalten der Tabelle
========================================================= */
const columns = [
  { displayName: 'Kategorie', key: 'kategorie' },
  { displayName: 'Aussage 1', key: 'aussage_eins' },
  { displayName: 'Aussage 2', key: 'aussage_zwei' },
  { displayName: 'Kommentar', key: 'kommentar' },
  { displayName: 'Grafik', key: 'grafik_url' },
  { displayName: '', key: 'actions' },
];

/* =========================================================
   Hilfen / Mapper
========================================================= */
const catMap = computed<Record<string | number, string>>(() =>
  Object.fromEntries((kategorien.value || []).map(k => [k.id, k.name]))
);

const allRows = computed<TabellenZeile[]>(() =>
  allRowsRaw.value.map(item => ({
    id: item.id,
    kategorie: (item.kategorie || []).map(k => catMap.value[k] ?? String(k)).join(', '),
    aussage_eins: item._aussagenTexte?.[0] ?? '',
    aussage_zwei: item._aussagenTexte?.[1] ?? '',
    kommentar: item.kommentar ?? '',
    grafik_url: item.grafik_url ?? '',
    bearbeiter: item.bearbeiter ?? '',
  }))
);

// Optionen für die FilterBar (aus den gemappten Zeilen extrahiert)
const kategorieOptionen = computed<string[]>(() => {
  const s = new Set<string>();
  for (const row of allRows.value) {
    row.kategorie.split(',').map(x => x.trim()).filter(Boolean).forEach(v => s.add(v));
  }
  return Array.from(s).sort((a, b) => a.localeCompare(b));
});

// Gefilterte Zeilen
const filteredRows = computed<TabellenZeile[]>(() =>
  allRows.value.filter(row => {
    const cats = row.kategorie.split(',').map(x => x.trim()).filter(Boolean);
    const matchCat = !selectedKategorie.value || cats.includes(selectedKategorie.value);
    const matchBearbeiter = !selectedBearbeiter.value || row.bearbeiter === selectedBearbeiter.value;
    return matchCat && matchBearbeiter;
  })
);

// Für UpdateAussageModal: gemappte Statements aus currentRow
const mappedStatements = computed(() =>
  (currentRow.value?.aussagen ?? []).map((a, idx) => {
    const id = typeof a === 'string' || typeof a === 'number' ? a : a.id;
    const text = currentRow.value?._aussagenTexte?.[idx] ?? '';
    // correct-Wert wird beim Edit gezielt nachgeladen (siehe editRow)
    return { id, text, correct: false };
  })
);

/* =========================================================
   Loader
========================================================= */
async function loadAussage(id: ID): Promise<Aussage | null> {
  const res = await fetch(`${API_BASE}/aussagen/${id}`);
  if (!res.ok) return null;
  return res.json();
}

async function loadPairs(): Promise<void> {
  const res = await fetch(`${API_BASE}/aussagenpaare`);
  const pairs: AussagenPairRaw[] = await res.json();

  for (const pair of pairs) {
    const ids = (pair.aussagen || [])
      .filter(a => a != null)
      .map(a => (typeof a === 'string' || typeof a === 'number' ? a : a.id))
      .filter(id => id != null);

    const loaded = await Promise.all(ids.map(loadAussage));
    pair._aussagenTexte = loaded.map(a => a?.aussage ?? '');
  }
  allRowsRaw.value = pairs;
}

async function loadUsers(): Promise<void> {
  const res = await fetch(`${API_BASE}/users`);
  if (res.ok) users.value = await res.json();
}

async function loadCategories(): Promise<void> {
  const res = await fetch(`${API_BASE}/kategorien`);
  if (res.ok) kategorien.value = await res.json();
}

onMounted(async () => {
  await Promise.all([loadCategories(), loadPairs(), loadUsers()]);
});

/* =========================================================
   Actions (Create/Update/Delete)
========================================================= */
function openCreateModal(): void {
  statements.value = [
    { text: '', correct: false },
    { text: '', correct: false },
  ];
  showStatementModal.value = true;
}

async function afterCreate(): Promise<void> {
  await loadPairs();
  showStatementModal.value = false;
}

// Edit: lädt die vollständigen Aussagen (inkl. loesung) neu,
// damit UpdateAussageModal die "correct"-Flags korrekt bekommt.
async function editRow(row: TabellenZeile): Promise<void> {
  modalOpen.value = true;

  const raw = allRowsRaw.value.find(p => p.id === row.id);
  if (!raw) return;

  currentRow.value = raw;

  const ids = (raw.aussagen || []).map(a => (typeof a === 'string' || typeof a === 'number' ? a : a.id));
  const texte = await Promise.all(ids.map(loadAussage));

  statements.value = texte.map(a => ({
    id: a?.id,
    text: a?.aussage ?? '',
    correct: a?.loesung ?? false,
  }));
}

async function afterUpdate(): Promise<void> {
  modalOpen.value = false;
  currentRow.value = null;
  await loadPairs();
}

async function deleteRow(row: TabellenZeile): Promise<void> {
  if (!confirm('Willst du dieses Aussagenpaar wirklich löschen?')) return;

  const raw = allRowsRaw.value.find(p => p.id === row.id);
  if (!raw) return;

  const ids = raw.aussagen.map(a => (typeof a === 'string' || typeof a === 'number' ? a : a.id));

  await fetch(`${API_BASE}/aussagenpaare/${row.id}`, { method: 'DELETE' });

  for (const id of ids) {
    await fetch(`${API_BASE}/aussagen/${id}`, { method: 'DELETE' });
  }

  await loadPairs();
}

async function deleteSelectedRows(): Promise<void> {
  if (selectedRows.value.length === 0) return;
  if (!confirm(`Willst du wirklich ${selectedRows.value.length} ausgewählte Paare löschen?`)) return;

  // IDs der ausgewählten Zeilen
  const idsToDelete = selectedRows.value.map(r => r.id);

  // Rohdatensätze finden und deren Aussagen-IDs mitlöschen
  const rawToDelete = allRowsRaw.value.filter(r => idsToDelete.includes(r.id));

  for (const pair of rawToDelete) {
    await fetch(`${API_BASE}/aussagenpaare/${pair.id}`, { method: 'DELETE' });
    const aussageIds = pair.aussagen.map(a => (typeof a === 'string' || typeof a === 'number' ? a : a.id));
    for (const aid of aussageIds) {
      await fetch(`${API_BASE}/aussagen/${aid}`, { method: 'DELETE' });
    }
  }

  selectedRows.value = [];
  await loadPairs();
}

/* =========================================================
   Exporte für Template (nicht nötig bei <script setup>, nur Info)
========================================================= */
// users, kategorieOptionen, selectedKategorie, selectedBearbeiter,
// selectedRows, filteredRows, columns, showStatementModal, modalOpen,
// currentRow, statements, mappedStatements, openCreateModal, afterCreate,
// editRow, afterUpdate, deleteRow, deleteSelectedRows
</script>