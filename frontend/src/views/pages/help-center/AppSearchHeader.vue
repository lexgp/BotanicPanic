<script setup lang="ts">
import SearchForm from '@/components/search/SearchForm.vue';
import ShowResult from '@/components/search/ShowResult.vue';
import AppVideoHeaderBg from '@images/videos/top-background-c2.mp4';

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

const backgroundVideoElement = computed(() => {
  return document.querySelector('video#main-video-background') as HTMLVideoElement | null
})

const dashboardHeaderElement = computed(() => {
  return document.querySelector('#dashboard-header') as HTMLHeadingElement | null
})

const uploadAreaElement = computed(() => {
  return document.querySelector('.upload-area') as HTMLDivElement | null
})



const finishSearch = (result: any) => {
  predictionResult.value = result
  backgroundVideoElement.value?.pause()
  dashboardHeaderElement.value?.scrollIntoView({
    behavior: 'smooth',
    block: 'start'
  })
}

const retryAgain = () => {
  predictionResult.value = null
  backgroundVideoElement.value?.play()
  nextTick(() => {
    uploadAreaElement.value?.scrollIntoView({
      behavior: 'smooth',
      block: 'center'
    })
  })
}
</script>

<template>
  <div class="search-header">
    <!-- Видеофон -->
    <video id="main-video-background"
      autoplay
      loop
      muted
      playsinline
      class="video-background"
    >
      <source :src="AppVideoHeaderBg" type="video/mp4" />
    </video>
    
    <div class="overlay-background"></div>
    
    <VCard
      flat
      class="text-center overlay-card"
      :class="props.customClass"
      style="z-index: 2;"
    >
      <VCardText>
        <slot name="title">
          <h4 class="text-h4 mb-2 font-weight-medium">
            {{ props.title }}
          </h4>
        </slot>
        <div v-if="!predictionResult" class="d-flex flex-column">
          <div class="my-4">
            <SearchForm
              :is-show-button="true"
              :is-only-main-search="true"
              @finish="finishSearch"
            />
          </div>

          <p class="mt-4 mb-0">
            {{ props.subtitle }}
          </p>

        </div>
        <ShowResult v-else
          :prediction-result="predictionResult"
          @retry-again="retryAgain"
        />

      </VCardText>
    </VCard>
  </div>
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

.video-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: brightness(0.4) blur(4px);
  z-index: 1;
}

.search-header {
  position: relative;
  overflow: hidden;
}
.overlay-card {
  position: relative;
  z-index: 2;
  background-color: transparent !important;
  backdrop-filter: blur(4px);
}
.overlay-background {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: #28243d99;
  z-index: 1;
}
</style>
