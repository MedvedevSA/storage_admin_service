
<template>
  <div class="q-pa-md">
    <q-table
      :rows="props.rows"
      :columns="columns"
      row-key="name"
      :filter="filter"
      :pagination="pagination"
      grid
      hide-header
    >

      <template v-slot:top-left>
        <p class="text-h5">
          Предметы:
          <q-btn
            round
            class="q-ma-md bg-primary text-white"
            icon="add"
            @click="newClicked = true"
          />
          <q-dialog v-model="newClicked">
            <StorageItemNew />
          </q-dialog>
        </p>
      </template>

      <template v-slot:top-right>
        <q-input  v-model="filter" placeholder="Поиск">
          <template v-slot:append>
            <q-icon name="search" />
          </template>
        </q-input>
      </template>

      <template v-slot:item="props">
        <div class="q-pa-xs">
          <q-card bordered flat class="flex">
            <q-list>
              <q-card-section class="q-pa-sm row">
              <q-btn-dropdown class="col">
                  <q-btn
                      round
                      icon="edit"
                      size="md"
                      class="q-ma-sm bg-green-2"
                      @click="editStorageItem = props.row"
                  />
                  <q-dialog v-model="editClicked">
                    <StorageItemEdit :storage-item="editStorageItem"/>
                  </q-dialog>
                  <q-btn
                      round
                      icon="delete"
                      size="md"
                      class="q-ma-sm bg-red-3"
                      @click="deleteStorageItem(props.row.id)"
                  />
              </q-btn-dropdown>
              </q-card-section>
              <q-item v-for="col in props.cols" :key="col.name">
                <q-item-section class="row" :class="col.meta ? 'meta':'text-subtitle1' ">

                  <q-item-label caption class="text-caption col">
                    {{ col.label }}
                  </q-item-label>
                  <q-item-label class="col">
                    {{col.value}}
                  </q-item-label>
                </q-item-section>
              </q-item>
              <q-separator/>
              <q-card-section class="q-pa-sm">
                <q-chip size="sm" v-for="category in props.row.categories" :key="category.name">
                  {{ category.name }}
                </q-chip>
              </q-card-section>
            </q-list>

          </q-card>
        </div>
      </template>
    </q-table>
  </div>
</template>

<script setup>
import { ConvertDateTime } from "~/utils/ConvertDateTime"
import { apiFetch } from "~/utils/apiFetch"

const props = defineProps(["rows"])
const newClicked = ref(false)
const selected = ref([])
const filter = ref('')
const columns = ref([
    { name: 'name', label: 'Название', field: 'name' },
    { name: 'time_created', label: 'Создан', field: 'time_created', format: (val, row) => ConvertDateTime(val), meta: true},
    { name: 'time_updated', label: 'Изменен', field: 'time_updated', format: (val, row) => ConvertDateTime(val), meta: true},
])
const pagination = ref({
  page: 1,
  rowsPerPage: 15
})

const editStorageItem = ref(null)
const editClicked = computed({
  get() {
    return Boolean(editStorageItem.value);
  },
  set(newVal) {
    window.location.reload();
    editStorageItem.value = null;
  },
});

function deleteStorageItem(id) {
  apiFetch("/storage_items/" + id, {
    method: "DELETE",
  }).then((response) => {
    response.json().then((data) => {
      console.log("storage item id:", id, " deleted");
    });
  });
  window.location.reload();
}
</script>

<style scoped>
.meta {
  font-size: 8pt;
}
</style>