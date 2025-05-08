<script setup lang="ts">
import SearchForm from '@/components/search/SearchForm.vue';
import ShowResult from '@/components/search/ShowResult.vue';
import AppSearchHeaderBg from '@images/pages/header-bg.png';

interface Props {
  title?: string
  subtitle?: string
  customClass?: string
  placeholder?: string
  density?: 'comfortable' | 'compact' | 'default'
  isReverse?: boolean
}

defineOptions({
  inheritAttrs: false,
})

const predictionResult =ref(null)

const props = withDefaults(defineProps<Props>(), {
  density: 'comfortable',
  isReverse: false,
})

const finishSearch = (result: any) => {
  predictionResult.value = result
}
</script>

<template>
  <!-- 👉 Search Banner  -->
  <VCard
    flat
    class="text-center search-header"
    :class="props.customClass"
    :style="`background: url(${AppSearchHeaderBg});`"
  >
    <VCardText>
      <slot name="title">
        <h4 class="text-h4 mb-2 font-weight-medium" style="color: #5229aa;">
          {{ props.title }}
        </h4>
      </slot>
      <div v-if="!predictionResult"
        class="d-flex"
        :class="isReverse ? 'flex-column' : 'flex-column-reverse' "
      >
        <p class="mb-0">
          {{ props.subtitle }}
        </p>

        <div class="my-4">
          <SearchForm
            :is-show-button="true"
            :is-only-main-search="true"
            @finish="finishSearch"
          />
        </div>
      </div>
      <ShowResult v-else
        :prediction-result="predictionResult"
        @retry-again="predictionResult=null"
      />

    </VCardText>
  </VCard>
</template>

<style lang="scss">
.search-header {
  padding: 4rem !important;
  background-size: cover !important;
}

// search input
.search-header-input {
  border-radius: 0.375rem !important;
  background-color: rgb(var(--v-theme-surface));
  max-inline-size: 28.125rem !important;
}

@media (max-width: 37.5rem) {
  .search-header {
    padding: 1.5rem !important;
  }
}
</style>
