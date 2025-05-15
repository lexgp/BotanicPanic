<script lang="ts">
import { useApi } from '@/composables/useApi';
import errors from '@/utils/errors';
import { defineComponent } from "vue";
import { toast } from 'vue3-toastify';

const $api = useApi()

export default defineComponent({
  props: {
    id: { type: Number, default: null },
    label: { type: String, default: 'Загрузить фото:' },
    url: { type: String, default: null },
    api: { type: String, required: true },
    apiProps: { type: Object, required: true },
    isContain: { type: Boolean, default: false },
    acceptMediaTypes: { type: String, default: '*' },
    defaultUrl: { type: String, default: '' },
    disabled: { type: Boolean, default: false },
  },
  data() {
    return {
      is_dragover: false,
      is_processing: false,
      progress: 0,
      interval: null as ReturnType<typeof setInterval> | null,
    }
  },
  methods: {
    handleUpload(e : Event) {
      this.is_dragover = false;
      this.is_processing = true;
      this.simulateProgress();

      const fileInput: HTMLInputElement = e.target as HTMLInputElement;
      const files = fileInput.files;

      if (files && files.length) {
        const selectedFile = files[0]
        const formData = new FormData()
        formData.append('file', selectedFile)
        for(var key in this.apiProps) {
          if (this.apiProps[key]) {
            formData.append(key, this.apiProps[key])
          }
        }

        const headers = { headers: { 'Content-Type': 'multipart/form-data' } };

        $api.post(this.api, formData, headers)
          .then((response : any) => {
            this.stopProgress();
            this.$emit('finish', response.data);
          })
          .catch((error : any) => {
            this.stopProgress();
            toast.error("Не удалось загрузить фото. " + errors.getErrorText(error), { autoClose: 8000 });
          })
      }
    },
    simulateProgress() {
      this.progress = 0;
      this.interval = setInterval(() => {
        if (this.progress < 80) {
          this.progress += 2;
        } else if (this.progress < 99) {
          this.progress += 0.1;
        }
      }, 250);
    },
    stopProgress() {
      this.is_processing = false;
      if (this.interval) clearInterval(this.interval);
      this.progress = 100;
    },
    clickOnFile() {
      const fileInput = this.$refs.file as HTMLElement
      fileInput.click()
    },
    onDrop(e: DragEvent) {
      e.preventDefault();
      if (e.dataTransfer?.files.length) {
        const fakeEvent = { target: { files: e.dataTransfer.files } } as unknown as Event;
        this.handleUpload(fakeEvent);
      }
    },
  },
})
</script>

<template>
  <div
    class="upload-area d-flex flex-column align-center justify-center text-center rounded-lg pa-6"
    :class="{ 'drag-over': is_dragover }"
    @dragover.prevent="is_dragover = true"
    @dragleave.prevent="is_dragover = false"
    @drop="onDrop"
  >
    <h4 v-if="label" class="text-h6 mt-3">{{ label }}</h4>
    <VAvatar v-if="defaultUrl"
      rounded="lg"
      size="100"
      class="me-6 my-4"
      :image="defaultUrl"
    />
    <VIcon v-else size="48" color="primary" icon="ri-upload-cloud-2-line" />

    <p v-if="!is_processing" class="text-body-2 mb-4">Перетащите фото сюда или нажмите кнопку ниже</p>

    <input
      ref="file"
      type="file"
      hidden
      :accept="acceptMediaTypes"
      @change="handleUpload"
    />

    <VBtn
      v-if="!is_processing"
      color="primary"
      :disabled="disabled"
      @click="clickOnFile"
    >
      Загрузить фотографию...
    </VBtn>

    <VProgressCircular
      v-if="is_processing"
      :model-value="progress"
      color="primary"
      size="120"
      width="6"
      class="mt-6"
    >
      {{ Math.round(progress) }}%
    </VProgressCircular>

  </div>
</template>

<style scoped>
.upload-area {
  border: 2px dashed #888;
  background-color: rgba(124, 124, 124, 0.15);
  transition: background-color 0.2s;
  min-height: 240px;
  cursor: pointer;
}
.drag-over {
  background-color: rgba(255, 255, 255, 0.3);
  border-color: #5e9bff;
}
</style>
