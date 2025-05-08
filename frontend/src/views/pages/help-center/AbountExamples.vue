<script setup lang="ts">

import examplePhoto2 from '@images/examples/047c4fba0f7b4123965e52de5fdd4997_predicted.jpg';
import examplePhoto1 from '@images/examples/3bf990c21f9e48bbad61a56fbaac869a_predicted.jpg';
import examplePhoto3 from '@images/examples/a6d4523b99ba4945aa6c7a8cbe5ac753_predicted.jpg';
import examplePhoto4 from '@images/examples/c6f7633fc44d45fcaac25adaf5d9c545_predicted.jpg';
import examplePhoto5 from '@images/examples/cdc8ba1dc4d745bab29bd9299ee4c303_predicted.jpg';

  const exampleImages = ref([
    examplePhoto1,
    examplePhoto2,
    examplePhoto3,
    examplePhoto4,
    examplePhoto5
  ])

</script>

<template>
  <v-container class="py-6">
    <h2 class="text-h5 mb-4">📸 Примеры анализов</h2>
    <v-row dense>
      <v-col
        v-for="(image, index) in exampleImages"
        :key="index"
        cols="12"
        sm="4"
        md="2"
      >
        <v-img
          :src="image"
          width="100%"
          aspect-ratio="1"
          cover
          class="rounded-lg elevation-2"
        />
      </v-col>
    </v-row>
  </v-container>
</template>
