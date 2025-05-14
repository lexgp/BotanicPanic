<script setup lang="ts">
  import { requiredValidator } from '@/@core/utils/validators';
import { useApi } from '@/composables/useApi';
import { useUserStore } from "@/store";
import errors from '@/utils/errors';
import { toast } from 'vue3-toastify';
import { VForm } from 'vuetify/components/VForm';

  const $store = useUserStore()
  const $api = useApi()
  const $route = useRoute()
  const isProcessing = ref(false)
  const form = ref({
    email: '',
    password: ''
  })

  const refLoginForm = ref<VForm>()

  const tryLogin = async () => {
    refLoginForm.value?.validate()
      .then(async ({ valid: isValid }) => {
        if (isValid) {
          isProcessing.value = true
          localStorage.setItem('token', '');
          await $api.post('/auth/login/', form.value )
            .then((response: any) => {
              localStorage.setItem('token', response.data.token)
            })
            .catch((error) => {
              isProcessing.value = false
              toast.error("Не удалось авторизоваться с данными логином и паролем. " + errors.getErrorText(error), {
                autoClose: 8000,
              })
            })
            await $store.loginByToken()
            if ($store.$state.account) {
              toast.success("Добро пожаловать.", {
                autoClose: 8000,
              })
            }
            isProcessing.value = false
        }
      })
  }

const isPasswordVisible = ref(false)
</script>

<template>

  <VMenu
    width="280"
    location="bottom end"
    offset="14px"
    :close-on-content-click="false"
  >
    <template v-slot:activator="{ props }">
      <VBtn
        :variant="$vuetify.display.xs ? 'tonal' : 'elevated'"
        v-bind="props"
        prepend-icon="ri-user-fill"
        class="ml-1"
        :class="$vuetify.display.xs ? 'pl-3 pr-4 py-2' : ''"
        :size="$vuetify.display.xs ? 'sm' : 'default'"
      >
        Личный кабинет
      </VBtn>

    </template>
    <VList>
      <VListItem>

        <VForm class="mt-4" ref="refLoginForm" @submit.prevent="() => tryLogin()">
          <VRow>
            <VCol cols="12">
              <VTextField
                v-model="form.email"
                label="Email"
                type="email"
                size="sm"
                :rules="[requiredValidator]"
              />
            </VCol>

            <VCol cols="12">
              <VTextField
                v-model="form.password"
                label="Password"
                placeholder="············"
                :type="isPasswordVisible ? 'text' : 'password'"
                autocomplete="password"
                :append-inner-icon="isPasswordVisible ? 'ri-eye-off-line' : 'ri-eye-line'"
                @click:append-inner="isPasswordVisible = !isPasswordVisible"
                size="small"
                :rules="[requiredValidator]"
              />
            </VCol>

            <VCol cols="12">
              <VBtn
                block
                type="submit"
                style="text-transform: none;"
                :loading="isProcessing"
                :disabled="isProcessing"
              >
                Войти в Личный кабинет
              </VBtn>
            </VCol>

          </VRow>
        </VForm>
      </VListItem>
    </VList>
  </VMenu>



</template>
