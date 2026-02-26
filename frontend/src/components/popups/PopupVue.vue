<script setup>
import { ref } from "vue"

import ConfirmUserModal from "./ConfirmUserModal.vue"
import CredentialsModal from "./CredentialsModal.vue"
import StatementModal from "./StatementModal.vue"
import Benutzeranlegen from "./Benutzeranlegen.vue"

/* -------------------------
   STATE
-------------------------- */

const showConfirm = ref(false)
const showCredentials = ref(false)
const showStatement = ref(false)
const showUserCreate = ref(false)

const statements = ref([
  { correct: false },
  { correct: true }
])

/* -------------------------
   HANDLER
-------------------------- */

function closeConfirm() {
  showConfirm.value = false
}

function confirmAction() {
  console.log("Bestätigt!")
  showConfirm.value = false
}

function saveStatements(updated) {
  console.log("Gespeichert:", updated)
  statements.value = updated
}

// function selectCategory() {
//   console.log("Kategorie auswählen")
// }

// function selectGraphic() {
//   console.log("Grafik auswählen")
// }

function closeUserCreate() {
  showUserCreate.value = false
}

function confirmUserCreate() {
  console.log("Benutzer angelegt")
  showUserCreate.value = false
}
</script>

<template>
  <div class="p-10 space-y-6 ">

    <div class="container">
      <!-- BUTTON 1 -->
      <button class="rounded-lg bg-blue-500 px-6 py-3 text-white" @click="showConfirm = true">
        Confirm Modal
      </button>

      <!-- BUTTON 2 -->
      <button class="rounded-lg bg-green-500 px-6 py-3 text-white" @click="showCredentials = true">
        Credentials Modal
      </button>

      <!-- BUTTON 3 -->
      <button class="rounded-lg bg-purple-500 px-6 py-3 text-white" @click="showStatement = true">
        Statement Modal
      </button>




    </div>

    <!-- ========================= -->
    <!-- VIEW 4 : Benutzeranlegen -->
    <!-- ========================= -->
    <!-- BUTTON 4 -->
    <div class="container">
      <!-- BUTTON 4 -->
      <button class="rounded-lg bg-orange-500 px-6 py-3 text-white" @click="showUserCreate = true">
        Benutzer anlegen
      </button>


    </div>
    <Benutzeranlegen :open="showUserCreate" text="Bitte gib deine E-Mail-Adresse ein" bt1="Abbrechen" bt2="Speichern"
      @cancel="closeUserCreate" @confirm="confirmUserCreate" />


    <!-- ========================= -->
    <!-- VIEW 1 : ConfirmUserModal -->
    <!-- ========================= -->

    <ConfirmUserModal :open="showConfirm" text="Möchtest du diesen Benutzer wirklich löschen?" username="max.mustermann"
      bt1="Abbrechen" bt2="Löschen" type="red" @cancel="closeConfirm" @confirm="confirmAction" />

    <!-- ========================= -->
    <!-- VIEW 2 : CredentialsModal -->
    <!-- ========================= -->

    <CredentialsModal :open="showCredentials" text="Deine Zugangsdaten wurden erstellt" btn="Schließen"
      @cancel="showCredentials = false" />

    <!-- ========================= -->
    <!-- VIEW 3 : StatementModal -->
    <!-- ========================= -->

    <StatementModal v-model="showStatement" :statements="statements" @save="saveStatements"
      @select-category="selectCategory" @select-graphic="selectGraphic" />


  </div>
</template>

<style scoped>
.container {
  display: flex;
  justify-content: space-between;
  flex-direction: column;
}

.container>button {
  margin: 4px;
  width: 400px;
}
</style>