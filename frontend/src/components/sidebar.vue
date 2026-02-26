<script setup>
const menuItems = [
    { name: 'Startseite' },
    { name: 'Aussagenpaare' },
    { name: 'Übungen' },
    { name: 'Kategorien' },
    { name: 'Admindashboard' },
];

const email = 'max.mustermann@example.com';

const logout = () => {
    alert('Abgemeldet!');
};
</script>


<template>
    <aside class="flex flex-col w-80 h-screen bg-main-blue text-white justify-between">
        <div>
            <img src="../assets/gso-logo.png" alt="gso logo">
            <nav>
                <ul>
                    <li v-for="item in menuItems" :key="item.name"
                        class=" text-2xl p-5 hover:bg-hover-black rounded-md cursor-pointer">
                        {{ item.name }}
                    </li>
                </ul>
            </nav>
        </div>

        <div class="p-5 mb-4">
            <p class="text-[1rem] mb-5 truncate" :title="email">{{ email }}</p>
            <button @click="logout"
                class="w-full p-2 bg-accent-red hover:bg-hover-red rounded text-white font-medium text-2xl">
                Abmelden
            </button>
        </div>
    </aside>
</template>