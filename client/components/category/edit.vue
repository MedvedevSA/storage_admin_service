<template>
  <q-card class="q-pa-md">
    <div class="column q-gutter-md">
        <div class="row justify-between q-gutter-sm">
            <p class="col-auto text-h6">
                Изменить категорию:
            </p>
            <div class="col">
                <q-btn size="md" class="align-right" v-close-popup icon="close" />
            </div>
        </div>
      <q-input filled v-model="category.name" @focus="edited='bg-yellow-2'"/>
      <q-btn icon="save" @click="saveEdited" :class="edited"/>
    </div>
  </q-card>
</template>

<script setup>
import { apiFetch } from "~/utils/apiFetch";
const props = defineProps(["category"]);
const category = ref(Object.assign({}, props.category));
const edited = ref('bg-white')

function saveEdited() {
  console.log(JSON.stringify(category.value))
  apiFetch("/category/" + category.value.id, {
    method: "PUT",
    body: JSON.stringify(category.value)
  })
    .then((response) => {
        response.json()
            .then((data) => {
                edited.value = 'bg-green-3'
            });
    });
}
</script>
