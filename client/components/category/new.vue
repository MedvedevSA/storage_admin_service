<template>
  <q-card class="q-pa-md">
    <div class="column q-gutter-md">
        <div class="row justify-between q-gutter-sm">
            <p class="col-auto text-h6">
                Создать категорию:
            </p>
            <div class="col">
                <q-btn size="md" class="align-right" v-close-popup icon="close" />
            </div>
        </div>
      <q-input filled v-model="category.name" placeholder="Название категории"/>
      <q-btn icon="save" @click="saveEdited" :class="edited"/>
    </div>
  </q-card>
</template>

<script setup>
import { apiFetch } from "~/utils/apiFetch";
const category = ref({
  name: '',
  parent_id: null
});
const edited = ref('bg-white')

function saveEdited() {
  apiFetch("/category", {
    method: "POST",
    body: JSON.stringify(category.value)
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
