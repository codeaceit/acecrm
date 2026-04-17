<template>
  <div v-if="brand?.logo">
    <img :src="brand.logo" class="h-10 w-10 object-cover" />
  </div>
  <CRMLogo v-else class="size-10 shrink-0 rounded" />
</template>

<script setup>
import CRMLogo from '@/components/Icons/CRMLogo.vue'

const brand = defineModel({ type: Object, default: () => ({}) })
</script>
