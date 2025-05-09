<script setup lang="ts">
import UploadPhotoArea from '@/components/common/UploadPhotoArea.vue';
import emptyProfilePhoto from '@images/pages/microscope.png';

</script>

<template>
  <VForm action="/search" class="form-search-service" method="GET">
    <VRow>
      <VCol cols="12" class="text-center">
        
        <UploadPhotoArea style="max-width: 600px;"
          :api="'/api/predict/'"
          :api-props="{}"
          :default-url="emptyProfilePhoto"
          label="Загрузить фото для тестирования:"
          class="mx-auto"
          @finish="$emit('finish', $event)"
        />
      </VCol>
    </VRow>
  </VForm>
</template>

<style>
  .form-search-service .v-field__field {
    border-radius: 6px;
    border: solid 1px #8c57ff;
    background-color: white !important;
  }
</style>
