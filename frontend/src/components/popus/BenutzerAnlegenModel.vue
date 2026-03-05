<script setup>
import { ref } from "vue"

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
      body: JSON.stringify({  
        email: email.value,
        password: "",
        is_admin: false,
        needs_pw_change: true
      })
      
    })

    if (!response.ok) throw new Error("Fehler beim Speichern")

    const data = await response.json()
    console.log("Gespeichert:", data)

    email.value = ""

    emit("confirm") // 👈 Parent schließt Modal
  } catch (err) {
    console.error(err)
    alert("Fehler beim Erstellen des Benutzers")
  }
}

function close() {
  email.value = ""
  emit("cancel")
}
</script>

<template>
  <div
    class="fixed inset-0 flex items-center justify-center bg-black/40 backdrop-blur-sm z-50"
  >
    <div
      class="bg-white rounded-3xl shadow-xl border-4 border-[#538fc6]/60 p-8 max-w-lg w-[90%] text-center"
    >
      <h2 class="text-3xl font-semibold mb-8 leading-snug">
        Benutzer anlegen
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
          @click="close"
        >
          Abbrechen
        </button>

        <button
          class="px-8 py-3 rounded-full text-white bg-[#538fc6] hover:bg-[#538fc6]/90 transition"
          @click="submit"
        >
          Anlegen
        </button>
      </div>
    </div>
  </div>
</template>