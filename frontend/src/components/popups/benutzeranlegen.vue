<template>
  <div
    v-if="open"
    class="fixed inset-0 flex items-center justify-center bg-black/40 backdrop-blur-sm z-50"
  >
    <div class="bg-white rounded-3xl shadow-xl border-4 border-[#538fc6]/60 p-8 max-w-lg w-[90%] text-center">
      <h2 class="text-3xl font-semibold mb-8 leading-snug">
        {{ text }}<br />
        <input type="email" class="border-2 border-gray-300 rounded-lg px-4 py-2 mt-4 w-full" placeholder="E-Mail-Adresse eingeben" />
      
      </h2>

      <div class="flex justify-center gap-6">
        <button
          class="px-8 py-3 rounded-full border-2 border-[#538fc6]/90 text-[#538fc6] bg-white hover:bg-[#538fc6] text-lg font-medium transition"
          @click="$emit('cancel')"
        >
          {{ bt1 }}
        </button>

        <button
          class="px-8 py-3 rounded-full text-white text-lg font-medium tran bg-[#538fc6] hover:bg-[#538fc6]"
          @click="$emit('confirm')"
        >
          {{ bt2 }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  open: Boolean,
  text: String,
  username: String,
  bt1: String,
  bt2: String
 
});
</script>