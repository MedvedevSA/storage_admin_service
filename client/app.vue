<template>
    <div class="column flex bg-indigo-1 screen">
      <div class="flex row justify-center q-pa-sm q-mb-sm q-gutter-md text-h5 shadow-2 bg-indigo-2 shadow-3">
          <NuxtLink to="/" class="">
            Хранение
          </NuxtLink>
          <NuxtLink to="/journal" class="n-link-base">
            Журнал
          </NuxtLink>
      </div>
      <div class="flex row justify-center ">
        <div class="col-9 bg-white q-pa-md ">
          <NuxtPage/>
        </div>
      </div>
    </div>
</template>

<style scoped>
.screen{
  min-height: 100vh;
}
</style>