<template>
  <button
    :type="type"
    :disabled="disabled || loading"
    :class="buttonClasses"
    @click="$emit('click', $event)"
  >
    <span v-if="loading" class="mr-2 animate-spin h-4 w-4 border-2 border-current border-t-transparent rounded-full" />
    <slot />
  </button>
</template>

<script setup lang="ts">
interface Props {
  type?: 'button' | 'submit' | 'reset'
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean
  loading?: boolean
  block?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  type: 'button',
  variant: 'primary',
  size: 'md',
  disabled: false,
  loading: false,
  block: false
})

const emit = defineEmits<{
  click: [event: Event]
}>()

const buttonClasses = computed(() => {
  const base = 'inline-flex items-center cursor-pointer justify-center font-medium rounded-md transition focus:outline-none focus:ring-1 focus:ring-offset-2 focus:ring-offset-zinc-900 disabled:opacity-50 disabled:cursor-not-allowed'
  
  const variants = {
    primary: 'bg-zinc-100 text-zinc-900 hover:bg-zinc-200 focus:ring-zinc-300',
    secondary: 'bg-zinc-800 text-zinc-100 hover:bg-zinc-700 focus:ring-zinc-600',
    outline: 'border border-zinc-700 bg-transparent text-zinc-100 hover:bg-zinc-800 focus:ring-zinc-600',
    ghost: 'bg-transparent text-zinc-100 hover:bg-zinc-800 focus:ring-zinc-600'
  }
  
  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg'
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

<Button /> component

Usage:
  <Button>Click me</Button>
  <Button variant="secondary" size="lg">Large Secondary</Button>
  <Button loading>Loading...</Button>
  <Button block>Full Width</Button>

Props:
  type     : 'button' | 'submit' | 'reset'  – defaults to 'button'
  variant  : 'primary' | 'secondary' | 'outline' | 'ghost'  – defaults to 'primary'
  size     : 'sm' | 'md' | 'lg'  – defaults to 'md'
  disabled : boolean  – disables the button
  loading  : boolean  – shows spinner and disables the button
  block    : boolean  – makes the button full-width

Events:
  @click(event) – emitted when the button is clicked (not fired when disabled or loading)

Styling:
  Uses TailwindCSS utility classes for a clean, minimal design.
  Focus styles are included for accessibility.
-->
