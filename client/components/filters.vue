<template>
    <div class="flex column shadow-2 q-gutter-md q-ma-md">
        <p class="text-h6">
            Фильтры
        </p>
        <q-checkbox v-model="val" label="Foo" />
        <q-checkbox v-model="val" label="Bar" />
        <q-checkbox v-model="val" label="Baz"/>
    </div>
</template>

<script setup>
const val = ref()

</script>