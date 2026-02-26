<script setup lang="ts">
import Square from '../components/Startseite/Square.vue';

</script>

<template>
    <h2 class="text-4xl ml-10 mt-15">Hallo, [User-Email]</h2>
    <div class="ml-10 mt-15 flex gap-15 flex-wrap">
        <Square text="Aussagenpaare" routerLink="aussagenpaare" />
        <Square text="Übungen" routerLink="uebungen" />
        <Square text="Kategorien" routerLink="kategorien" />
        <Square text="Admindashboard" routerLink="admindashboard" />
    </div>
</template>