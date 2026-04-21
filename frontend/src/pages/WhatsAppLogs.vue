<template>
  <LayoutHeader>
    <template #left-header>
      <ViewBreadcrumbs v-model="viewControls" routeName="WhatsApp Logs" />
    </template>
    <template #right-header>
      <CustomActions v-if="listView?.customListActions" :actions="listView.customListActions" />
      <Button variant="solid" :label="__('Create')" iconLeft="plus" @click="showCreateModal = true" />
    </template>
  </LayoutHeader>
  <ViewControls
    ref="viewControls"
    v-model="whatsappLogs"
    v-model:loadMore="loadMore"
    v-model:resizeColumn="triggerResize"
    v-model:updatedPageCount="updatedPageCount"
    doctype="Whatsapp Log"
  />
  <WhatsAppLogsListView
    v-if="whatsappLogs.data && rows.length"
    ref="listView"
    v-model="whatsappLogs.data.page_length_count"
    v-model:list="whatsappLogs"
    :rows="rows"
    :columns="columns"
    :options="{
      showTooltip: false,
      resizeColumn: true,
      rowCount: whatsappLogs.data.row_count,
      totalCount: whatsappLogs.data.total_count,
    }"
    @showLog="showLog"
    @loadMore="loadMorePlus"
    @columnWidthUpdated="triggerResizePlus"
    @updatePageCount="updatePageCount"
    @applyFilter="applyFilter"
    @applyLikeFilter="applyLikeFilter"
    @likeDoc="likeDoc"
    @selectionsChanged="updateSelections"
  />
  <EmptyState v-else-if="whatsappLogs.data && !rows.length" name="WhatsApp Logs" :icon="WhatsAppIcon" />
  <WhatsAppLogDetailModal
    v-model="showWhatsAppLogDetailModal"
    v-model:whatsappLog="whatsappLog"
  />
  <Dialog v-model="showCreateModal" :options="{ title: __('Create WhatsApp Log'), size: 'lg' }">
    <template #body>
      <div class="flex flex-col gap-4 p-4">
        <div class="flex flex-col gap-1">
          <label class="text-sm font-medium text-ink-gray-5">{{ __("From Number") }}</label>
          <FormControl v-model="newLog.from" placeholder="+91xxxxxxxxxx" />
        </div>
        <div class="flex flex-col gap-1">
          <label class="text-sm font-medium text-ink-gray-5">{{ __("Message") }}</label>
          <textarea v-model="newLog.message" class="w-full rounded border border-outline-gray-modals bg-surface-white px-3 py-2 text-base" :rows="4" />
        </div>
        <div class="flex flex-col gap-1">
          <label class="text-sm font-medium text-ink-gray-5">{{ __("Date") }}</label>
          <DatePicker v-model="newLog.date" />
        </div>
        <div class="flex flex-col gap-1">
          <label class="text-sm font-medium text-ink-gray-5">{{ __("User") }}</label>
          <Link v-model="newLog.user" doctype="User" />
        </div>
      </div>
    </template>
    <template #actions>
      <Button variant="solid" class="w-full" @click="createLog" :loading="saving">{{ __("Create") }}</Button>
    </template>
  </Dialog>
</template>

<script setup>
import ViewBreadcrumbs from '@/components/ViewBreadcrumbs.vue'
import CustomActions from '@/components/CustomActions.vue'
import WhatsAppIcon from '@/components/Icons/WhatsAppIcon.vue'
import LayoutHeader from '@/components/LayoutHeader.vue'
import ViewControls from '@/components/ViewControls.vue'
import WhatsAppLogsListView from '@/components/ListViews/WhatsAppLogsListView.vue'
import EmptyState from '@/components/ListViews/EmptyState.vue'
import WhatsAppLogDetailModal from '@/components/Modals/WhatsAppLogDetailModal.vue'
import { getRandom } from '@/utils'
import { call, Button, FormControl, DatePicker, Dialog } from 'frappe-ui'
import Link from '@/components/Controls/Link.vue'
import { ref, computed } from 'vue'

const listView = ref(null)
const showCreateModal = ref(false)
const showWhatsAppLogDetailModal = ref(false)
const whatsappLog = ref({})
const saving = ref(false)
const newLog = ref({ from: '', message: '', date: '', user: '' })
const loadMore = ref(1)
const triggerResize = ref(1)
const updatedPageCount = ref(20)
const viewControls = ref(null)

const whatsappLogs = ref({})

const rows = computed(() => {
  if (!whatsappLogs.value?.data?.data) {
    return []
  }
  let viewType = whatsappLogs.value.data.view_type
  if (viewType && !['list', 'group_by'].includes(viewType)) {
    return []
  }
  return whatsappLogs.value.data.data
})

const columns = computed(() => {
  return [
    { label: "From Number", type: "Data", key: "from", width: "12rem" },
    { label: "Message", type: "Small Text", key: "message", width: "20rem" },
    { label: "Date", type: "Date", key: "date", width: "10rem" },
    { label: "User", type: "Link", key: "user", width: "10rem" },
  ]
})

function getWhatsAppLogDetail(name, log, columns) {
  let _log = { name }
  if (columns) {
    columns.forEach((col) => {
      if (col.key === 'name') return
      _log[col.key] = log[col.key] || ''
    })
  }
  return _log
}

function showLog(row) {
  console.log('showLog called with row:', JSON.parse(JSON.stringify(row)))
  showWhatsAppLogDetailModal.value = true
  whatsappLog.value = { data: row }
}

function loadMorePlus() {
  loadMore.value++
}

function triggerResizePlus() {
  triggerResize.value++
}

function updatePageCount(count) {
  updatedPageCount.value = count
}

function applyFilter(data) {
  viewControls.value?.applyFilter(data)
}

function applyLikeFilter(data) {
  viewControls.value?.applyLikeFilter(data)
}

function likeDoc(data) {
  viewControls.value?.likeDoc(data)
}

function updateSelections(selections) {
  viewControls.value?.updateSelections(selections)
}

async function createLog() {
  saving.value = true
  try {
    await call('frappe.client.insert', {
      doc: {
        doctype: 'Whatsapp Log',
        id: getRandom(6),
        from: newLog.value.from,
        message: newLog.value.message,
        date: newLog.value.date,
        user: newLog.value.user,
      },
    })
    showCreateModal.value = false
    saving.value = false
    newLog.value = { from: '', message: '', date: '', user: '' }
    whatsappLogs.value.reload?.()
  } catch (e) {
    saving.value = false
  }
}
</script>