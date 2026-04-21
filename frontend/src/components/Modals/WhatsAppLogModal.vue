<template>
  <Dialog v-model="show" :options="dialogOptions">
    <template #body>
      <div class="px-4 pt-5 pb-6 bg-surface-modal sm:px-6">
        <div class="flex items-center justify-between mb-5">
          <div class="flex items-center gap-2">
            <h3 class="text-2xl font-semibold leading-6 text-ink-gray-9">
              {{ __(dialogOptions.title) || __('Untitled') }}
            </h3>
          </div>
          <div class="flex items-center gap-1">
            <Button
              variant="ghost"
              class="w-7"
              icon="x"
              @click="show = false"
            />
          </div>
        </div>
        <div class="flex flex-col gap-4">
          <div class="flex flex-col gap-1">
            <label class="text-sm font-medium text-ink-gray-5">
              {{ __("From Number") }} <span class="text-red-500">*</span>
            </label>
            <FormControl
              v-model="whatsappLog.doc.from"
              placeholder="+91xxxxxxxxxx"
            />
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-sm font-medium text-ink-gray-5">
              {{ __("Message") }} <span class="text-red-500">*</span>
            </label>
            <textarea
              v-model="whatsappLog.doc.message"
              class="w-full rounded border border-outline-gray-modals bg-surface-white px-3 py-2 text-base text-ink-gray-9"
              :rows="4"
              :placeholder="__('Enter message...')"
            />
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-sm font-medium text-ink-gray-5">
              {{ __("Date") }}
            </label>
            <DatePicker
              v-model="whatsappLog.doc.date"
              :value="whatsappLog.doc.date"
              placeholder="Select date"
            />
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-sm font-medium text-ink-gray-5">
              {{ __("Messaged By") }} <span class="text-red-500">*</span>
            </label>
            <Link
              v-model="whatsappLog.doc.user"
              doctype="User"
              placeholder="Select user"
            />
          </div>
        </div>
        <ErrorMessage class="mt-4" :message="error" />
      </div>
      <div class="px-4 pt-4 pb-7 sm:px-6">
        <Button variant="solid" class="w-full" @click="createWhatsAppLog" :loading="loading">
          {{ __('Create') }}
        </Button>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import FieldLayout from '@/components/FieldLayout/FieldLayout.vue'
import Link from '@/components/Controls/Link.vue'
import { getRandom } from '@/utils'
import { call, Button, createResource, ErrorMessage, FormControl, DatePicker } from 'frappe-ui'
import { ref, computed, reactive } from 'vue'

const props = defineProps({
  data: { type: Object, default: () => ({}) },
  referenceDoc: { type: Object, default: () => ({}) },
  options: { type: Object, default: () => ({ afterInsert: () => {} }) },
})

const show = defineModel({ type: Boolean })

const loading = ref(false)
const error = ref(null)

const whatsappLog = reactive({
  doc: {
    from: '',
    message: '',
    user: '',
    date: '',
  },
})

const dialogOptions = computed(() => {
  return {
    title: __('Log WhatsApp'),
    size: 'lg',
  }
})

const _createWhatsAppLog = createResource({
  url: 'frappe.client.insert',
  onSuccess(doc) {
    loading.value = false
    if (doc.name) {
      handleWhatsAppLogUpdate(doc)
    }
  },
  onError(err) {
    loading.value = false
    if (err.exc_type == 'MandatoryError') {
      const errorMessage = err.messages
        .map((msg) => {
          let arr = msg.split(': ')
          return arr[arr.length - 1].trim()
        })
        .join(', ')
      error.value = __('These fields are required: {0}', [errorMessage])
      return
    }
    error.value = err.messages?.[0] || err
  },
})

function handleWhatsAppLogUpdate(doc) {
  loading.value = false
  show.value = false
  whatsappLog.doc = { from: '', message: '', user: '', date: '' }
  props.options.afterInsert?.(doc)
}

async function createWhatsAppLog() {
  let reference_doctype = props.referenceDoc.doctype

  if (reference_doctype === 'CRM Lead') {
    reference_doctype = 'CRM Lead'
  } else if (reference_doctype === 'CRM Deal') {
    reference_doctype = 'CRM Deal'
  }

  Object.assign(whatsappLog.doc, {
    doctype: 'Whatsapp Log',
    id: getRandom(6),
    reference_doctype: reference_doctype,
    reference_docname: props.referenceDoc.name,
  })

  loading.value = true
  
  await _createWhatsAppLog.submit({
    doc: whatsappLog.doc,
  })
}
</script>