<template>
  <q-card class="q-pa-md">
    <div class="row">
      <q-btn class="self-end" flat v-close-popup round dense icon="close" />
      <q-input v-model="category.name" />
      <q-btn icon="save" @click="saveEdited"/>
    </div>
  </q-card>
</template>

<script setup>
import { apiFetch } from "~/utils/apiFetch";
const props = defineProps(["category"]);
const category = ref(Object.assign({}, props.category));

function saveEdited() {
  console.log(JSON.stringify(category.value))
  apiFetch("/category/" + category.value.id, {
    method: "PUT",
    body: JSON.stringify(category.value)
  })
    .then((response) => {
        response.json()
            .then((data) => {
                console.log(data)
            });
    });
}
</script>
