<template>
  <Table 
    :columns="columns" 
    :rows="rows"
    v-model:selectedRows="selectedRows"
  >
    <template #actions="{ row }">
      <button @click="$emit('edit', row)">✏️</button>
      <button @click="$emit('delete', row)">🗑️</button>
    </template>
  </Table>
</template>

<script setup>
import Table from "../components/Table.vue";

defineProps({
  rows: Array,
  selectedRows: Array,
  columns: Array
});

defineEmits(["edit", "delete", "update:selectedRows"]);
</script>