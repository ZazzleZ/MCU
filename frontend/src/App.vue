<script setup>

import { ref } from "vue";

import HelloWorld from './components/HelloWorld.vue'
import PasswordModal from './components/popups/popup.vue'

const showModal = ref(false);

function handleGenerate() {
  showModal.value = false;
  console.log("Passwort generieren...");
  alert("Neues Passwort generiert!");
}

</script>

<template>
  <div>
    <a href="https://vite.dev" target="_blank">
      <img src="/vite.svg" class="logo" alt="Vite logo" />
    </a>
    <a href="https://vuejs.org/" target="_blank">
      <img src="./assets/vue.svg" class="logo vue" alt="Vue logo" />
    </a>
  </div>
  <HelloWorld msg="Vite + Vue" />
  

  <button  class="text-blue-500" @click="showModal = true">Passwort ändern</button>

  <PasswordModal
    :open="showModal"
    text="Passwort neu generieren?"
    username="mostafa"
    bt1="Abbrechen"
    bt2="Generieren"
    type="blue"
    @cancel="showModal = false"
    @confirm="handleGenerate"
  />






</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
