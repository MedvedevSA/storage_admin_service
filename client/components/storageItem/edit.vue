<template>
  <q-card class="q-pa-md">
    <div class="column q-gutter-md">
        <div class="row justify-between q-gutter-sm">
            <p class="col-auto text-h6">
                Измененить предмет:
            </p>
            <div class="col">
                <q-btn size="md" class="align-right" v-close-popup icon="close" />
            </div>
        </div>
      <q-input filled v-model="storageItem.name" placeholder="Название прeдмета"/>
        <CategoryList v-model="storageItem.categories" :edit-disabled="true"/>
      <q-btn icon="save" @click="saveNew" :class="edited"/>
    </div>
  </q-card>
</template>

<script setup>
import { apiFetch } from "~/utils/apiFetch";
const props = defineProps(["storageItem"]);
const storageItem = ref(Object.assign({}, props.storageItem));
const edited = ref('bg-white')

storageItem.value.categories = storageItem.value.categories.map(
  (el) => el.id
)

function saveNew() {
  apiFetch("/storage_items/" + storageItem.value.id, {
    method: "PUT",
    body: JSON.stringify(storageItem.value)
  })
    .then((response) => {
        response.json()
            .then((data) => {
                edited.value = 'bg-green-3'
            });
    });
    // window.location.reload();
}
</script>
