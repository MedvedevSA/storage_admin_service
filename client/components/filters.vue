<template>
  <div class="flex column shadow-2 q-pa-sm q-ma-sm">
    <p class="text-h5">Фильтры:</p>
    <div class="q-pl-sm">
      <div class="">
        <p class="text-h6">
          Категории:
          <q-btn
            round
            class="q-ma-sm bg-primary text-white"
            size="md"
            icon="add"
            @click="createClicked = true"
          />
          <q-dialog v-model="createClicked">
            <CategoryNew />
          </q-dialog>
        </p>
      </div>

      <div
        class="row q-ma-sm"
        v-for="category in categories"
        :key="category.name"
      >
        <q-checkbox
          class="col"
          v-model="category.chBox"
          :label="category.name"
        />
        <q-btn-dropdown>
            <q-btn
                round
                icon="edit"
                size="md"
                class="q-ma-sm bg-green-2"
                @click="editCategory = category"
            />
            <q-btn
                round
                icon="delete"
                size="md"
                class="q-ma-sm bg-red-3"
                @click="deleteCategory(category.id)"
            />
        </q-btn-dropdown>

        <q-dialog v-model="editClicked">
          <CategoryEdit :category="editCategory"/>
        </q-dialog>
      </div>
    </div>
  </div>
</template>

<script setup>
import { apiFetch } from "~/utils/apiFetch";
const categories = ref([]);
const editCategory = ref(null);

const createClicked = ref(false);
const editClicked = computed({
  get() {
    return Boolean(editCategory.value);
  },
  set(newVal) {
    window.location.reload();
    editCategory.value = null;
  },
});

function deleteCategory(id) {
  apiFetch("/category/" + id, {
    method: "DELETE",
  }).then((response) => {
    response.json().then((data) => {
      console.log("category id:", id, " deleted");
    });
  });
  window.location.reload();
}

function loadCategories() {
  apiFetch("/category").then((response) => {
    response.json().then((data) => {
      categories.value = data;
      categories.value.forEach((el) => (el.chBox = false));
    });
  });
}

loadCategories();
</script>
