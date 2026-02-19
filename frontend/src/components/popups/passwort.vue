<template>
  <div
    v-if="open"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm"
  >
    <div
      class="w-[90%] max-w-lg rounded-3xl border-4 border-[#538fc6] bg-white p-8 text-center shadow-xl"
    >
      <h2 class="mb-8 text-3xl font-semibold leading-snug">
        {{ text }}<br />
        <span class="text-[#538fc6]">@{{ username }}</span>
      </h2>

      <div class="flex justify-center gap-6">
        <!-- Cancel -->
        <button
          class="rounded-full border-2 border-[#538fc6] bg-white px-8 py-3 text-lg font-medium text-[#538fc6] transition hover:bg-[#538fc6]/80 hover:text-white"
          @click="$emit('cancel')"
        >
          {{ bt1 }}
        </button>

        <!-- Confirm -->
        <button
          class="rounded-full px-8 py-3 text-lg font-medium text-white transition"
          :class="{
            'bg-[#538fc6] hover:bg-[#538fc6]/80': type === 'blue',
            'bg-[#ff3131] hover:bg-[#ff3131]/80': type === 'red'
          }"
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
  bt2: String,
  type: {
    type: String,
    default: "blue",
  },
});
</script>
