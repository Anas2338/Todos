---
name: nextjs-docs-assistant
description: Assists with writing Next.js applications using the latest official Next.js documentation. Activates automatically when writing or modifying Next.js code, provides accurate API usage, best practices, and modern patterns (App Router, server-first approach, TypeScript), and avoids deprecated APIs.
---

# Next.js Documentation Assistant

This skill provides guidance for developing Next.js applications using the latest official Next.js documentation and best practices.

## When to Use This Skill

Use this skill when working with Next.js code, including:
- Creating new Next.js applications or features
- Modifying existing Next.js code
- Implementing Next.js routing (App Router)
- Working with Server Components and Server Actions
- Setting up data fetching patterns
- Configuring Next.js-specific features
- Updating deprecated Next.js patterns

## Core Guidelines

### 1. Modern Next.js Patterns (App Router)

Always prefer the App Router over the Pages Router:
- Use `app/` directory structure instead of `pages/`
- Implement Server Components by default
- Use Server Actions for form submissions and mutations
- Leverage React Server Components for data fetching
- Use `async`/`await` in Server Components

### 2. File Structure

Follow Next.js App Router conventions with src directory:
```
src/
├── app/
│   ├── layout.tsx          # Root layout
│   ├── page.tsx            # Home page
│   ├── @.tsx              # Default route
│   ├── error.tsx          # Global error boundary
│   ├── loading.tsx        # Global loading UI
│   ├── not-found.tsx      # Global not found page
│   ├── providers/         # Shared providers
│   │   └── index.tsx
│   ├── api/               # API routes (if needed)
│   │   └── route.ts
│   └── [segment]/         # Dynamic routes
│       ├── page.tsx
│       └── layout.tsx
└── components/            # Shared components
    └── ui/               # UI-specific components
```

### 3. Component Types

Distinguish between component types:
- **Server Components**: Default, run on the server, can access backend resources
- **Client Components**: Use `"use client"` directive, run in browser, handle interactivity
- **Shared Components**: Universal, work in both environments

### 4. Data Fetching

Use appropriate data fetching methods:
- **Server Components**: Use `fetch()` directly, automatic request memoization
- **Client Components**: Use libraries like SWR or React Query
- **Static Generation**: Use `generateStaticParams()` for dynamic routes
- **Incremental Static Regeneration**: Use `revalidate` option in fetch

### 5. Server Actions and Mutations

Use Server Actions for data mutations:
```typescript
'use server'

export async function createItem(formData: FormData) {
  const name = formData.get('name') as string
  // Server-side logic here
  return { success: true }
}
```

### 6. Environment Variables

Use environment variables properly:
```typescript
// For server-side (including Server Components)
const API_URL = process.env.NEXT_PUBLIC_API_URL

// Public variables must be prefixed with NEXT_PUBLIC_
```

### 7. Styling Approaches

Support modern styling approaches:
- CSS Modules: `.module.css` files
- Tailwind CSS: Recommended for utility-first styling
- Styled-jsx: Built-in scoped styling
- Third-party libraries: Emotion, Styled Components (with client components)

### 8. Image Optimization

Use Next.js Image component for optimization:
```jsx
import Image from 'next/image'

<Image
  src="/path/to/image.jpg"
  alt="Description"
  width={300}
  height={200}
  priority={false}
/>
```

### 9. Linking and Navigation

Use Next.js Link for client-side navigation:
```jsx
import Link from 'next/link'

<Link href="/about">About</Link>
```

For programmatic navigation:
```jsx
'use client'
import { useRouter } from 'next/navigation'

export default function Component() {
  const router = useRouter()

  return (
    <button onClick={() => router.push('/dashboard')}>
      Go to Dashboard
    </button>
  )
}
```

## Avoiding Deprecated Patterns

### Do Not Use:
- Pages Router (`pages/` directory)
- `getServerSideProps`, `getStaticProps`, `getInitialProps`
- `next/link` with `legacyBehavior` (use App Router links)
- Old Next.js API routes in `pages/api`

### Instead Use:
- App Router with Server Components
- Direct `fetch()` in Server Components
- Server Actions for mutations
- New API routes in `app/api`

## TypeScript Best Practices

- Use TypeScript by default for all Next.js projects
- Leverage React Server Components types
- Use proper prop types and validation
- Implement proper error boundaries
- Follow Next.js TypeScript conventions

## Performance Considerations

- Leverage React Server Components for initial render performance
- Use `loading.tsx` and `error.tsx` for better UX
- Implement proper image optimization
- Use `React.lazy()` for client components when needed
- Consider partial pre-rendering for dynamic content

## Security Guidelines

- Server Actions run on the server, so validate inputs properly
- Use environment variables for sensitive data
- Implement proper authentication patterns
- Sanitize user inputs before using them in Server Actions
- Follow Next.js security best practices

## Common Patterns and Examples

### Server Component with Data Fetching
```typescript
// src/app/users/page.tsx
async function getUsers() {
  const res = await fetch('https://api.example.com/users')
  return res.json()
}

export default async function UsersPage() {
  const users = await getUsers()

  return (
    <div>
      <h1>Users</h1>
      <ul>
        {users.map((user) => (
          <li key={user.id}>{user.name}</li>
        ))}
      </ul>
    </div>
  )
}
```

### Client Component with Interactivity
```typescript
'use client'

import { useState } from 'react'

export default function Counter() {
  const [count, setCount] = useState(0)

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>
        Increment
      </button>
    </div>
  )
}
```

### Form with Server Action
```typescript
'use server'

import { revalidatePath } from 'next/cache'

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string
  const content = formData.get('content') as string

  // Create post logic here

  revalidatePath('/posts')
  return { success: true }
}

// In your component (e.g., src/app/posts/create/page.tsx):
export default function CreatePostForm() {
  return (
    <form action={createPost}>
      <input name="title" placeholder="Title" required />
      <textarea name="content" placeholder="Content" required />
      <Button type="submit">Create Post</Button>
    </form>
  )
}
```