<script setup lang="ts">
import AbountExamples from '@/views/pages/help-center/AbountExamples.vue';
import AppSearchHeader from '@/views/pages/help-center/AppSearchHeader.vue';
import CompanyAbount from '@/views/pages/help-center/CompanyAbount.vue';
import ProjectStages from '@/views/pages/help-center/ProjectStages.vue';

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

    <div class="help-center-section">
      <VContainer>
        <h4 class="text-h4 text-center font-weight-semibold mb-6">
          Результаты исследований загруженных фотографий
        </h4>
        <AbountExamples />
      </VContainer>
    </div>

    <div class="help-center-section bg-surface">
      <VContainer>
        <h4 id="about-company" class="text-h4 text-center font-weight-semibold mb-6">
          О команде
        </h4>
        <CompanyAbount />
      </VContainer>
    </div>

    <div class="help-center-section">
      <VContainer>
        <h4 id="project-stages" class="text-h4 text-center font-weight-semibold mb-6">
          Этапы проекта
        </h4>
        <ProjectStages />
      </VContainer>
    </div>

    
  </div>

</template>

<style>
.v-btn {
  text-transform: none;
}
</style>
