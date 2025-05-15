<script setup lang="ts">
import { useApi } from '@/composables/useApi';

const $api = useApi()

  const predictsList = ref<Array<any>|null>(null)

  const loadPredicts = () => {
    $api.get('/api/predictions/')
      .then(response => {
        predictsList.value = response.data
      })
  }

  onMounted(() => loadPredicts())

</script>

<template>
  <v-container class="py-6">
    <h2 class="text-h5 mb-4">📸 Примеры анализов</h2>
    <v-row v-if="predictsList" dense>
      <v-col
        v-for="(predict, index) in predictsList"
        :key="predict.id"
        cols="12"
        sm="4"
        md="3"
      >
        <v-card class="rounded-lg elevation-2" outlined>
          <v-img
            :src="predict.marked_photo"
            width="100%"
            aspect-ratio="1"
            cover
            class="rounded-t-lg"
          />
          <v-card-text class="pa-2">
            <div class="text-subtitle-2 font-weight-medium">
              {{ (predict.avg_confidence * 100).toFixed(0) }}%
            </div>
            <div class="text-caption text-grey-darken-1" style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
              {{ predict.opinions.map((op: any) => op.disease).join(", ") }}
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
