<script setup lang="ts">
import Sidebar from '../components/Sidebar.vue';

</script>

<template>
  <div class="flex h-screen">
    <Sidebar />

    <div class="flex-1 flex flex-col overflow-hidden">
      <main class="flex-1 overflow-y-auto p-6">
        <router-view />
      </main>
    </div>
  </div>
</template>