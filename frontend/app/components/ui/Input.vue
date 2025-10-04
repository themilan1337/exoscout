<template>
  <input
    :type="type"
    :value="modelValue"
    :placeholder="placeholder"
    :disabled="disabled"
    :readonly="readonly"
    :class="inputClasses"
    @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
    @blur="$emit('blur', $event)"
    @focus="$emit('focus', $event)"
  />
</template>

<script setup lang="ts">
interface Props {
  modelValue?: string | number
  type?: 'text' | 'email' | 'password' | 'number' | 'tel' | 'url' | 'search'
  placeholder?: string
  disabled?: boolean
  readonly?: boolean
  variant?: 'default' | 'error' | 'success'
  size?: 'sm' | 'md' | 'lg'
  block?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: '',
  type: 'text',
  variant: 'default',
  size: 'md',
  disabled: false,
  readonly: false,
  block: false
})

const emit = defineEmits<{
  'update:modelValue': [value: string | number]
  blur: [event: FocusEvent]
  focus: [event: FocusEvent]
}>()

const inputClasses = computed(() => {
  const base = 'block rounded-md border-0 ring-1 ring-zinc-300 ring-inset transition-colors transition-all focus:ring-1 focus:outline-none focus:ring-zinc-600 focus:ring-inset disabled:cursor-not-allowed disabled:opacity-50'

  const variants = {
    default: 'text-gray-900 ring-gray-300 placeholder:text-gray-400 focus:ring-indigo-600',
    error: 'text-red-900 ring-red-300 placeholder:text-red-400 focus:ring-red-500',
    success: 'text-green-900 ring-green-300 placeholder:text-green-400 focus:ring-green-500'
  }

  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-3.5 py-2 text-base',
    lg: 'px-4 py-3 text-lg'
  }

  return [
    base,
    variants[props.variant],
    sizes[props.size],
    props.block ? 'w-full' : ''
  ].join(' ')
})
</script>

<!--

<Input /> component

Usage:
  <Input v-model="value" placeholder="Enter text" />
  <Input type="email" variant="error" placeholder="Invalid email" />
  <Input type="password" size="lg" block />
  <Input disabled placeholder="Disabled input" />

Props:
  modelValue : string | number  – bound value (use v-model)
  type       : 'text' | 'email' | 'password' | 'number' | 'tel' | 'url' | 'search'  – defaults to 'text'
  variant    : 'default' | 'error' | 'success'  – defaults to 'default'
  size       : 'sm' | 'md' | 'lg'  – defaults to 'md'
  placeholder: string  – placeholder text
  disabled   : boolean  – disables the input
  readonly   : boolean  – makes the input read-only
  block      : boolean  – makes the input full-width

Events:
  @update:modelValue(value) – emitted on input (use v-model)
  @blur(event)  – emitted when the input loses focus
  @focus(event) – emitted when the input gains focus

Styling:
  Uses TailwindCSS utility classes for a clean, minimal design.
  Focus and disabled states are included for accessibility.
-->
