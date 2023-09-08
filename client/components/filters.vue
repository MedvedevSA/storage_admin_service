<template>
  <div class="flex column shadow-2 q-pa-sm q-ma-sm">
    <p class="text-h5">
        Фильтры:
    </p>
    <CategoryList v-model="categories" />
    <q-btn 
        @click="$emit('onApply', prepareFilters())"
        color="secondary"
        class="q-ma-sm secondary"
    >
        Применить
    </q-btn >
  </div>
</template>

<script setup>
const categories = ref([])

function prepareFilters(){
    return {
        categories: categories.value
    }
}

</script>

