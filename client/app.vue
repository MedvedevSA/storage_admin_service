<template>
    <div class="column">
      <div class="row justify-center q-pa-md q-gutter-md text-h5">
          <NuxtLink to="/" class="">
            Хранение
          </NuxtLink>
          <NuxtLink to="/categories" class="n-link-base">
            Категории
          </NuxtLink>
          <NuxtLink to="/journal" class="n-link-base">
            Журнал
          </NuxtLink>
      </div>
      <div class="flex row justify-center">
        <div class="col-8">
          <NuxtPage/>
        </div>
      </div>
    </div>
</template>
