<template>
    <div class="w-130 h-130 border-2 rounded-2xl border-border-grey bg-white">
        <h2 class="text-center mt-10 text-4xl font-bold text-grey-text">Neues Passwort</h2>
        <div class="flex flex-col items-center mt-15 gap-10">
            <input type="password" placeholder="Neues Passwort"
                class="w-full max-w-md px-6 py-3 rounded-full border-2 
                    border-border-grey hover:bg-gray-100 text-grey-text placeholder-grey-text outline-none focus:border-gray-800 transition" />
            <input type="password" placeholder="Passwort bestätigen"
                class="w-full max-w-md px-6 py-3 rounded-full border-2 
                    border-border-grey hover:bg-gray-100 text-grey-text placeholder-grey-text outline-none focus:border-gray-800 transition" />

            <button class="w-full mt-10 max-w-md py-3 rounded-full bg-main-blue text-white text-lg font-medium
                shadow-md hover:bg-hover-blue active:bg-blue-400 transition">Bestätigen</button>
        </div>
    </div>
</template>