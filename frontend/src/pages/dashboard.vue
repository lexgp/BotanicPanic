<script setup lang="ts">
import AbountExamples from '@/views/pages/help-center/AbountExamples.vue';
import AppSearchHeader from '@/views/pages/help-center/AppSearchHeader.vue';
import HowHelpAbount from '@/views/pages/help-center/HowHelpAbount.vue';

const pagesPragments = ref<any>({
  MainSlogan: { title: '', content: '' },
  MainCard1: { title: '', content: '' },
  MainCard2: { title: '', content: '' },
  MainCard3: { title: '', content: '' },
  MainHowHelp: { title: '', content: '' },
  MainHowHelpLidogenerator: {
    title: '🧠 Запустили сервис распознавания болезней растений',
    content: `Изображения анализируются тремя ИИ-моделями: Gemini 2.5, GPT 4.1 nano и LLama 4.
    Все вместе выдают консолидированное решение.
    Испытать можно прямо на сайте`
  },
  MainHowHelpBonus: {
    title: '🌿 В разработке — автономное устройство мониторинга',
    content: 'Планируем компактный гаджет с камерой и ИИ, который сам следит за растениями и сообщает о признаках болезней прямо в приложение.'
  },
  MainHowHelpReferral: { title: '', content: '' },
  MainHowButtonStart: { title: '', content: '' },
})

</script>

<template>
  <div>
    <AppSearchHeader
      subtitle="Онлайн-анализ изображений растений на наличие заболеваний."
      custom-class="rounded-0"
      placeholder="Search"
    >
      <template #title>
        <h4 id="dashboard-header"
          class="text-h4 text-dark-primary mb-4"
          style="color: var(--v-theme-on-surface); z-index: 1; position: relative; font-weight: 700;"
        >
        Система мониторинга болезней растений
        </h4>
      </template>
    </AppSearchHeader>

    <div class="help-center-section bg-surface">
      <VContainer>
        <h4 class="text-h4 font-weight-semibold mb-6">
          Состояние проекта
        </h4>
        <HowHelpAbount :pages-pragments="pagesPragments" />
      </VContainer>
    </div>

    <div class="help-center-section">
      <VContainer>
        <h4 class="text-h4 font-weight-semibold mb-6">
          Результаты анализа
        </h4>
        <AbountExamples :pages-pragments="pagesPragments" />
      </VContainer>
    </div>
  </div>

</template>

<style>
.v-btn {
  text-transform: none;
}
</style>
