<script setup lang="ts">

import { useApi } from '@/composables/useApi';
import footerLightBg from '@images/front-pages/backgrounds/footer-bg-light.png';

const $api = useApi()
const pagesPragments = ref<any>({
  FooterSignature: { title: '', content: '' },
})

interface Menu {
  title: string
  path: string
}

const pagesList: Menu[] = [
{
  title: 'Распознать заболевание',
    path: '/'
  },
]

const demoList = [
  {
    title: 'О компании',
    path: '/',
  },
]

onMounted(() => {
})

</script>

<template>
  <div class="footer">
    <div
      class="footer-top pt-11"
      :style="{ 'background-image': `url(${footerLightBg})` }"
    >
      <VContainer>
        <VRow>
          <!-- 👉 Footer  -->
          <VCol
            cols="12"
            md="5"
          >
            <div
              class="mb-4"
              :class="$vuetify.display.smAndDown ? 'w-100 text-center' : 'w-75'"
            >
              <div class="app-logo mb-6">
                <h3 class="app-logo-title text-white">
                  {{ pagesPragments.FooterSignature.title }}
                </h3>
              </div>

              <div
                class="mb-6"
                :class="$vuetify.theme.current.dark ? 'text-body-1' : 'text-white-variant'"
              >
                {{ pagesPragments.FooterSignature.content }}
              </div>
              <div class="align-center">
                <div class="text-body-1 text-white-variant text-wrap me-4">
                  BotanicPanic МФТИ
                  &copy;
                  {{ new Date().getFullYear() }}
                </div>

              </div>
            </div>
          </VCol>

          <VCol
            md="2"
            sm="4"
            xs="6"
          >
            <div class="footer-links">
              <h6 class="footer-title text-h6 mb-6 text-secondary">
                Информация:
              </h6>
              <ul style="list-style: none;">
                <li
                  v-for="(item, index) in demoList"
                  :key="index"
                  class="mb-4"
                >
                  <a
                    :href="item.path"
                    target="_blank"
                    rel="noopener noreferrer"
                    :class="$vuetify.theme.current.dark ? 'text-body-1' : 'text-white-variant'"
                  >
                    {{ item.title }}
                  </a>
                </li>
              </ul>
            </div>
          </VCol>

          <!-- 👉 Pages  -->
          <VCol
            md="2"
            sm="4"
            xs="6"
          >
            <div class="footer-links">
              <h6 class="footer-title text-h6 mb-6 text-secondary">
                Разделы сайта:
              </h6>
              <ul style="list-style: none;">
                <li
                  v-for="(item, index) in pagesList"
                  :key="index"
                  class="mb-4"
                >
                  <RouterLink
                    :class="$vuetify.theme.current.dark ? 'text-body-1' : 'text-white-variant'"
                    class="me-2"
                    :to="item.path"
                  >
                    {{ item.title }}
                  </RouterLink>
                </li>
              </ul>
            </div>
          </VCol>

          <!-- 👉 Download App -->
          <VCol
            cols="12"
            md="3"
            sm="4"
          >
            <div>
              <h6 class="footer-title text-h6 mb-6 text-secondary">
                Социальные сети:
              </h6>

              <div class="d-flex gap-x-6">
                <template
                  v-for="(item, index) in [
                    { title: 'Telegram', icon: 'ri-telegram-fill', href: 'https://t.me/lexgp1' },
                  ]"
                  :key="index"
                >
                  <a
                    :href="item.href"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    <VIcon
                      :icon="item.icon"
                      size="32"
                      color="white"
                    />
                  </a>
                </template>
              </div>
            </div>
          </VCol>
        </VRow>
      </VContainer>
    </div>

  </div>
</template>

<style lang="scss" scoped>
.footer-title {
  color: rgba(255, 255, 255, 92%);
}

.footer-top {
  border-radius: 60px 60px 0 0;
  background-size: cover;
  color: #fff;
}

.footer-links {
  .text-white-variant,
  .text-body-1 {
    &:hover {
      color: #fff;
    }
  }
}

.footer-line {
  background: #282c3e;
}
</style>

<style lang="scss">
.subscribe-form {
  .v-label {
    color: rgba(225, 222, 245, 90%) !important;
  }

  .v-field {
    border-end-end-radius: 0;
    border-end-start-radius: 10px;
    border-start-end-radius: 0;
    border-start-start-radius: 10px;

    input.v-field__input::placeholder {
      color: rgba(225, 222, 245, 40%) !important;
    }

    input.v-field__input {
      color: rgba(255, 255, 255, 78%);
    }
  }
}

.footer {
  border-radius: 50%;

  @media (min-width: 600px) and (max-width: 960px) {
    .v-container {
      padding-inline: 2rem !important;
    }

    .footer-logo-buttons {
      gap: 0.75rem;
    }
  }
}
</style>
