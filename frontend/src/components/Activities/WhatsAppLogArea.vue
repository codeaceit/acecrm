<template>
  <div>
    <div class="mb-1 flex items-center justify-stretch gap-2 py-1 text-base">
      <div class="inline-flex items-center flex-wrap gap-1 text-ink-gray-5">
        <Avatar
          :image="log._user?.image"
          :label="log._user?.label"
          size="md"
        />
        <span class="font-medium text-ink-gray-8 ml-1">
          {{ log._user?.label || log.from || __('WhatsApp') }}
        </span>
      </div>
      <div class="ml-auto whitespace-nowrap">
        <Tooltip :text="formatDate(log.creation)">
          <div class="text-sm text-ink-gray-5">
            {{ __(timeAgo(log.creation)) }}
          </div>
        </Tooltip>
      </div>
    </div>
    <div
      class="flex flex-col gap-2 border cursor-pointer border-outline-gray-modals rounded-md bg-surface-cards px-3 py-2.5 text-ink-gray-9"
    >
      <div class="flex items-center justify-between">
        <div class="inline-flex gap-2 items-center text-base font-medium">
          <div>
            {{ log.from }}
          </div>
        </div>
      </div>
      <div
        v-if="log.message"
        class="flex items-center flex-wrap gap-2 text-sm text-ink-gray-7"
      >
        <div class="line-clamp-2">{{ log.message }}</div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { Avatar, Tooltip } from 'frappe-ui'
import { timeAgo, formatDate } from '@/utils'

const props = defineProps({
  log: {
    type: Object,
    required: true,
  },
})
</script>
