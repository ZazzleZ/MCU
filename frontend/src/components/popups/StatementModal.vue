<!--------------------------------- Aussagepaare -------------------------------------->

<template>
  <!-- Overlay -->
  <div
    v-if="modelValue"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/40"
  >
    <!-- Modal -->
    <div class="w-[420px] rounded-2xl border-4 border-[#538fc6]/90 bg-white p-6">

      <!-- Aussagen -->
      <div
        v-for="(item, index) in localStatements"
        :key="index"
        class="mb-4"
      >
        <div class="mb-2 flex items-center justify-between font-semibold">
          <span>Aussage {{ index + 1 }}</span>

          <label class="flex items-center gap-2">
            korrekt?
            <input
              type="checkbox"
              v-model="item.correct"
              class="h-5 w-5 accent-red-500"
            />
          </label>
        </div>

        <div class="h-20 rounded-xl bg-[#538fc6]"></div>
      </div>

      <!-- Kommentar -->
      <div class="mb-4">
        <div class="mb-2 font-semibold">Kommentar</div>
        <div class="h-24 rounded-xl bg-[#538fc6]"></div>
      </div>

      <!-- Selectors -->
      <div class="mb-6 flex justify-between">
        <button
          class="flex items-center gap-2 rounded-lg border-2 border-[#538fc6]/90 px-4 py-2 font-medium text-[#538fc6]"
          @click="$emit('select-category')"
        >
          Kategorie ⬇
        </button>

        <button
          class="flex items-center gap-2 rounded-lg border-2 border-[#538fc6]/90 px-4 py-2 font-medium text-[#538fc6]"
          @click="$emit('select-graphic')"
        >
          Grafik ⬆
        </button>
      </div>

      <!-- Footer -->
      <div class="flex justify-between">
        <button
          class="rounded-lg bg-[#dd4d4d] px-6 py-2 font-semibold text-white"
          @click="close"
        >
          Abbrechen
        </button>

        <button
          class="rounded-lg bg-[#538fc6] px-6 py-2 font-semibold text-white"
          @click="save"
        >
          Speichern
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, watch } from "vue"

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  statements: {
    type: Array,
    default: () => [
      { correct: false },
      { correct: false }
    ]
  }
})

const emit = defineEmits([
  "update:modelValue",
  "save",
  "select-category",
  "select-graphic"
])

// lokale Kopie (Prototype-freundlich)
const localStatements = reactive(
  JSON.parse(JSON.stringify(props.statements))
)

// optional: sync bei Änderung
watch(
  () => props.statements,
  (val) => {
    localStatements.splice(
      0,
      localStatements.length,
      ...JSON.parse(JSON.stringify(val))
    )
  }
)

const close = () => {
  emit("update:modelValue", false)
}

const save = () => {
  emit("save", localStatements)
  close()
}
</script>
