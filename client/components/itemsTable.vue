
<template>
  <div class="q-pa-md">
    <q-table
      title="Предметы"
      :rows="rows"
      :columns="columns"
      row-key="name"
      :filter="filter"
      :pagination="pagination"
      grid
      hide-header
    >
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
              <q-item v-for="col in props.cols" :key="col.name">
                <q-item-section>
                  <q-item-label caption>
                    {{ col.label }}
                  </q-item-label>
                  <q-item-label class="">
                    {{col.value}}
                  </q-item-label>
                </q-item-section>
              </q-item>
              <q-separator/>
              <q-card-section>
                <q-chip v-for="category in props.row.categories" :key="category.name">
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

const selected = ref([])
const filter = ref('')
const rows = ref([])
const columns = ref([
    { name: 'name', label: 'Название', field: 'name' },
    { name: 'time_created', label: 'Создан', field: 'time_created', format: (val, row) => ConvertDateTime(val)},
    { name: 'time_updated', label: 'Изменен', field: 'time_updated', format: (val, row) => ConvertDateTime(val) },
])
const pagination = ref({
  page: 1,
  rowsPerPage: 15
})

apiFetch('/storage_items')
  .then(response => {
    response.json().then(data => {
      rows.value = data
    })
  })

</script>