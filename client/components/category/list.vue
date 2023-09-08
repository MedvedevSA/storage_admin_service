<template>
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
            v-if="! props.editDisabled"
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
          v-model="selectedCategories"
          :val="category.id"
          :label="category.name"
        />
        <q-btn-dropdown v-if="! props.editDisabled">
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

const props = defineProps(['modelValue', 'editDisabled'])
const emit = defineEmits(['update:modelValue'])

const selectedCategories = computed({
  get() {
    return props.modelValue 
  },
  set(value) {
    emit('update:modelValue', value)
  }
})


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
    });
  });
}

loadCategories();
</script>
