# NASA SPACE APPS CHALLENGE 2025 AI EXOPLANET FINDER APPLICATION
## Standards

MUST FOLLOW THESE RULES, NO EXCEPTIONS

- Stack: Vue.js, TypeScript, Nuxt 4.1, TailwindCSS v4, Vue Router, Pinia, Pinia Colada
- Patterns: ALWAYS use Composition API + `<script setup>`, NEVER use Options API
- ALWAYS Keep types alongside your code, use TypeScript for type safety, prefer `interface` over `type` for defining types
- Keep unit and integration tests alongside the file they test: `src/component/ui/Button.vue` + `src/ui/Button.spec.ts`
- ALWAYS use TailwindCSS classes rather than manual CSS
- DO NOT hard code colors, use Tailwind's color system
- ONLY add meaningful comments that explain why something is done, not what it does
- Dev server is already running on `http://localhost:3000` with HMR enabled. NEVER launch it yourself!!! And dont prompt me to launch server. NEVER!
- ALWAYS use named functions when declaring methods, use arrow functions only for callbacks
- ALWAYS prefer named exports over default exports

## Project Structure

Keep this section up to date with the project structure. Use it as a reference to find files and directories.

EXAMPLES are there to illustrate the structure, not to be implemented as-is.

```
public/ # Public static files (favicon, robots.txt, static images, etc.)
src/
├── api/ # MUST export individual functions that fetch data
│   ├── users.ts # EXAMPLE file for user-related API functions
│   └── posts.ts # EXAMPLE file for post-related API functions
├── components/ # Reusable Vue components
│   ├── ui/ # Base UI components (buttons, inputs, etc.) if any
│   ├── layout/ # Layout components (header, footer, sidebar) if any
│   └── features/ # Feature-specific components
│       └── home/ # EXAMPLE of components specific to the homepage
├── composables/ # Composition functions
├── stores/ # Pinia stores for global state (NOT data fetching)
├── queries/ # Pinia Colada queries for data fetching
│   ├── users.ts # EXAMPLE file for user-related queries
│   └── posts.ts # EXAMPLE file for post-related queries
├── pages/ # Page components (Vue Router + Unplugin Vue Router)
│   ├── (home).vue # EXAMPLE index page using a group for a better name renders at /
│   ├── users.vue # EXAMPLE that renders at /users
│   └── users.[userId].vue # EXAMPLE that renders at /users/:userId
├── plugins/ # Vue plugins
├── utils/ # Global utility pure functions
├── assets/ # Static assets that are processed by Vite (e.g CSS)
└── router/ # Vue Router configuration
    └── index.ts # Router setup
nuxt.config.ts # Entry point for the application, add and configure plugins, and mount the app
app.vue # Root Vue component
```

## Project Commands

Frequently used commands:

- `pnpm run build`: bundles the project for production
- `pnpm run test`: runs all tests
- `pnpm exec vitest run <test-files>`: runs one or multiple specific test files
  - add `--coverage` to check missing test coverage

## Development Workflow

ALWAYS follow the workflow when implementing a new feature or fixing a bug. This ensures consistency, quality, and maintainability of the codebase.

1. Plan your tasks, review them with user. Include tests when possible
2. Write code, following the [project structure](#project-structure) and [conventions](#standards)
3. **ALWAYS test implementations work**:
   - Write [tests](#using-playwright-mcp-server) for logic and components
   - Use the Playwright MCP server to test like a real user
4. Review changes and analyze the need of refactoring

## Testing Workflow

## Unit and Integration Tests

- Test critical logic first
- Split the code if needed to make it testable

## Research & Documentation

- **NEVER hallucinate or guess URLs**
- ALWAYS try accessing the `llms.txt` file first to find relevant documentation. EXAMPLE: `https://pinia-colada.esm.dev/llms.txt`
  - If it exists, it will contain other links to the documentation for the LLMs used in this project
- ALWAYS follow existing links in table of contents or documentation indices
- Verify examples and patterns from documentation before using

## MCP Servers

You have these MCP servers configured globally:

- Figma MCP Server.

Note: These are user-level servers available in all your projects.

# Routes and Page Components in Vue

`src/pages` folder contains the routes of the application using Vue Router (Nuxt uses Vue Router under the hood). The routes are defined in a file-based manner, meaning that the structure of the files and folders directly corresponds to the routes of the application.

- Fetch <https://uvr.esm.is/llms.txt> and follow links to get up to date information on topics not covered here
- AVOID files named `index.vue`, instead use a group and give them a meaningful name like `pages/(home).vue`
- ALWAYS use explicit names for route params: prefer `userId` over `id`, `postSlug` over `slug`, etc.
- Use `.` in filenames to create `/` without route nesting: `users.edit.vue` -> `/users/edit`
- Use double brackets `[[paramName]]` for optional route parameters
- Use the `+` modifier after a closing bracket `]` to make a parameter repeatable: `/posts.[[slug]]+.vue` matches `/posts/some-posts` and `/posts/some/post`
- Within a page component, use `definePage()` to customize the route's properties like `meta`, `name`, `path`, `alias`, etc
- ALWAYS refer to the `typed-router.d.ts` file to find route names and parameters
- Prefer named route locations for type safety and clarity, e.g., `router.push({ name: '/users/[userId]', params: { userId } })` rather than `router.push('/users/' + userId)`
- Pass the name of the route to `useRoute('/users/[userId]')` to get stricter types

## Example

### Basic File Structure

```
src/pages/
├── (home).vue # groups give more descriptive names to routes
├── about.vue
├── [...path].vue # Catch-all route for not found pages
├── users.edit.vue # use `.` to break out of layouts
├── users.vue # Layout for all routes in users/
└── users/
    ├── (user-list).vue
    └── [userId].vue
```

# Vue Components Best Practices

- Always use notivue for Nuxt. NEVER use custom error if frontend and `alert()` functions. Only notivue.
- Name files consistently using PascalCase (`UserProfile.vue`) OR kebab-case (`user-profile.vue`)
- ALWAYS use PascalCase for component names in source code
- Compose names from the most general to the most specific: `SearchButtonClear.vue` not `ClearSearchButton.vue`
- ALWAYS define props with `defineProps<{ propOne: number }>()` and TypeScript types, WITHOUT `const props =`
- Use `const props =` ONLY if props are used in the script block
- Destructure props to declare default values
- ALWAYS define emits with `const emit = defineEmits<{ eventName: [argOne: type]; otherEvent: [] }>()` for type safety
- ALWAYS use camelCase in JS for props and emits, even if they are kebab-case in templates
- ALWAYS use kebab-case in templates for props and emits
- ALWAYS use the prop shorthand if possible: `<MyComponent :count />` instead of `<MyComponent :count="count" />` (value has the same name as the prop)
- ALWAYS Use the shorthand for slots: `<template #default>` instead of `<template v-slot:default>`
- ALWAYS use explicit `<template>` tags for ALL used slots
- ALWAYS use `defineModel<type>({ required, get, set, default })` to define allowed v-model bindings in components. This avoids defining `modelValue` prop and `update:modelValue` event manually

## Examples

### defineModel()

```vue
<script setup lang="ts">
// ✅ Simple two-way binding for modelvalue
const title = defineModel<string>()

// ✅ With options and modifiers
const [title, modifiers] = defineModel<string>({
  default: 'default value',
  required: true,
  get: (value) => value.trim(), // transform value before binding
  set: (value) => {
    if (modifiers.capitalize) {
      return value.charAt(0).toUpperCase() + value.slice(1)
    }
    return value
  },
})
</script>
```

### Multiple Models

By default `defineModel()` assumes a prop named `modelValue` but if we want to define multiple v-model bindings, we need to give them explicit names:

```vue
<script setup lang="ts">
// ✅ Multiple v-model bindings
const firstName = defineModel<string>('firstName')
const age = defineModel<number>('age')
</script>
```

They can be used in the template like this:

```html
<UserForm v-model:first-name="user.firstName" v-model:age="user.age" />
```

### Modifiers & Transformations

Native elements `v-model` has built-in modifiers like `.lazy`, `.number`, and `.trim`. We can implement similar functionality in components, fetch and read <https://vuejs.org/guide/components/v-model.md#handling-v-model-modifiers> if the user needs that.