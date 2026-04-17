<template>
  <div class="h-full w-full">
    <div
      v-if="item.type == 'number_chart'"
      class="flex h-full w-full rounded shadow overflow-hidden cursor-pointer bg-[#343434] text-white [&_*]:bg-[#343434] [&_*]:text-white"
    >
      <Tooltip :text="__(item.data.tooltip)">
        <NumberChart
          v-if="item.data"
          :key="index"
          class="!items-start !bg-[#343434]"
          :config="item.data"
        />
      </Tooltip>
    </div>
    <div
      v-else-if="item.type == 'spacer'"
      class="rounded bg-surface-white h-full overflow-hidden text-ink-gray-5 flex items-center justify-center"
      :class="editing ? 'border border-dashed border-outline-gray-2' : ''"
    >
      {{ editing ? __('Spacer') : '' }}
    </div>
    <div
      v-else-if="item.type == 'axis_chart'"
      class="h-full w-full rounded-md bg-[#343434] shadow [&_*]:bg-[#343434]"
    >
      <AxisChart v-if="item.data" :config="axisChartConfig" />
    </div>
    <div
      v-else-if="item.type == 'donut_chart'"
      class="h-full w-full rounded-md bg-[#343434] shadow overflow-hidden [&_*]:bg-[#343434]"
    >
      <DonutChart v-if="item.data" :config="donutChartConfig" />
    </div>
  </div>
</template>
<script setup>
import { AxisChart, DonutChart, NumberChart, Tooltip } from 'frappe-ui'
import { computed } from 'vue'

const props = defineProps({
  index: { type: Number, required: true },
  item: { type: Object, required: true },
  editing: { type: Boolean, default: false },
})

const greenColors = ['#22c55e', '#16a34a', '#15803d', '#166534', '#14532d', '#4ade80']

const axisChartConfig = computed(() => {
  if (!props.item.data) return null
  const config = { ...props.item.data }
  if (config.series) {
    config.series = config.series.map((s, i) => ({
      ...s,
      color: greenColors[i % greenColors.length]
    }))
  }
  return config
})

const donutChartConfig = computed(() => {
  if (!props.item.data) return null
  const config = { ...props.item.data }
  if (config.colors) {
    config.colors = greenColors
  }
  return config
})
</script>

<style scoped>
.number-card {
  background: #343434 !important;
  width: 100% !important;
}
.number-card > * {
  background: #343434 !important;
}
</style>
