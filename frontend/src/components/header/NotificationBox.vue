<script lang="ts" setup>

import { useApi } from '@/composables/useApi';
import { useUserStore } from "@/store";
import messageAudio from '@images/audio/message.mp3';

  const $api = useApi()
  const isOpen = ref(false)
  const $store = useUserStore()
  const isLoading = ref(false)
  const $route = useRoute()
  const regularInterval = ref<any|null>(null)

  const isAuthorize = computed(() => {
    return !!$store.currentAccount
  })

  const notifications = computed(() => {
    return isAuthorize.value && $store.currentAccount && $store.currentNotifications ? $store.currentNotifications : []
  })

  const currentRouteName = computed(() => $route.name)

  watch(() => isAuthorize.value, async () => {
    isLoading.value = true
    await $store.loadNotifications()
    isLoading.value = false
  })

  const regularLoading = async () => {
    if (!isAuthorize.value) {
      return
    }
    const previosCount = notifications.value.length
    isLoading.value = true
    await $store.loadNotifications()
    if (notifications.value.length > previosCount) {
      new Audio(messageAudio).play()
    }
    isLoading.value = false
  }

  const hideNotification = async (notificationId: number) => {
    isLoading.value = true
    await $api.get(`/account/notifications/${notificationId}/hide/`)
    await $store.loadNotifications()
    isLoading.value = false
  }

  const notificationLink = computed(() => (item: any) => {
    if (item.offer) {
      return '/account/my-offers/' + item.offer + '#' + item.id
    }
    else if (item.service) {
      return '/services/' + item.service
    }
    else if (item.route) {
      return item.route
    }
    return null
  })

  onMounted(async () => {
    if ($store.currentAccount) {
      isLoading.value = true
      await $store.loadNotifications()
      isLoading.value = false
      regularInterval.value = setInterval(() => {
        regularLoading()
      }, 10000);
    }
  })

  onBeforeUnmount(() => {
    clearInterval(regularInterval.value)
  })
</script>

<template>
  <VMenu
    width="280"
    location="bottom end"
    offset="14px"
    :close-on-content-click="false"
  >
    <template v-slot:activator="{ props }">
      <VBadge :content="notifications.length"
        :color="notifications && notifications.length ? 'error' : 'light-secondary'"
      >
      <!-- class="mr-4" -->

        <VBtn icon="ri-notification-fill"
        :color="notifications && notifications.length ? 'primary' : 'default'"
          v-bind="props"
        />
      </VBadge>
    </template>
    <VList>
      <!-- <VBtn @click="regularLoading">!!!</VBtn> -->
      <div v-if="!notifications || !notifications.length" class="px-4 py-4">
        <span class="text-primary">
          Пока нет уведомлений
        </span>
      </div>
      <VListItem :to="notificationLink(notification)"
        v-for="(notification, index) in notifications"
        :key="index"
        @click="hideNotification(notification.id)"
      >
        <VListItemTitle style="white-space: wrap;">{{ notification.message }}</VListItemTitle>
        <VDivider v-if="index < notifications.length - 1" />
      </VListItem>
    </VList>
  </VMenu>

</template>

<style scoped>
.v-enter-active,
.v-leave-active {
  transition: opacity 0.5s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}

</style>
