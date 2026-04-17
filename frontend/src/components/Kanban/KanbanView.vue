<template>
  <div class="flex overflow-x-auto h-full">
    <Draggable
      v-if="columns"
      :list="columns"
      item-key="column"
      :delay="isTouchScreenDevice() ? 200 : 0"
      class="flex gap-8 sm:mx-10 mx-8 pb-3.5"
      @end="updateColumn"
    >
      <template #item="{ element: column }">
        <div
          v-if="!column.column.delete"
          class="flex flex-col gap-2.5 min-w-72 w-72 rounded-lg p-2.5"
          :class="getColumnBgColor(column.column.color)"
        >
          <div class="flex gap-2 items-center group justify-between">
            <div class="flex items-center text-base">
              <Popover>
                <template #target="{ togglePopover }">
                  <Button
                    variant="ghost"
                    size="sm"
                    class="hover:!bg-surface-gray-2"
                    @click="togglePopover"
                  >
                    <IndicatorIcon :class="parseColor(column.column.color)" />
                  </Button>
                </template>
                <template #body>
                  <div
                    class="flex flex-col gap-3 px-3 py-2.5 min-w-40 rounded-lg bg-surface-modal shadow-2xl ring-1 ring-black ring-opacity-5 focus:outline-none"
                  >
                    <div class="flex gap-1">
                      <Button
                        v-for="color in colors"
                        :key="color"
                        variant="ghost"
                        @click="() => (column.column.color = color)"
                      >
                        <IndicatorIcon :class="parseColor(color)" />
                      </Button>
                    </div>
                    <div class="flex flex-row-reverse">
                      <Button
                        variant="solid"
                        :label="__('Apply')"
                        @click="updateColumn"
                      />
                    </div>
                  </div>
                </template>
              </Popover>
              <div class="text-ink-gray-9">{{ column.column.name }}</div>
            </div>
            <div class="flex">
              <Dropdown :options="actions(column)">
                <template #default>
                  <Button
                    class="hidden group-hover:flex"
                    icon="more-horizontal"
                    variant="ghost"
                  />
                </template>
              </Dropdown>
              <Button
                icon="plus"
                variant="ghost"
                @click="options.onNewClick(column)"
              />
            </div>
          </div>
          <div
              class="overflow-y-auto flex flex-col gap-2 h-full kanban-scroll"
              :style="{ '--scroll-color': getColumnColor(column.column.color) }"
            >
            <Draggable
              :list="column.data"
              group="fields"
              item-key="name"
              class="flex flex-col gap-3.5 flex-1"
              :delay="isTouchScreenDevice() ? 200 : 0"
              :data-column="column.column.name"
              @end="updateColumn"
            >
              <template #item="{ element: fields }">
                <component
                  :is="options.getRoute ? 'router-link' : 'div'"
                  class="pt-3 px-3.5 pb-2.5 rounded-lg border border-outline-gray-modals bg-surface-cards text-base flex flex-col text-ink-gray-9"
                  :data-name="fields.name"
                  v-bind="{
                    to: options.getRoute ? options.getRoute(fields) : undefined,
                    onClick: options.onClick
                      ? () => options.onClick(fields)
                      : undefined,
                  }"
                >
                  <slot
                    name="title"
                    v-bind="{ fields, titleField, itemName: fields.name }"
                  >
                    <div class="h-5 flex items-center">
                      <div v-if="fields[titleField]">
                        {{ fields[titleField] }}
                      </div>
                      <div v-else class="text-ink-gray-4">
                        {{ __('No Title') }}
                      </div>
                    </div>
                  </slot>
                  <div class="border-b h-px my-2.5" />

                  <div class="flex flex-col gap-3.5">
                    <template v-for="value in column.fields" :key="value">
                      <slot
                        name="fields"
                        v-bind="{
                          fields,
                          fieldName: value,
                          itemName: fields.name,
                        }"
                      >
                        <div v-if="fields[value]" class="truncate">
                          {{ fields[value] }}
                        </div>
                      </slot>
                    </template>
                  </div>
                  <div class="border-b h-px mt-2.5 mb-2" />
                  <slot name="actions" v-bind="{ itemName: fields.name }">
                    <div class="flex gap-2 items-center justify-between">
                      <div></div>
                      <Button icon="plus" variant="ghost" @click.stop.prevent />
                    </div>
                  </slot>
                </component>
              </template>
            </Draggable>
            <div
              v-if="column.column.count < column.column.all_count"
              class="flex items-center justify-center"
            >
              <Button
                :label="__('Load More')"
                @click="emit('loadMore', column.column.name)"
              />
            </div>
          </div>
        </div>
      </template>
    </Draggable>
    <div class="shrink-0 min-w-64">
      <Autocomplete
        value=""
        :options="deletedColumns"
        @change="(e) => addColumn(e)"
      >
        <template #target="{ togglePopover }">
          <Button
            class="w-full mt-2.5 mb-1 mr-5"
            :label="__('Add Column')"
            iconLeft="plus"
            @click="togglePopover()"
          />
        </template>
        <template #footer>
          <Button
            class="w-full"
            :label="__('Reload Columns')"
            :iconLeft="RefreshIcon"
            @click="updateColumn(null, true)"
          />
        </template>
      </Autocomplete>
    </div>
  </div>
</template>
<script setup>
import RefreshIcon from '@/components/Icons/RefreshIcon.vue'
import Autocomplete from '@/components/frappe-ui/Autocomplete.vue'
import IndicatorIcon from '@/components/Icons/IndicatorIcon.vue'
import { isTouchScreenDevice, colors, parseColor } from '@/utils'
import Draggable from 'vuedraggable'
import { Dropdown, Popover } from 'frappe-ui'
import { computed } from 'vue'

defineProps({
  options: {
    type: Object,
    default: () => ({
      getRoute: null,
      onClick: null,
      onNewClick: null,
    }),
  },
})

const emit = defineEmits(['update', 'loadMore'])

const kanban = defineModel({ type: Object })

const titleField = computed(() => {
  return kanban.value?.data?.title_field
})

const columns = computed(() => {
  if (!kanban.value?.data?.data || kanban.value.data.view_type != 'kanban')
    return []
  let _columns = kanban.value.data.data

  _columns.forEach((column, i) => {
    column.column['color'] = colors[i % colors.length]
  })
  return _columns
})

const deletedColumns = computed(() => {
  const _columns = kanban.value?.data?.kanban_columns || []
  return _columns
    ?.filter((col) => col['delete'])
    .map((col) => {
      return { label: col.name, value: col.name }
    })
})

function actions(column) {
  return [
    {
      group: __('Options'),
      hideLabel: true,
      items: [
        {
          label: __('Delete'),
          icon: 'trash-2',
          onClick: () => {
            column.column['delete'] = true
            updateColumn()
          },
        },
      ],
    },
  ]
}

function addColumn(e) {
  let column = columns.value.find((col) => col.column.name == e.value)
  column.column['delete'] = false
  columns.value.splice(columns.value.indexOf(column), 1)
  columns.value.push(column)
  updateColumn()
}

function updateColumn(d, fetchNewColumns = false) {
  let toColumn = d?.to?.dataset.column
  let fromColumn = d?.from?.dataset.column
  let itemName = d?.item?.dataset.name

  let _columns = []
  columns.value.forEach((col) => {
    col.column['order'] = col.data.map((d) => d.name)
    if (col.column.page_length) {
      delete col.column.page_length
    }
    _columns.push(col.column)
  })

  let data = { kanban_columns: _columns, fetchNewColumns }

  if (toColumn != fromColumn) {
    data = { item: itemName, to: toColumn, kanban_columns: _columns }
  }

  emit('update', data)
}

function getColumnBgColor(color) {
  const colorMap = {
    blue: 'bg-gradient-to-br from-[#8B7B74] to-[#C9B8A8]',
    violet: 'bg-gradient-to-br from-blue-600 to-blue-200',
    gray: 'bg-gradient-to-br from-violet-600 to-violet-200',
    green: 'bg-gradient-to-br from-green-600 to-green-200',
    red: 'bg-gradient-to-br from-red-600 to-red-200',
    pink: 'bg-gradient-to-br from-pink-600 to-pink-200',
    orange: 'bg-gradient-to-br from-orange-600 to-orange-200',
    amber: 'bg-gradient-to-br from-amber-600 to-amber-200',
    yellow: 'bg-gradient-to-br from-yellow-600 to-yellow-200',
    cyan: 'bg-gradient-to-br from-cyan-600 to-cyan-200',
    teal: 'bg-gradient-to-br from-teal-600 to-teal-200',
    purple: 'bg-gradient-to-br from-purple-600 to-purple-200',
    black: 'bg-gradient-to-br from-gray-500 to-gray-200',
  }
  return colorMap[color] || 'bg-gradient-to-br from-yellow-600 to-yellow-200'
}

function getColumnColor(color) {
  const colorMap = {
    blue: '#D4C4B5',
    violet: '#93c5fd',
    gray: '#c4b5fd',
    green: '#86efac',
    red: '#fca5a5',
    pink: '#f9a8d4',
    orange: '#fdba74',
    amber: '#fde68a',
    yellow: '#fde68a',
    cyan: '#67e8f9',
    teal: '#5eead4',
    purple: '#d8b4fe',
    black: '#e5e7eb',
  }
  return colorMap[color] || '#fef08a'
}
</script>

<style scoped>
.kanban-scroll::-webkit-scrollbar {
  width: 6px;
}
.kanban-scroll::-webkit-scrollbar-track {
  background: transparent;
}
.kanban-scroll::-webkit-scrollbar-thumb {
  background: var(--scroll-color);
  border-radius: 3px;
}
.kanban-scroll::-webkit-scrollbar-thumb:hover {
  background: var(--scroll-color);
}
</style>
