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
  // const isOpen = ref(false)
  const isProcessing = ref(false)
  const form = ref({
    email: '',
    password: ''
  })

  const refLoginForm = ref<VForm>()
  const currentRouteName = computed(() => $route.name)

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
  
  // watch(() => currentRouteName.value, () => {
  //   isOpen.value = false
  // })

  onMounted(async () => {
    // document.addEventListener('click', (e: any) => {
    //   const target = e.target as HTMLElement
    //   if (!target.closest('#header-mini-login')) {
    //     isOpen.value = false
    //   }
    // })
  })

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
      <!-- v-if="$vuetify.display.lgAndUp" -->
      <VBtn
        :variant="$vuetify.display.xs ? 'tonal' : 'elevated'"
        v-bind="props"
        prepend-icon="ri-user-fill"
        class="ml-1"
        :class="$vuetify.display.xs ? 'pl-3 pr-4 py-2' : ''"
        :size="$vuetify.display.xs ? 'sm' : 'default'"
      >
      <!-- color="white" -->
        Личный кабинет
      </VBtn>

      <!-- <VBtn
        v-else
        rounded
        icon
        variant="elevated"
        color="primary"
        v-bind="props"
      >
        <VIcon icon="ri-user-fill" />
      </VBtn> -->

      <!-- <VBtn
        v-if="$vuetify.display.lgAndUp"
        variant="elevated"
        color="success"
        prepend-icon="ri-account-box-fill"
        to="/register"
      >
        Регистрация
      </VBtn> -->

    </template>
    <VList>
      <!-- 👉 User Avatar & Name -->
      <VListItem>
        

        <!-- <h5 class="text-h5 mb-2 text-center">
          Войти в личный кабинет
        </h5> -->

        <VForm class="mt-4" ref="refLoginForm" @submit.prevent="() => tryLogin()">
          <VRow>
            <!-- email -->
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

            <!-- <VCol
              cols="12"
              class="d-flex align-center"
            >
              <VDivider />
              <span class="mx-2">или</span>
              <VDivider />
            </VCol>

            <VCol
              cols="12"
              class="text-center text-base"
            >
              <RouterLink
                class="text-primary ms-2"
                to="/register"
              >
                Создать новый аккаунт
              </RouterLink>
            </VCol> -->
          </VRow>
        </VForm>
      </VListItem>
    </VList>
  </VMenu>



</template>
