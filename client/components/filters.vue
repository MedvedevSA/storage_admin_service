<template>
  <div class="flex column shadow-2 q-pa-sm q-ma-sm">
    <p class="text-h6">Фильтры:</p>
    <div class="q-ma-sm">
      <div class="row">
        <p class="col text-h7 q-pa-sm">Категории:</p>
        <q-btn
          class="q-ma-sm bg-primary text-white"
          size="sm"
          icon="add"
        >
        </q-btn>
      </div>

      <div class="row" v-for="category in categories" :key="category.name">
        <q-checkbox
          class="col"
          v-model="category.chBox"
          :label="category.name"
        />
        <q-btn
          round
          icon="edit"
          size="md"
          class=""
          @click="editCategoryId = category.id"
        />

        <q-dialog v-model="editClicked">
            <EditCategory :category="category"/>
        </q-dialog>
      </div>

    </div>
  </div>
</template>

<script setup>
import { apiFetch } from "~/utils/apiFetch";
const categories = ref([]);
const editCategoryId = ref(null);

const editClicked = computed({
    get() {
        return Boolean(editCategoryId.value);
    },
    set(newVal) {
        window.location.reload();
        editCategoryId.value = null
    }
});

function loadCategories(){
    apiFetch("/category").then((response) => {
    response.json().then((data) => {
        categories.value = data;
        categories.value.forEach((el) => (el.chBox = false));
    });
    });
}

loadCategories()
</script>
