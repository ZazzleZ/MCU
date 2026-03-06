<template>
  <div class="flex gap-5">
    <select v-model="kategorieModel" class="min-w-52 border rounded-xl">
      <option value="">Alle Kategorien</option>
      <option v-for="k in kategorien" :key="k" :value="k">{{ k }}</option>
    </select>

    <select v-model="bearbeiterModel" class="min-w-52 border rounded-xl">
      <option value="">Alle Bearbeiter</option>
      <option v-for="u in users" :key="u.id" :value="u.email">{{ u.email }}</option>
    </select>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  kategorien: { type: Array, default: () => [] },
  users: { type: Array, default: () => [] },
  kategorie: { type: String, default: '' },
  bearbeiter: { type: String, default: '' }
});

const emit = defineEmits(['update:kategorie', 'update:bearbeiter']);

const kategorieModel = computed({
  get: () => props.kategorie,
  set: (val) => emit('update:kategorie', val)
});

const bearbeiterModel = computed({
  get: () => props.bearbeiter,
  set: (val) => emit('update:bearbeiter', val)
});
</script>
