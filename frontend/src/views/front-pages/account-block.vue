<script setup lang="ts">

import NotificationBox from '@/components/header/NotificationBox.vue';
import UserProfile from '@/layouts/components/UserProfile.vue';
import { useUserStore } from "@/store";
import MiniLogin from '@/views/front-pages/mini-login.vue';
  
  const $store = useUserStore()

  const isAuthorize = computed(() => {
    return !!$store.currentAccount
  })
</script>
<template>
  <div class="d-flex gap-x-4">

    <!-- <NotificationBox v-if="!$vuetify.display.xs" /> -->
    <NotificationBox v-if="isAuthorize" />
    
    <!-- <VBtn icon="ri-shopping-cart-fill" color="secondary" /> -->

    <UserProfile v-if="isAuthorize" />
    <MiniLogin v-else />

  </div>
</template>
