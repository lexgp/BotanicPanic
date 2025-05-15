<template>
  <v-container class="py-6">
    <v-row>
      <v-col cols="12" md="6">
        <v-img :src="predictionResult.received_photo" aspect-ratio="1" contains class="rounded-lg mb-2"
          style="max-height: 50vh;"
        />
        <div class="text-caption text-center">Загруженное фото</div>
      </v-col>
      <v-col cols="12" md="6">
        <v-img :src="predictionResult.marked_photo" aspect-ratio="1" contains class="rounded-lg mb-2"
          style="max-height: 50vh;"
        />
        <div class="text-caption text-center">Результат с разметкой</div>
      </v-col>
    </v-row>

    <v-divider class="my-6" />

    <div class="text-h6 mb-4">Вероятность заражения:</div>
    <div class="text-h5 font-weight-bold" :style="{ color: confidenceColor }">
      {{ Math.round(predictionResult.avg_confidence * 100) }}%
    </div>

    <div class="mt-6">
      <div
        v-for="(opinion, index) in predictionResult.opinions"
        :key="index"
        class="mb-4"
      >
        <div class="d-flex justify-space-between mb-1">
          <span class="font-weight-medium">{{ opinion.disease }}</span>
          <span>{{ Math.round(opinion.confidence * 100) }}%</span>
        </div>
        <v-progress-linear
          :model-value="opinion.confidence * 100"
          height="16"
          color="primary"
          rounded
        ></v-progress-linear>
        <div class="text-caption mt-1 text-grey-darken-1">Модель: {{ opinion.model_name }}</div>
      </div>
    </div>

    <v-btn class="mt-6" color="primary" variant="tonal"
      @click="$emit('retry-again')"
    >
      Попробовать снова
    </v-btn>
  </v-container>
</template>

<script setup lang="ts">
  const $props = defineProps({
    predictionResult: {
      type: Object,
      required: true
    }
  })

  const confidenceColor = computed(() => {
    if (!$props.predictionResult) {
      return ''
    }
    if ($props.predictionResult.avg_confidence > 0.8) return 'red';
    if ($props.predictionResult.avg_confidence > 0.5) return 'orange';
    return 'green';
  })
</script>
