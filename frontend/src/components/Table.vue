<script setup>
import { computed, ref, useSlots, watchEffect } from "vue";


const props = defineProps({
  columns: {
    type: Array,
    required: true,
    validator: (value) =>
      value.every(
        (column) =>
          typeof column === "object" &&
          column !== null &&
          typeof column.displayName === "string" &&
          typeof column.key === "string",
      ),
  },
  rows: {
    type: Array,
    default: () => [],
  },
  selectedRows: {
    type: Array,
    default: () => [],
  },
  rowKey: {
    type: String,
    default: "id",
  },
});

const emitSelectedRows = defineEmits(["update:selectedRows"]);
const slots = useSlots();

const selectAllCheckbox = ref(null);

const rowHasKey = (row) =>
  row?.[props.rowKey] !== undefined && row?.[props.rowKey] !== null;

const keyedSelection = computed(() => {
  const selectedKeys = new Set();

  props.selectedRows.forEach((row) => {
    if (rowHasKey(row)) {
      selectedKeys.add(row[props.rowKey]);
    }
  });

  return selectedKeys;
});

const isRowSelected = (row) => {
  if (rowHasKey(row)) {
    return keyedSelection.value.has(row[props.rowKey]);
  }

  return props.selectedRows.includes(row);
};

const allRowsSelected = computed(
  () => props.rows.length > 0 && props.rows.every((row) => isRowSelected(row)),
);

const someRowsSelected = computed(
  () => props.rows.some((row) => isRowSelected(row)) && !allRowsSelected.value,
);

watchEffect(() => {
  if (selectAllCheckbox.value) {
    selectAllCheckbox.value.indeterminate = someRowsSelected.value;
  }
});

const setRowSelected = (row, isSelected) => {
  const nextSelection = [...props.selectedRows];

  if (rowHasKey(row)) {
    const key = row[props.rowKey];
    const filtered = nextSelection.filter(
      (selectedRow) => !rowHasKey(selectedRow) || selectedRow[props.rowKey] !== key,
    );

    emitSelectedRows("update:selectedRows", isSelected ? [...filtered, row] : filtered);
    return;
  }

  if (isSelected && !nextSelection.includes(row)) {
    emitSelectedRows("update:selectedRows", [...nextSelection, row]);
    return;
  }

  if (!isSelected) {
    emitSelectedRows(
      "update:selectedRows",
      nextSelection.filter((selectedRow) => selectedRow !== row),
    );
  }
};

const setAllRowsSelected = (isSelected) => {
  emitSelectedRows("update:selectedRows", isSelected ? [...props.rows] : []);
};

const lastColumn = computed(() =>
  props.columns.length > 0 ? props.columns[props.columns.length - 1] : null,
);
</script>

<template>
  <div class="overflow-x-auto rounded-xl border border-slate-200 bg-white shadow-sm">
    <table class="min-w-full border-collapse text-sm text-slate-700">
      <thead
        class="bg-slate-100 text-left text-xs font-semibold uppercase tracking-wide text-slate-600"
      >
        <tr>
          <th scope="col" class="w-12 px-4 py-3 text-center">
            <label class="relative inline-flex h-4 w-4 cursor-pointer items-center justify-center">
              <input
                ref="selectAllCheckbox"
                type="checkbox"
                class="peer sr-only"
                :checked="allRowsSelected"
                aria-label="Select all rows"
                @change="setAllRowsSelected($event.target.checked)"
              />
              <span
                class="h-4 w-4 rounded border border-slate-300 bg-white peer-checked:border-main-blue peer-checked:bg-main-blue peer-focus-visible:ring-2 peer-focus-visible:ring-main-blue peer-focus-visible:ring-offset-1"
              ></span>
              <svg
                class="pointer-events-none absolute h-3 w-3 text-white opacity-0 drop-shadow-[0_0_1px_rgba(0,0,0,0.35)] peer-checked:opacity-100"
                viewBox="0 0 16 16"
                fill="none"
                aria-hidden="true"
              >
                <path
                  d="M3.5 8.5L6.5 11.5L12.5 4.5"
                  stroke="currentColor"
                  stroke-width="2.8"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>
            </label>
          </th>
          <th
            v-for="column in columns"
            :key="column.key"
            scope="col"
            class="px-4 py-3"
          >
            <template v-if="lastColumn && column.key === lastColumn.key && slots.actions"></template>
            <template v-else>{{ column.displayName }}</template>
          </th>
        </tr>
      </thead>

      <tbody class="divide-y divide-slate-200">
        <tr v-if="rows.length === 0">
          <td :colspan="columns.length + 1" class="px-4 py-6"></td>
        </tr>

        <tr
          v-for="(row, rowIndex) in rows"
          v-else
          :key="row?.[props.rowKey] ?? row.id ?? rowIndex"
          :class="[
            rowIndex % 2 === 1 ? 'bg-slate-100/50' : 'bg-white',
            'hover:bg-slate-100/70',
          ]"
        >
          <td class="w-12 px-4 py-3 text-center">
            <label class="relative inline-flex h-4 w-4 cursor-pointer items-center justify-center">
              <input
                type="checkbox"
                class="peer sr-only"
                :checked="isRowSelected(row)"
                :aria-label="`Select row ${rowIndex + 1}`"
                @change="setRowSelected(row, $event.target.checked)"
              />
              <span
                class="h-4 w-4 rounded border border-slate-300 bg-white peer-checked:border-main-blue peer-checked:bg-main-blue peer-focus-visible:ring-2 peer-focus-visible:ring-main-blue peer-focus-visible:ring-offset-1"
              ></span>
              <svg
                class="pointer-events-none absolute h-3 w-3 text-white opacity-0 drop-shadow-[0_0_1px_rgba(0,0,0,0.35)] peer-checked:opacity-100"
                viewBox="0 0 16 16"
                fill="none"
                aria-hidden="true"
              >
                <path
                  d="M3.5 8.5L6.5 11.5L12.5 4.5"
                  stroke="currentColor"
                  stroke-width="2.8"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>
            </label>
          </td>
          <td
            v-for="column in columns"
            :key="`${rowIndex}-${column.key}`"
            class="px-4 py-3"
          >
            <slot
              v-if="lastColumn && column.key === lastColumn.key && slots.actions"
              name="actions"
              :row="row"
              :row-index="rowIndex"
            >
              {{ row[column.key] ?? "" }}
            </slot>
            <template v-else>
              {{ row[column.key] ?? "" }}
            </template>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
