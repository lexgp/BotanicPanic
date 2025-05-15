<template>
  <v-timeline align="start" :side="$vuetify.display.smAndDown ? 'end' : undefined">
    <v-timeline-item
      v-for="(timelineItem, i) in timelineItems"
      :key="i"
      :dot-color="timelineItem.color"
      size="small"
      :icon="timelineItem.icon"
      fill-dot
    >
      <template v-slot:opposite>
        <div
          :class="`pt-1 headline font-weight-bold text-${timelineItem.color}`"
          v-text="timelineItem.status"
        ></div>
      </template>
      <div :class="{'text-right': i % 2 && !$vuetify.display.smAndDown}">
        <h2 :class="`mt-n1 headline font-weight-light mb-4 text-${timelineItem.color}`">
          {{ timelineItem.title }}
        </h2>
        <div>
          {{ timelineItem.description }}
        </div>
      </div>
    </v-timeline-item>
  </v-timeline>
</template>

<script setup lang="ts">
  const timelineItems = ref([{
    color: 'success',
    icon: 'ri-check-double-line',
    status: 'Завершено',
    title: 'CustDev',
    description: 'Общение с потенциальными клиентами, сбор требований',
  },
  {
    color: 'success',
    icon: 'ri-check-double-line',
    status: 'Завершено',
    title: 'Онлайн-прототип',
    description: 'Анализатор заболеваний на основе сторонних нейросетей',
  },
  {
    color: 'info',
    icon: 'ri-loader-4-line',
    status: 'Лето 2025',
    title: 'Автономный модуль',
    description: 'Подключение к анализатору заболеваний',
  },
  {
    color: 'warning',
    icon: 'ri-time-line',
    status: 'Осень 2025',
    title: 'Испытания',
    description: 'Установка на объекте, тестирование',
  },
  {
    color: 'primary',
    icon: 'ri-brain-line',
    status: 'Зима 2025',
    title: 'Собственная модель',
    description: 'Завершение обучения и интеграция модели',
  },
  {
    color: 'primary',
    icon: 'ri-tools-line',
    status: 'Зима/весна 2026',
    title: 'Конструкционные правки',
    description: 'Обновление модуля мониторинга',
  },
  {
    color: 'primary',
    icon: 'ri-cpu-line',
    status: 'Весна 2026',
    title: 'Пробная партия',
    description: 'Сборка устройств',
  },
  {
    color: 'primary',
    icon: 'ri-map-pin-line',
    status: 'Весна/лето 2026',
    title: 'Развёртывание',
    description: 'Установка на объектах партнёров'
  },
  {
    color: 'secondary',
    icon: 'ri-line-chart-line',
    status: 'До конца 2026',
    title: 'Анализ результатов',
    description: 'Длительный сбор данных, подготовка к следующему этапу'
  }
])
</script>
