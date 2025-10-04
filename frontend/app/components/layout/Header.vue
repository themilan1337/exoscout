<template>
    <div class="flex justify-between items-center border-b border-dashed border-zinc-300">
        <NuxtLink to="/" class="flex cursor-pointer transition hover:bg-zinc-100">
            <img src="/nasa.png" alt="NASA Logo" class="my-auto ml-2 h-5 w-6 mr-1" />
            <svg class="size-4 my-auto" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24"><!-- Icon from Material Symbols Light by Google - https://github.com/google/material-design-icons/blob/master/LICENSE --><path fill="currentColor" d="m8.401 16.333l-.734-.727L11.266 12L7.667 8.42l.734-.728L12 11.29l3.574-3.597l.734.727L12.709 12l3.599 3.606l-.734.727L12 12.737z"/></svg>
            <Logo fill="#000" class="my-auto" />
            <h1 class="my-auto border-r border-dashed py-1 border-zinc-300 px-2 text-sm flex items-center">exoscout.vercel.app</h1>
        </NuxtLink>
        <div class="flex">
            <NuxtLink to="/team" class="cursor-pointer border-l border-r border-dashed border-zinc-300 px-6 py-1 text-sm transition hover:bg-zinc-100 flex items-center gap-2">
                Team
                <svg class="size-4" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24"><!-- Icon from Pixel Icon by HackerNoon - https://creativecommons.org/licenses/by/4.0/ --><path fill="currentColor" d="M16 20h-1v1H2v-1H1v-3h1v-1h1v-1h1v-1h9v1h1v1h1v1h1zm-3-8v-1h1V5h4v1h1v5h-1v1z"/><path fill="currentColor" d="M23 17v3h-1v1h-6v-1h1v-4h-1v-1h-1v-1h5v1h1v1h1v1zM12 3v1h-1v1h-1V4H9V3H8v1H7v1H6V4H5V3H4v7h1v1h1v1h5v-1h1v-1h1V3zm-1 6h-1v1H7V9H6V7h5z"/></svg>
            </NuxtLink>
            <NuxtLink to="https://github.com/themilan1337/exoscout" class="cursor-pointer px-6 py-1 text-sm transition hover:bg-zinc-100 flex items-center gap-2">
                Github
                <svg class="size-4" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24"><!-- Icon from Pixel Icon by HackerNoon - https://creativecommons.org/licenses/by/4.0/ --><path fill="currentColor" d="M23 9v6h-1v2h-1v2h-1v1h-1v1h-1v1h-2v1h-1v-5h-1v-1h1v-1h2v-1h1v-1h1V9h-1V6h-2v1h-1v1h-1V7h-4v1H9V7H8V6H6v3H5v5h1v1h1v1h2v2H7v-1H6v-1H4v1h1v2h1v1h3v3H8v-1H6v-1H5v-1H4v-1H3v-2H2v-2H1V9h1V7h1V5h1V4h1V3h2V2h2V1h6v1h2v1h2v1h1v1h1v2h1v2z"/></svg>
            </NuxtLink>
        </div>
    </div>
</template>
<script setup>
import Logo from '@/components/Logo.vue'
</script>