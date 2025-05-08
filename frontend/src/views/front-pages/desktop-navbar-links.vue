<script setup lang="ts">
  interface MenuItem {
    listTitle: string
    listIcon?: string
    path?: string
    children?: MenuItem[]
  }

  const isMegaMenuOpen = ref(false)

  const menuItems: MenuItem[] = [
    {
      listTitle: 'Распознать заболевание',
      path: '/'
    },
    {
      listTitle: 'Возможности',
      path: '/'
    },
    // {
    //   listTitle: 'Информация',
    //   children: [
    //     {
    //       listTitle: 'О компании',
    //       listIcon: 'ri-circle-line',
    //       path: '/about/company',
    //     },
    //     {
    //       listTitle: 'Правила сайта',
    //       listIcon: 'ri-circle-line',
    //       path: '/about/rules',
    //     },
    //   ]
    // },
  ]

  const $props = defineProps({
    // menuItems: {
    //   type: Array as () => Array<any>,
    //   required: true
    // },
    isMegaMenuOpen: {
      type: Boolean,
      required: true
    },
  })

</script>
<template>
  <div class="desktop-navbar-links text-base align-center d-none d-md-flex">
    <template v-for="menuItem in menuItems">
      <RouterLink v-if="menuItem.path"
        :to="menuItem.path"
        class="nav-link font-weight-medium py-2 px-2 px-lg-4"
      >
        <!-- active-link -->
        {{ menuItem.listTitle }}
      </RouterLink>

      <a v-if="menuItem.children"
        class="nav-link font-weight-medium cursor-pointer px-2 px-lg-4 py-2"
        :class="isMegaMenuOpen ? 'active-link' : ''"
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
          close-on-content-click
          activator="parent"
          transition="slide-y-transition"
          location="bottom center"
          offset="16"
          content-class="mega-menu"
          location-strategy="static"
        >
          <VCard max-width="1000">
            <VCardText class="desktop-navbar-links px-6 pb-1 pt-4">
              <div class="nav-menu">
                <div>
                  <ul>
                    <li v-for="subMenuItem in menuItem.children" style="list-style: none;" class="text-body-1 mb-4 text-no-wrap">
                      <RouterLink v-if="subMenuItem.path"
                        class="mega-menu-item nav-link"
                        :to="subMenuItem.path"
                      >
                      <!-- :class="isCurrentRoute(listItem.to) ? 'active-link' : 'text-high-emphasis'" -->
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
      </a>
    </template>
  </div>

</template>


<style lang="scss">
@use "@layouts/styles/mixins" as layoutMixins;

.desktop-navbar-links .nav-link {
  &:not(:hover) {
    color: rgb(var(--v-theme-on-surface));
  }
}

.mega-menu {
  // margin-top: -20px;
  position: fixed !important;
  inset-block-start: 4.4rem;
  inset-inline-start: 50%;
  transform: translateX(-50%);

  @include layoutMixins.rtl {
    transform: translateX(50%);
  }
}

</style>
