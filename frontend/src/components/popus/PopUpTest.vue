<script setup>
import { ref } from "vue"

/* Import your modals */
import ConfirmUserModal from "./ConfirmUserModal.vue"
import CredentialsModal from "./CredentialsModal.vue"
import StatementModal from "./StatementModal.vue"
import BenutzerAnlegenModel from "./BenutzerAnlegenModel.vue"

/* popup state */
const activePopup = ref(null)

/* shared data */
const popupData = ref({})

/* public API */
const openPopup = (name, data = {}) => {
  popupData.value = data
  activePopup.value = name
}

const closePopup = () => {
  activePopup.value = null
  popupData.value = {}
}

/* expose to parent */
defineExpose({
  openPopup,
  closePopup
})
</script>

<template>
  <!-- Confirm User -->
  <ConfirmUserModal
    v-if="activePopup === 'confirm-user'"
    :open="true"
    v-bind="popupData"
    @cancel="closePopup"
    @confirm="popupData.onConfirm?.(); closePopup()"
  />

  <!-- Credentials -->
  <CredentialsModal
    v-if="activePopup === 'credentials'"
    :open="true"
    v-bind="popupData"
    @cancel="closePopup"
  />

  <!-- Statement -->
  <StatementModal
    v-if="activePopup === 'statement'"
    v-model="popupData.modelValue"
    :statements="popupData.statements"
    @save="popupData.onSave"
    @select-category="popupData.onSelectCategory"
    @select-graphic="popupData.onSelectGraphic"
  />

  <!-- Benutzer anlegen -->
  <BenutzerAnlegenModel
    v-if="activePopup === 'create-user'"
    :open="true"
    v-bind="popupData"
    @cancel="closePopup"
    @confirm="popupData.onConfirm?.(); closePopup()"
  />
</template>