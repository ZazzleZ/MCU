<script setup>
import { ref } from "vue"

/* -------------------------
   PROPS & EMITS
-------------------------- */

const props = defineProps({
  open: Boolean,
  text: String,
  bt1: String,
  bt2: String
})

const emit = defineEmits(["cancel", "confirm"])

const email = ref("")

/* -------------------------
   SUBMIT
-------------------------- */

async function submit() {
  if (!email.value) {
    alert("Bitte eine gültige E-Mail eingeben!")
    return
  }

  try {
    const response = await fetch("http://localhost:8000/users", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: email.value })
    })

    if (!response.ok) throw new Error("Fehler beim Speichern")

    const data = await response.json()
    console.log("Gespeichert:", data)

    alert("Benutzer erfolgreich erstellt!")
    email.value = ""

    emit("confirm") // 👈 Parent schließt Modal
  } catch (err) {
    console.error(err)
    alert("Fehler beim Erstellen des Benutzers")
  }
}
</script>

<template>
  <div
    v-if="open"
    class="fixed inset-0 flex items-center justify-center bg-black/40 backdrop-blur-sm z-50"
  >
    <div
      class="bg-white rounded-3xl shadow-xl border-4 border-[#538fc6]/60 p-8 max-w-lg w-[90%] text-center"
    >
      <h2 class="text-3xl font-semibold mb-8 leading-snug">
        {{ text }}
      </h2>

      <input
        v-model="email"
        type="email"
        class="border-2 border-gray-300 rounded-lg px-4 py-2 mb-6 w-full"
        placeholder="E-Mail-Adresse eingeben"
      />

      <div class="flex justify-center gap-6">
        <button
          class="px-8 py-3 rounded-full border-2 border-[#538fc6]/90 text-[#538fc6] hover:bg-[#538fc6] hover:text-white transition"
          @click="emit('cancel')"
        >
          {{ bt1 }}
        </button>

        <button
          class="px-8 py-3 rounded-full text-white bg-[#538fc6] hover:bg-[#538fc6]/90 transition"
          @click="submit"
        >
          {{ bt2 }}
        </button>
      </div>
    </div>
  </div>
</template>