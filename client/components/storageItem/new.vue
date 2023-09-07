<template>
  <q-card class="q-pa-md">
    <div class="column q-gutter-md">
        <div class="row justify-between q-gutter-sm">
            <p class="col-auto text-h6">
                Добавить предмет:
            </p>
            <div class="col">
                <q-btn size="md" class="align-right" v-close-popup icon="close" />
            </div>
        </div>
      <q-input filled v-model="storageItem.name" placeholder="Название прeдмета"/>
        <CategoryList v-model="storageItem.categories"/>
      <q-btn icon="save" @click="saveNew" :class="edited"/>
    </div>
  </q-card>
</template>

<script setup>
import { apiFetch } from "~/utils/apiFetch";
const selectedCategories = ref([])
const storageItem = ref({
  name: '',
  categories: []
});
const edited = ref('bg-white')

function saveNew() {
  apiFetch("/storage_items", {
    method: "POST",
    body: JSON.stringify(storageItem.value)
  })
    .then((response) => {
        response.json()
            .then((data) => {
                edited.value = 'bg-green-3'
            });
    });
    window.location.reload();
}
</script>
