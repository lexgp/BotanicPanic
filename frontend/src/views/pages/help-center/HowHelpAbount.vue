<template>
  <v-expansion-panels multiple v-model="howHelp">
    <VExpansionPanel
      value="lids"
      :title="pagesPragments.MainHowHelpLidogenerator.title"
      :text="pagesPragments.MainHowHelpLidogenerator.content"
    />
    <VExpansionPanel
      value="bonuses"
      :title="pagesPragments.MainHowHelpBonus.title"
      :text="pagesPragments.MainHowHelpBonus.content"
    />
    <VExpansionPanel
      value="referrals"
      :title="pagesPragments.MainHowHelpReferral.title"
      :text="pagesPragments.MainHowHelpReferral.content"
    />
  </v-expansion-panels>
  <p class="px-2 mt-4 font-weight-semibold">
    {{ pagesPragments.MainHowHelp.content }}
  </p>
</template>

<script setup lang="ts">

  const howHelp = ref(['lids', 'bonuses', 'referrals'])

  defineProps({
    pagesPragments: {
      type: Object,
      required: true
    }
  })

</script>
