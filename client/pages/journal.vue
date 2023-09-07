<template>
  <div class="q-pa-md">
    <q-table
      flat bordered
      title="Журнал"
      :rows="rows"
      :columns="columns"
      row-key="name"
    >

      <template v-slot:header="props">
        <q-tr :props="props">
          <q-th auto-width />
          <q-th
            v-for="col in props.cols"
            :key="col.name"
            :props="props"
          >
            {{ col.label }}
          </q-th>
        </q-tr>
      </template>

      <template v-slot:body="props">
        <q-tr :props="props">
          <q-td>
            <q-btn size="sm" color="accent" round dense @click="props.row.expand = !props.row.expand" :icon="props.row.expand ? 'remove' : 'add'" />
          </q-td>
          <q-td
            v-for="col in props.cols"
            :key="col.name"
            :props="props"
          >
            {{ col.value }}
          </q-td>
        </q-tr>
        <q-tr v-show="props.row.expand" :props="props">
          <q-td colspan="100%">
            <div class="text-left">method: {{ props.row.data.method }}.</div>
            <div class="text-left">url: {{ props.row.data.path }}.</div>
            <div class="text-left">url params: {{ props.row.data.path_params }}.</div>
            <div class="text-left">body: {{ props.row.data.body }}.</div>
          </q-td>
        </q-tr>
      </template>

    </q-table>
  </div>
</template>

<script setup>
const columns = ref([
  { name: 'id', label: '#', field: 'id', sortable: true },
  { name: 'client_ip', label: 'IP', field: 'client_ip', sortable: true },
  { name: 'time_created', label: 'Время', field: 'time_created', sortable: true, format: (val, row) => ConvertDateTime(val) },
])
const rows = ref([])

apiFetch('/journal_log')
.then(response => {
    response.json().then(data => {
    rows.value = data
    })
})
</script>
