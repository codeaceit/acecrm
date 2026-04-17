<template>
  <button
    class="sidebar-link flex h-7.5 cursor-pointer items-center rounded duration-300 ease-in-out focus:outline-none focus:transition-none focus-visible:rounded focus-visible:ring-2 focus-visible:ring-outline-gray-3"
    :class="
      isActive ? 'bg-surface-selected shadow-sm' : 'hover:bg-surface-gray-2'
    "
    @click="handleClick"
  >
    <div
      class="flex w-full items-center justify-between duration-300 ease-in-out"
      :class="isCollapsed ? 'ml-[3px] p-1' : 'px-4 py-4'"
    >
      <div class="flex items-center truncate">
        <Tooltip :text="label" placement="right" :disabled="!isCollapsed">
          <slot name="icon">
            <Icon
              :icon="icon"
              class="flex items-center size-4"
            />
          </slot>
        </Tooltip>
        <Tooltip
          :text="label"
          placement="right"
          :disabled="isCollapsed"
          :hoverDelay="1.5"
        >
          <span
            class="flex-1 flex-shrink-0 truncate text-sm font-medium duration-300 ease-in-out"
            :class="[
              isCollapsed
                ? 'ml-0 w-0 overflow-hidden opacity-0'
                : 'ml-2 w-auto opacity-100'
            ]"
          >
            {{ label }}
          </span>
        </Tooltip>
      </div>
      <slot name="right" />
    </div>
  </button>
</template>

<script setup>
import Icon from '@/components/Icon.vue'
import { Tooltip } from 'frappe-ui'
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { isMobileView, mobileSidebarOpened } from '@/composables/settings'

const router = useRouter()
const route = useRoute()

const props = defineProps({
  icon: { type: [Object, String, Function], default: null },
  label: { type: String, default: '' },
  to: { type: [Object, String], default: null },
  isCollapsed: { type: Boolean, default: false },
})

function handleClick() {
  if (!props.to) return
  if (typeof props.to === 'object') {
    router.push(props.to)
  } else {
    router.push({ name: props.to })
  }
  if (isMobileView.value) {
    mobileSidebarOpened.value = false
  }
}

let isActive = computed(() => {
  if (route.query.view) {
    return route.query.view == props.to?.query?.view
  }
  return route.name === props.to
})
</script>

<style scoped>
.sidebar-link:hover span,
.sidebar-link:hover svg {
  color: #98b055 !important;
}
.sidebar-link.bg-surface-selected span,
.sidebar-link.bg-surface-selected svg {
  color: #98b055 !important;
}
</style>
