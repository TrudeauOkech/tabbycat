<script setup>
import SmartTable from './SmartTable.vue'
import { computed, ref, onBeforeUpdate } from 'vue'
import { useDjangoI18n } from '../composables/useDjangoI18n.js'

const props = defineProps({
  tablesData: Array,
  orientation: String,
})

const emit = defineEmits(['toggle-checked'])

const { gettext } = useDjangoI18n()
const tableRefs = ref([])
const search = ref('')

// Reset refs before each update to ensure they match the current render cycle
onBeforeUpdate(() => {
  tableRefs.value = []
})

const filteredTablesData = computed(() => {
  if (props.tablesData === null) {
    return []
  }
  if (!search.value) {
    return props.tablesData
  }
  const needle = search.value.toLowerCase()
  return props.tablesData.filter((table) => {
    return (
      table.title.toLowerCase().includes(needle) ||
      (table.rows || []).some((row) => {
        return (
          row.cells || row
        ).some((cell) => {
          return (
            (cell.text && cell.text.toLowerCase().includes(needle)) ||
            (cell.sort && cell.sort.toString().toLowerCase().includes(needle))
          )
        })
      })
    )
  })
})

const copyTableTrigger = (i) => {
  const child = tableRefs.value?.[i]
  child?.copyTableData?.()
}
</script>

<template>
  <div>
    <div
      v-if="filteredTablesData.length > 0"
      class="row"
    >
      <div class="col-xl-6">
        <div class="input-group mb-3">
          <span class="input-group-text"><i data-feather="search" /></span>
          <input
            v-model="search"
            class="form-control"
            :placeholder="gettext('Filter tables...')"
          >
        </div>
      </div>
    </div>
    <div
      :class="{
        'masonry-grid': orientation === 'masonry',
        row: orientation === 'row',
      }"
    >
      <div
        v-for="(t, i) in filteredTablesData"
        :key="i"
        class="col-12"
        :class="{ 'col-xl-6': orientation === 'masonry' }"
      >
        <div class="card mb-4">
          <div
            v-if="t.title"
            class="card-header d-flex justify-content-between align-items-center"
          >
            <h4 class="card-title mb-0">
              {{ t.title }}
              <span
                v-if="t.rows"
                class="badge bg-secondary"
              >
                {{ t.rows.length }}
              </span>
            </h4>
            <div class="dropdown">
              <a
                href="#"
                class="btn btn-ghost-secondary btn-icon btn-sm rounded-circle"
                data-bs-toggle="dropdown"
              >
                <i data-feather="more-vertical" />
              </a>
              <div class="dropdown-menu dropdown-menu-end">
                <a
                  class="dropdown-item"
                  href="#"
                  @click="copyTableTrigger(i)"
                >
                  <i data-feather="copy" /> {{ gettext("Copy table to CSV") }}
                </a>
              </div>
            </div>
          </div>
          <smart-table
            :ref="
              (el) => {
                if (el) tableRefs[i] = el;
              }
            "
            :table-data="t"
            @toggle-checked="emit('toggle-checked', $event)"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.masonry-grid {
  column-count: 2;
  column-gap: 1.5rem;
}
@media (max-width: 1200px) {
  .masonry-grid {
    column-count: 1;
  }
}
.card {
  break-inside: avoid;
}
</style>
