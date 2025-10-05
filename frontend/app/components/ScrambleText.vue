<script setup lang="ts">
import { onMounted, onUnmounted, watch, useTemplateRef, nextTick } from 'vue';
import { gsap } from 'gsap';
import { SplitText } from 'gsap/SplitText';
import { ScrambleTextPlugin } from 'gsap/ScrambleTextPlugin';

gsap.registerPlugin(SplitText, ScrambleTextPlugin);

interface ScrambleTextProps {
  radius?: number;
  duration?: number;
  speed?: number;
  scrambleChars?: string;
  className?: string;
  style?: Record<string, string | number>;
  trigger?: 'hover' | 'auto' | 'click' | 'mousemove';
  autoDelay?: number;
  glowEffect?: boolean;
  staggerDelay?: number;
  animateOnMount?: boolean;
  tag?: string;
}

const props = withDefaults(defineProps<ScrambleTextProps>(), {
  radius: 100,
  duration: 1.2,
  speed: 0.5,
  scrambleChars: '!<>-_\\/[]{}—=+*^?#________',
  className: '',
  style: () => ({}),
  trigger: 'mousemove',
  autoDelay: 2000,
  glowEffect: false,
  staggerDelay: 0.02,
  animateOnMount: false,
  tag: 'p'
});

const rootRef = useTemplateRef<HTMLDivElement>('rootRef');

let splitText: SplitText | null = null;
let handleMove: ((e: PointerEvent) => void) | null = null;
let handleHover: (() => void) | null = null;
let handleClick: (() => void) | null = null;
let autoTimeout: ReturnType<typeof setTimeout> | null = null;

const scrambleText = (chars?: HTMLElement[], customDuration?: number) => {
  if (!splitText) return;
  
  const elements = chars || splitText.chars;
  
  elements.forEach((el, index) => {
    const c = el as HTMLElement;
    gsap.to(c, {
      delay: props.staggerDelay * index,
      duration: customDuration || props.duration,
      scrambleText: {
        text: c.dataset.content || '',
        chars: props.scrambleChars,
        speed: props.speed
      },
      ease: 'power2.out'
    });
  });
};

const initializeScrambleText = async () => {
  if (!rootRef.value) return;

  await nextTick();
  
  const textElement = rootRef.value.querySelector(props.tag);
  if (!textElement) return;

  splitText = new SplitText(textElement, {
    type: 'chars',
    charsClass: 'inline-block will-change-transform'
  });

  splitText.chars.forEach(el => {
    const c = el as HTMLElement;
    gsap.set(c, { 
      attr: { 'data-content': c.innerHTML },
      transformOrigin: 'center center'
    });
    
    if (props.glowEffect) {
      c.style.textShadow = '0 0 10px currentColor';
      c.style.transition = 'text-shadow 0.3s ease';
    }
  });

  // Set up event handlers based on trigger type
  if (props.trigger === 'mousemove') {
    handleMove = (e: PointerEvent) => {
      if (!splitText) return;

      splitText.chars.forEach(el => {
        const c = el as HTMLElement;
        const { left, top, width, height } = c.getBoundingClientRect();
        const dx = e.clientX - (left + width / 2);
        const dy = e.clientY - (top + height / 2);
        const dist = Math.hypot(dx, dy);

        if (dist < props.radius) {
          gsap.to(c, {
            overwrite: true,
            duration: props.duration * (1 - dist / props.radius),
            scrambleText: {
              text: c.dataset.content || '',
              chars: props.scrambleChars,
              speed: props.speed
            },
            ease: 'power2.out'
          });
        }
      });
    };
    rootRef.value.addEventListener('pointermove', handleMove);
  } else if (props.trigger === 'hover') {
    handleHover = () => scrambleText();
    rootRef.value.addEventListener('mouseenter', handleHover);
  } else if (props.trigger === 'click') {
    handleClick = () => scrambleText();
    rootRef.value.addEventListener('click', handleClick);
  } else if (props.trigger === 'auto') {
    const runAutoScramble = () => {
      scrambleText();
      autoTimeout = setTimeout(runAutoScramble, props.autoDelay);
    };
    autoTimeout = setTimeout(runAutoScramble, props.autoDelay);
  }

  // Animate on mount if requested
  if (props.animateOnMount) {
    setTimeout(() => scrambleText(), 100);
  }
};

const cleanup = () => {
  if (rootRef.value) {
    if (handleMove) rootRef.value.removeEventListener('pointermove', handleMove);
    if (handleHover) rootRef.value.removeEventListener('mouseenter', handleHover);
    if (handleClick) rootRef.value.removeEventListener('click', handleClick);
  }
  
  if (autoTimeout) {
    clearTimeout(autoTimeout);
    autoTimeout = null;
  }
  
  if (splitText) {
    splitText.revert();
    splitText = null;
  }
  
  handleMove = null;
  handleHover = null;
  handleClick = null;
};

onMounted(() => {
  initializeScrambleText();
});

onUnmounted(() => {
  cleanup();
});

watch([() => props.radius, () => props.duration, () => props.speed, () => props.scrambleChars, () => props.trigger], () => {
  cleanup();
  initializeScrambleText();
});
</script>

<template>
  <div ref="rootRef" :class="`scramble-text ${className}`" :style="style">
    <component :is="tag" :class="glowEffect ? 'glow-text' : ''">
      <slot></slot>
    </component>
  </div>
</template>

<style scoped>
.glow-text {
  text-shadow: 0 0 10px currentColor, 0 0 20px currentColor, 0 0 30px currentColor;
  transition: text-shadow 0.3s ease;
}

.scramble-text {
  cursor: default;
}

.scramble-text:hover .glow-text {
  text-shadow: 0 0 15px currentColor, 0 0 25px currentColor, 0 0 35px currentColor;
}
</style>