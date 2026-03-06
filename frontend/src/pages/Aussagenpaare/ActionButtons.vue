
<template>
  <div class="flex gap-5">
    <template v-if="selectedRows.length === 0">
      <button class="border px-4 py-2 rounded">Importieren</button>
      <button class="bg-main-blue text-white px-4 py-2 rounded" @click="$emit('create')">
        Aussagenpaar hinzufügen
      </button>
    </template>

    <template v-else>
      <button class="bg-main-blue text-white px-4 py-2 rounded">Übung erstellen</button>
      <button class="bg-accent-red text-white px-4 py-2 rounded" @click="$emit('deleteSelected')">
        Löschen
      </button>
    </template>
  </div>
</template>

<script setup>
defineProps({
  selectedRows: Array
});

defineEmits(["create", "deleteSelected"]);
</script>
