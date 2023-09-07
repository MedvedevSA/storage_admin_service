<template>
  <div class="row q-gutter-md">
      <div class="col-3">
        <Filters 
          @on-apply="takeFilters"
        />
      </div>
      <div class="col-8">
        <ItemsTable :rows="rows"/>
      </div>
  </div>
</template>

<script setup>
import { apiFetch } from "~/utils/apiFetch"
const rows = ref([])

function takeFilters(filters){
  let params = new URLSearchParams()

  filters.categories.forEach((el) =>{
    params.append("category__id__in", el)
  })
  getStorageItems(params)
}

function getStorageItems(urlParams = null){
  let url = '/storage_items'
  if (urlParams){
    url = url + '?' + urlParams.toString()
    console.log(url)
  }
  apiFetch(url)
    .then(response => {
      response.json().then(data => {
        rows.value = data
      })
    })
}

getStorageItems()

</script>