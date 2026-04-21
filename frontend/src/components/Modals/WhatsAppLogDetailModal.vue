<template>
  <Dialog v-model="show">
    <template #body>
      <div class="bg-surface-modal px-4 pb-6 pt-5 sm:px-6">
        <div class="mb-5 flex items-center justify-between">
          <div>
            <h3 class="text-2xl font-semibold leading-6 text-ink-gray-9">
              {{ __('WhatsApp Details') }}
            </h3>
          </div>
          <div class="flex items-center gap-1">
            <Button icon="x" variant="ghost" class="w-7" @click="show = false" />
          </div>
        </div>
        <div class="flex flex-col gap-3.5">
          <div
            v-for="field in detailFields"
            :key="field.name"
            class="flex gap-2 text-base text-ink-gray-8"
          >
            <div class="grid size-7 place-content-center">
              <component :is="field.icon" />
            </div>
            <div class="flex min-h-7 w-full items-center gap-2">
              <Tooltip v-if="field.tooltip" :text="field.tooltip">
                {{ field.value }}
              </Tooltip>
              <div v-else>
                {{ field.value }}
              </div>
            </div>
          </div>
          <div v-if="!detailFields.length" class="text-base text-ink-gray-5">
            {{ __('No details available') }}
          </div>
        </div>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import EditIcon from '@/components/Icons/EditIcon.vue'
import ArrowUpRightIcon from '@/components/Icons/ArrowUpRightIcon.vue'
import { isMobileView } from '@/composables/settings'
import { FeatherIcon, Tooltip, Button, Dialog } from 'frappe-ui'
import { computed, h, watch, ref } from 'vue'

const show = defineModel({ type: Boolean })
const whatsappLog = defineModel('whatsappLog', { type: Object })

const logData = ref({})
const loading = ref(false)

watch(() => whatsappLog.value?.data, (newVal) => {
  if (newVal) {
    logData.value = { ...newVal, from_number: newVal.from_number || newVal.from }
    loading.value = false
  }
}, { immediate: true })

watch(() => whatsappLog.value, (newVal) => {
  if (newVal && typeof newVal === 'object' && (newVal.from_number || newVal.from)) {
    logData.value = { ...newVal, from_number: newVal.from_number || newVal.from }
    loading.value = false
  }
}, { immediate: true })

const detailFields = computed(() => {
  let data = logData.value
  if (!data || !data.from_number) return []

  let details = [
    {
      icon: h(FeatherIcon, { name: 'phone', class: 'h-4 w-4' }),
      name: 'from',
      value: data.from_number || data.from || '',
      tooltip: data.from_number || data.from || '',
    },
    {
      icon: h(FeatherIcon, { name: 'message-square', class: 'h-4 w-4' }),
      name: 'message',
      value: data.message || '',
    },
    {
      icon: h(FeatherIcon, { name: 'calendar', class: 'h-4 w-4' }),
      name: 'date',
      value: data.date ? new Date(data.date).toLocaleDateString() : '',
      tooltip: data.date ? new Date(data.date).toLocaleDateString() : '',
    },
    {
      icon: h(FeatherIcon, { name: 'user', class: 'h-4 w-4' }),
      name: 'user',
      value: data.user || '',
    },
  ]

  return details
})
</script>