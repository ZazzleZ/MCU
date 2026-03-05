<script setup lang="ts">
import Sidebar from '../components/Sidebar.vue';
import { computed } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const showSidebar = computed(() => !route.path.startsWith('/durchfuehren'));

</script>

<template>
  <div class="flex h-screen">
    <Sidebar v-if="showSidebar" />

    <div class="flex-1 flex flex-col overflow-hidden">
      <main class="flex-1 overflow-y-auto p-6">
        <router-view />
      </main>
    </div>
  </div>
</template>
