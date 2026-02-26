<template>
  <div
    v-if="open"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm p-4"
  >
    <div
      class="w-full max-w-lg rounded-3xl border-4 border-blue-200 bg-white p-8 text-center shadow-xl"
    >
      <h2 class="mb-6 text-3xl font-semibold leading-snug">
        {{ text }}
      </h2>

      <!-- Info Box -->
      <div class="mb-8 rounded-2xl bg-gray-50 p-5 text-left space-y-4">
        <div class="flex items-center justify-between gap-4">
          <span class="text-sm font-medium text-gray-600">Email</span>
          <span class="font-semibold text-gray-900">asd@asd.com</span>
        </div>

        <div class="flex items-center justify-between gap-4">
          <span class="text-sm font-medium text-gray-600">Password</span>
          <span class="font-semibold text-gray-900">••••••••••••</span>
        </div>
      </div>

      <!-- Button -->
      <div class="flex justify-center">
        <button
          class="rounded-full px-10 py-3 text-lg font-medium text-white transition hover:opacity-90"
          style="background-color:#538fc6"
          @click="$emit('cancel')"
        >
          {{ btn }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  open: Boolean,
  text: String,
  btn: String,
});
</script>
