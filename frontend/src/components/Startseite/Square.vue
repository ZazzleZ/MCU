<script setup lang="ts">
import { RouterLink } from 'vue-router';


const props = defineProps({
    text: String,
    routerLink: String
})

</script>

<template>
    <router-link :to="'/' + props.routerLink" :key="props.text" class="w-60 h-60 border-main-blue border-2 rounded-2xl flex items-center justify-center text-grey-text 
            hover:bg-main-blue hover:text-white cursor-pointer text-2xl font-bold">
        {{ props.text }}
    </router-link>
</template>