<script setup lang="ts">
import UploadPhotoAWS from '@/components/common/UploadPhotoAWS.vue';
import emptyProfilePhoto from '@images/pages/tree.png';

</script>

<template>
  <VForm action="/search" class="form-search-service" method="GET">
    <VRow>
      <VCol cols="12" class="text-center">
        Загрузить фото для тестирования:

        <UploadPhotoAWS
          :api="'/api/predict/'"
          :api-props="{}"
          :default-url="emptyProfilePhoto"
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
