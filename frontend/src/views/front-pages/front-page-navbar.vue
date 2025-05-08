<script setup lang="ts">
import { useWindowScroll } from '@vueuse/core';
// import type { RouteLocationRaw } from 'vue-router/auto'
import { useUserStore } from "@/store";
import AccountBlock from '@/views/front-pages/account-block.vue';
import DesktopNavbarLinks from '@/views/front-pages/desktop-navbar-links.vue';
import logolightMobile from '@images/svg/logo-mobile2.svg';
import logolight from '@images/svg/logo.svg';
import { PerfectScrollbar } from 'vue3-perfect-scrollbar';
import { useDisplay } from 'vuetify';


const props = defineProps({
  activeId: String,
})

const $store = useUserStore()
const display = useDisplay()

interface MenuItem {
  listTitle: string
  listIcon?: string
  path?: string
  children?: MenuItem[]
  isDivider?:boolean
}
const { y } = useWindowScroll()

const route = useRoute()
const router = useRouter()

const sidebar = ref(false)

watch(() => display, () => {
  return display.mdAndUp ? sidebar.value = false : sidebar.value
}, { deep: true })

const isMenuOpen = ref(false)
const isMegaMenuOpen = ref(false)

const currentAccount = computed(() => {
  return $store.currentAccount
})

const menuMobileItems = computed(() => {
  const items = [
    {
      listTitle: 'Распознать заболевание',
      path: '/search'
    },
  ] as MenuItem[]
  if (currentAccount.value) {
    items.push(...[
      { listTitle: '', isDivider: true },
      { listTitle: 'Мой аккаунт', path: '/account' },
      { listTitle: 'Мои услуги', path: '/account/services' },
      { listTitle: 'Мои сделки', path: '/account/my-offers' },
      { listTitle: '', isDivider: true },
      { listTitle: 'Реферальная программа', path: '/account/referrals' },
    ])
    if (currentAccount.value.profile.is_partner && currentAccount.value.profile.partner_type) {
      items.push(
        { listTitle: 'Партнёрская программа', path: '/account/partner' },
      )
    }
  }
  items.push(...[
    { listTitle: '', isDivider: true },
    { listTitle: 'Возможности', path: '/' },
    { listTitle: 'О компании', path: '/' },
    { listTitle: 'Правила сайта', path: '/' },
  ])

  return items
})

const menuItems: MenuItem[] = [
  {
    listTitle: 'Распознать заболевание',
    path: '/'
  },
  {
    listTitle: 'Возможности',
    path: '/'
  },
  {
    listTitle: 'Информация',
    children: [
      {
        listTitle: 'О компании',
        listIcon: 'ri-circle-line',
        path: '/about/company',
      },
      {
        listTitle: 'Правила сайта',
        listIcon: 'ri-circle-line',
        path: '/about/rules',
      },
    ]
  },
]

const isCurrentRoute = (to: any) => {
  return route.matched.some(_route => _route.path.startsWith(router.resolve(to).path))

  // ℹ️ Below is much accurate approach if you don't have any nested routes
  // return route.matched.some(_route => _route.path === router.resolve(to).path)
}

// const isPageActive = computed(() => menuItems.some(item => item.navItems.some(listItem => isCurrentRoute(listItem.to))))
</script>

<template>
  <!-- 👉 Navigation drawer for mobile devices  -->
  <VNavigationDrawer
    v-model="sidebar"
    width="275"
    disable-resize-watcher
    class="front-page-navbar"
  >
    <PerfectScrollbar
      :options="{ wheelPropagation: false }"
      class="h-100"
    >
      <!-- Nav items -->
      <div>
        <div class="d-flex flex-column gap-y-4 pa-4">
          <VIcon
                :icon="logolight"
                :size="210"
                style="max-height: 50px;"
              />

          <template v-for="menuItem in menuMobileItems">
            <VDivider v-if="menuItem.isDivider" />
            <RouterLink v-if="menuItem.path"
              :to="menuItem.path"
              class="nav-link font-weight-medium"
            >
              {{ menuItem.listTitle }}
            </RouterLink>
          </template>
            <!-- <template v-else>
              <template v-for="subMenuItem in menuItem.children">
                <RouterLink v-if="subMenuItem.path"
                  :to="subMenuItem.path"
                  class="nav-link font-weight-medium"
                >
                  {{ subMenuItem.listTitle }}
                </RouterLink>
              </template>
            </template> -->
            <!-- :class="[props.activeId?.toLocaleLowerCase().replace('-', ' ') === item.toLocaleLowerCase() ? 'active-link' : '']" -->

            <!-- <div v-if="menuItem.children" class="font-weight-medium cursor-pointer">
              <div
                :class="[isMenuOpen ? 'mb-6 active-link' : '', isPageActive ? 'active-link' : '']"
                style="color: rgba(var(--v-theme-on-surface));"
                class="page-link"
                @click="isMenuOpen = !isMenuOpen"
              >
                {{ menuItem.listTitle }} <VIcon :icon="isMenuOpen ? 'tabler-chevron-up' : 'tabler-chevron-down'" />
              </div>

              <div
                class="px-4"
                :class="isMenuOpen ? 'd-block' : 'd-none'"
              >
                <div
                  v-for="(item, index) in menuItems"
                  :key="index"
                >
                  <div class="d-flex align-center gap-x-3 mb-4">
                    <VAvatar
                      variant="tonal"
                      color="primary"
                      rounded
                      :icon="item.listIcon"
                    />
                    <div class="text-body-1 text-high-emphasis font-weight-medium">
                      {{ item.listTitle }}
                    </div>
                  </div>
                  <ul class="mb-6">
                    <li
                      v-for="listItem in item.navItems"
                      :key="listItem.name"
                      style="list-style: none;"
                      class="text-body-1 mb-4 text-no-wrap"
                    >
                      <RouterLink
                        :to="listItem.to"
                        :target="item.listTitle === 'Page' ? '_self' : '_blank'"
                        class="mega-menu-item"
                        :class="isCurrentRoute(listItem.to) ? 'active-link' : 'text-high-emphasis'"
                      >
                        <VIcon
                          icon="ri-circle-line"
                          :size="10"
                          class="me-2"
                        />
                        <span>  {{ listItem.name }}</span>
                      </RouterLink>
                    </li>
                  </ul>
                </div>
              </div>
            </div> -->
          <!-- </template> -->
        </div>
      </div>

      <!-- Navigation drawer close icon -->
      <VIcon
        id="navigation-drawer-close-btn"
        icon="ri-close-line"
        size="20"
        @click="sidebar = !sidebar"
        style="z-index: 100;"
      />
    </PerfectScrollbar>
  </VNavigationDrawer>

  <!-- 👉 Navbar for desktop devices  -->
  <div class="front-page-navbar">
    <div class="front-page-navbar">
      <VAppBar
        :color="$vuetify.theme.current.dark ? 'rgba(var(--v-theme-surface),0.38)' : 'rgba(var(--v-theme-surface), 0.38)'"
        :class="y > 10 ? 'app-bar-scrolled' : [$vuetify.theme.current.dark ? 'app-bar-dark' : 'app-bar-light', 'elevation-0']"
        class="navbar-blur"
      >
        <!-- toggle icon for mobile device -->
        <IconBtn
          id="vertical-nav-toggle-btn"
          class="ms-n3 me-2 d-inline-block d-md-none"
          @click="sidebar = !sidebar"
          size="large"
        >
          <VIcon
            size="26"
            icon="ri-menu-line"
            color="rgba(var(--v-theme-on-surface))"
          />
        </IconBtn>

        <!-- Title and Landing page sections -->
        <div class="d-flex align-center">
          <VAppBarTitle
            :class="$vuetify.display.xs ? 'me-0' : 'me-6'"
          >
            <RouterLink
              to="/"
              class="d-flex gap-x-4"
              :class="$vuetify.display.mdAndUp ? 'd-none' : 'd-block'"
            >
              <div class="app-logo">
                <!-- <VIcon class="logo-desktop"
                  :icon="logolight"
                  size="210"
                  style="height: auto !important;"
                /> -->
                <VIcon class="logo-mobile mx-auto"
                  :icon="logolightMobile"
                  :size="240"
                  style="height: auto !important;"
                />
                
                <!-- <img src="/images/svg/logo.svg"> -->
                <!-- ЛОГО
                <h1 class="app-logo-title">
                  Заголовок
                </h1> -->
              </div>
            </RouterLink>
          </VAppBarTitle>

          <!-- landing page sections -->
          <!-- :class="isCurrentRoute(listItem.to) ? 'active-link' : 'text-high-emphasis'" -->
          <!-- active-link -->
          <!-- <div class="text-base align-center d-none d-md-flex">

            <template v-for="menuItem in menuItems">
              <RouterLink v-if="menuItem.path"
                :to="menuItem.path"
                class="nav-link font-weight-medium py-2 px-2 px-lg-4"
              >
                {{ menuItem.listTitle }}
              </RouterLink>

              <span v-if="menuItem.children"
                class="font-weight-medium cursor-pointer px-2 px-lg-4 py-2"
                :class="isMegaMenuOpen ? 'active-link' : ''"
                style="color: rgba(var(--v-theme-on-surface));"
              >
                {{ menuItem.listTitle }}
                <VIcon
                  icon="ri-arrow-down-s-line"
                  size="16"
                  class="ms-2"
                />
                <VMenu
                  v-model="isMegaMenuOpen"
                  open-on-hover
                  activator="parent"
                  transition="slide-y-transition"
                  location="bottom center"
                  offset="16"
                  content-class="mega-menu"
                  location-strategy="static"
                  close-on-content-click
                >
                  <VCard max-width="1000">
                    <VCardText class="px-8 pb-2 pt-4">
                      <div class="nav-menu">
                        <div>
                          <ul>
                            <li v-for="subMenuItem in menuItem.children" style="list-style: none;" class="text-body-1 mb-4 text-no-wrap">
                              <RouterLink v-if="subMenuItem.path"
                                class="mega-menu-item"
                                :to="subMenuItem.path"
                              >
                                <div class="d-flex align-center">
                                  <VIcon
                                    :icon="subMenuItem.listIcon"
                                    color="primary"
                                    :size="10"
                                    class="me-2"
                                  />
                                  <span>{{ subMenuItem.listTitle }}</span>
                                </div>
                              </RouterLink>
                            </li>
                          </ul>
                        </div>
                      </div>
                    </VCardText>
                  </VCard>
                </VMenu>
              </span>
            </template>
          </div> -->
          <DesktopNavbarLinks 
            :menu-items="menuItems"
            v-model:isMegaMenuOpen="isMegaMenuOpen"
          />
        </div>

        <VSpacer />

        <AccountBlock />
      </VAppBar>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.nav-menu {
  display: flex;
  gap: 2rem;
}

.page-link {
  &:hover {
    color: rgb(var(--v-theme-primary)) !important;
  }
}

@media (max-width: 1280px) {
  .nav-menu {
    gap: 2.25rem;
  }
}

@media (min-width: 1920px) {
  .front-page-navbar {
    .v-toolbar {
      max-inline-size: calc(1440px - 32px);
    }
  }
}

@media (min-width: 1280px) and (max-width: 1919px) {
  .front-page-navbar {
    .v-toolbar {
      max-inline-size: calc(1200px - 32px);
    }
  }
}

@media (min-width: 960px) and (max-width: 1279px) {
  .front-page-navbar {
    .v-toolbar {
      max-inline-size: calc(900px - 32px);
    }
  }
}

@media (min-width: 600px) and (max-width: 959px) {
  .front-page-navbar {
    .v-toolbar {
      max-inline-size: calc(100% - 64px);
    }
  }
}

@media (max-width: 600px) {
  .front-page-navbar {
    .v-toolbar {
      max-inline-size: calc(100% - 6px);
    }
  }
}

.nav-item-img {
  border: 10px solid rgb(var(--v-theme-background));
  border-radius: 10px;
}

.active-link {
  color: rgb(var(--v-theme-primary)) !important;
}

.app-bar-light {
  border: 2px solid rgba(var(--v-theme-surface), 68%);
  border-radius: 0.5rem;
  background-color: rgba(var(--v-theme-surface), 38%);
  transition: all 0.1s ease-in-out;
}

.app-bar-dark {
  border: 2px solid rgba(var(--v-theme-surface), 68%);
  border-radius: 0.5rem;
  background-color: rgba(255, 255, 255, 4%);
  transition: all 0.1s ease-in-out;
}

.app-bar-scrolled {
  border: 2px solid rgb(var(--v-theme-surface));
  border-radius: 0.5rem;
  background-color: rgb(var(--v-theme-surface)) !important;
  transition: all 0.1s ease-in-out;
}

.front-page-navbar::after {
  position: fixed;
  z-index: 2;
  // backdrop-filter: saturate(100%) blur(6px);
  block-size: 5rem;
  content: "";
  inline-size: 100%;
}
</style>

<style lang="scss">

.front-page-navbar .nav-link {
  &:not(:hover) {
    color: rgb(var(--v-theme-on-surface));
  }
}


.front-page-navbar {
  .v-toolbar__content {
    padding-inline: 2rem !important;
  }

  .v-toolbar {
    inset-inline: 0 !important;
    margin-block-start: 0.2rem !important;
    margin-inline: auto !important;
  }
}

.mega-menu-item {
  &:hover {
    color: rgb(var(--v-theme-primary)) !important;
  }
}

#navigation-drawer-close-btn {
  position: absolute;
  cursor: pointer;
  inset-block-start: 0.5rem;
  inset-inline-end: 1rem;
}

@media (max-width: 400px) {
  .front-page-navbar .v-toolbar__content {
    padding-inline: 1rem !important;
  }
}

</style>
