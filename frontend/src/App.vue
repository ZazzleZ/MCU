
<script setup>
import { ref } from "vue"
import aussagepaare from "./components/popups/aussagepaare.vue"
import Passwort from "./components/popups/passwort.vue"

const open = ref(false)

const statements = ref([
  { correct: true },
  { correct: false }
])

const onSave = (data) => {
  console.log("Gespeichert:", data)
}
</script>

<template>
  <button
    class="rounded-lg bg-blue-500 px-6 py-2 text-white"
    @click="open = true"
  >
    Popup öffnen
  </button>

  <!-- <aussagepaare
    v-model="open"
    :statements="statements"
    @save="onSave"
  /> -->

  <Passwort
    :open="open"
    text="Möchten Sie wirklich das Passwort zurücksetzen?"
    username="MustafaHafez"
    bt1="Abbrechen"
    bt2="Löschen"
    type="red"
    @cancel="open = false"
    @confirm="onSave('Passwort zurückgesetzt')"
  />
</template>
