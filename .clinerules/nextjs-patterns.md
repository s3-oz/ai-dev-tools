---
description: Best practices and patterns for Next.js development across all projects
author: AI-Dev-Tools
version: 1.0
tags: ["nextjs", "react", "frontend", "ssr", "ssg", "patterns"]
globs: ["**/*.jsx", "**/*.tsx", "**/*.js", "**/*.ts"]
---

# Next.js Best Practices and Patterns

## Purpose

This rule defines consistent patterns and best practices for Next.js development across all projects. It extends the [React Patterns](./react-patterns.md) with Next.js-specific guidelines to ensure maintainable, performant, and accessible Next.js applications with a consistent architecture.

## Guidelines

### Core Principles

- **All React Patterns Apply**: Follow all patterns from the [React Patterns](./react-patterns.md) document
- **Server-First Mindset**: Leverage Next.js server capabilities for performance and SEO
- **Progressive Enhancement**: Build with progressive enhancement in mind
- **Type Safety**: Use TypeScript for all Next.js projects
- **Accessibility**: Ensure all components are accessible

### Project Structure

#### App Router (Preferred for New Projects)

- Use the App Router for new projects (Next.js 13+)
- Follow the file-based routing convention:
  ```
  app/
  ├── layout.tsx       # Root layout
  ├── page.tsx         # Home page
  ├── about/
  │   └── page.tsx     # About page
  ├── blog/
  │   ├── page.tsx     # Blog index
  │   └── [slug]/
  │       └── page.tsx # Blog post
  ```

- Use route groups for organization:
  ```
  app/
  ├── (marketing)/     # Route group (doesn't affect URL)
  │   ├── about/
  │   │   └── page.tsx
  │   └── contact/
  │       └── page.tsx
  ├── (shop)/
  │   ├── products/
  │   │   └── page.tsx
  │   └── cart/
  │       └── page.tsx
  ```

- Organize components by feature and type:
  ```
  components/
  ├── ui/              # Reusable UI components
  │   ├── Button.tsx
  │   └── Card.tsx
  ├── features/        # Feature-specific components
  │   ├── auth/
  │   └── products/
  └── layouts/         # Layout components
      ├── Header.tsx
      └── Footer.tsx
  ```

#### Pages Router (Legacy Projects)

- For legacy projects, follow the pages directory structure:
  ```
  pages/
  ├── index.tsx        # Home page
  ├── about.tsx        # About page
  ├── blog/
  │   ├── index.tsx    # Blog index
  │   └── [slug].tsx   # Blog post
  ```

### Data Fetching

#### App Router

- Use Server Components by default for data fetching:
  ```tsx
  // app/users/page.tsx
  async function getUsers() {
    const res = await fetch('https://api.example.com/users');
    return res.json();
  }

  export default async function UsersPage() {
    const users = await getUsers();
    return (
      <div>
        <h1>Users</h1>
        <ul>
          {users.map(user => (
            <li key={user.id}>{user.name}</li>
          ))}
        </ul>
      </div>
    );
  }
  ```

- Use `use client` directive only when necessary:
  ```tsx
  'use client';

  import { useState } from 'react';

  export default function Counter() {
    const [count, setCount] = useState(0);
    return (
      <button onClick={() => setCount(count + 1)}>
        Count: {count}
      </button>
    );
  }
  ```

- Use React Cache for data fetching:
  ```tsx
  import { cache } from 'react';

  export const getUser = cache(async (id: string) => {
    const res = await fetch(`https://api.example.com/users/${id}`);
    return res.json();
  });
  ```

#### Pages Router

- Use `getStaticProps` for content that can be generated at build time:
  ```tsx
  export async function getStaticProps() {
    const res = await fetch('https://api.example.com/posts');
    const posts = await res.json();
    
    return {
      props: {
        posts,
      },
      revalidate: 60, // Regenerate page every 60 seconds
    };
  }
  ```

- Use `getServerSideProps` for content that must be fetched at request time:
  ```tsx
  export async function getServerSideProps(context) {
    const { params, req, res } = context;
    const userData = await fetchUserData(params.id);
    
    return {
      props: {
        user: userData,
      },
    };
  }
  ```

- Use SWR or React Query for client-side data fetching:
  ```tsx
  import useSWR from 'swr';

  function Profile() {
    const { data, error } = useSWR('/api/user', fetcher);
    
    if (error) return <div>Failed to load</div>;
    if (!data) return <div>Loading...</div>;
    
    return <div>Hello {data.name}!</div>;
  }
  ```

### API Routes

#### App Router

- Use Route Handlers for API endpoints:
  ```tsx
  // app/api/users/route.ts
  import { NextResponse } from 'next/server';

  export async function GET() {
    const users = await fetchUsers();
    return NextResponse.json(users);
  }

  export async function POST(request: Request) {
    const data = await request.json();
    const newUser = await createUser(data);
    return NextResponse.json(newUser, { status: 201 });
  }
  ```

#### Pages Router

- Use API Routes for backend functionality:
  ```tsx
  // pages/api/users.ts
  import type { NextApiRequest, NextApiResponse } from 'next';

  export default async function handler(
    req: NextApiRequest,
    res: NextApiResponse
  ) {
    if (req.method === 'GET') {
      const users = await fetchUsers();
      res.status(200).json(users);
    } else if (req.method === 'POST') {
      const newUser = await createUser(req.body);
      res.status(201).json(newUser);
    } else {
      res.setHeader('Allow', ['GET', 'POST']);
      res.status(405).end(`Method ${req.method} Not Allowed`);
    }
  }
  ```

### Metadata and SEO

#### App Router

- Use the Metadata API for SEO:
  ```tsx
  // app/blog/[slug]/page.tsx
  import type { Metadata } from 'next';

  export async function generateMetadata({ params }): Promise<Metadata> {
    const post = await getPost(params.slug);
    
    return {
      title: post.title,
      description: post.excerpt,
      openGraph: {
        title: post.title,
        description: post.excerpt,
        images: [{ url: post.image }],
      },
    };
  }
  ```

#### Pages Router

- Use Next.js Head component for SEO:
  ```tsx
  import Head from 'next/head';

  export default function BlogPost({ post }) {
    return (
      <>
        <Head>
          <title>{post.title}</title>
          <meta name="description" content={post.excerpt} />
          <meta property="og:title" content={post.title} />
          <meta property="og:description" content={post.excerpt} />
          <meta property="og:image" content={post.image} />
        </Head>
        <article>{/* Post content */}</article>
      </>
    );
  }
  ```

### Image Optimization

- Use Next.js Image component for optimized images:
  ```tsx
  import Image from 'next/image';

  export default function Avatar() {
    return (
      <Image
        src="/profile.jpg"
        alt="Profile picture"
        width={64}
        height={64}
        priority
      />
    );
  }
  ```

### Navigation

- Use Next.js Link component for client-side navigation:
  ```tsx
  import Link from 'next/link';

  export default function Navigation() {
    return (
      <nav>
        <Link href="/">Home</Link>
        <Link href="/about">About</Link>
        <Link href="/blog">Blog</Link>
      </nav>
    );
  }
  ```

- Use `useRouter` for programmatic navigation:
  ```tsx
  'use client'; // For App Router

  import { useRouter } from 'next/navigation'; // or 'next/router' for Pages Router

  export default function LoginForm() {
    const router = useRouter();
    
    const handleSubmit = async (e) => {
      e.preventDefault();
      const success = await login(/* form data */);
      if (success) {
        router.push('/dashboard');
      }
    };
    
    return <form onSubmit={handleSubmit}>{/* Form fields */}</form>;
  }
  ```

### State Management

- Use React Context for global state in smaller applications:
  ```tsx
  // contexts/AuthContext.tsx
  'use client';

  import { createContext, useContext, useState } from 'react';

  const AuthContext = createContext(null);

  export function AuthProvider({ children }) {
    const [user, setUser] = useState(null);
    
    const login = async (credentials) => {
      // Login logic
      setUser(userData);
    };
    
    const logout = () => {
      // Logout logic
      setUser(null);
    };
    
    return (
      <AuthContext.Provider value={{ user, login, logout }}>
        {children}
      </AuthContext.Provider>
    );
  }

  export function useAuth() {
    return useContext(AuthContext);
  }
  ```

- Consider Redux, Zustand, or Jotai for more complex state management

### Error Handling

#### App Router

- Use error.tsx files for error boundaries:
  ```tsx
  'use client';

  export default function Error({
    error,
    reset,
  }: {
    error: Error;
    reset: () => void;
  }) {
    return (
      <div>
        <h2>Something went wrong!</h2>
        <p>{error.message}</p>
        <button onClick={() => reset()}>Try again</button>
      </div>
    );
  }
  ```

- Use not-found.tsx for 404 pages:
  ```tsx
  export default function NotFound() {
    return (
      <div>
        <h2>Page Not Found</h2>
        <p>The page you are looking for does not exist.</p>
      </div>
    );
  }
  ```

#### Pages Router

- Use custom error pages:
  ```tsx
  // pages/404.tsx
  export default function Custom404() {
    return <h1>404 - Page Not Found</h1>;
  }

  // pages/500.tsx
  export default function Custom500() {
    return <h1>500 - Server Error</h1>;
  }
  ```

### Performance Optimization

- Use dynamic imports for code splitting:
  ```tsx
  import dynamic from 'next/dynamic';

  const DynamicComponent = dynamic(() => import('../components/HeavyComponent'), {
    loading: () => <p>Loading...</p>,
    ssr: false, // Disable server-side rendering if needed
  });
  ```

- Use Suspense for loading states:
  ```tsx
  import { Suspense } from 'react';
  import Loading from './loading';
  import Comments from './Comments';

  export default function Post() {
    return (
      <article>
        <h1>My Post</h1>
        <Suspense fallback={<Loading />}>
          <Comments />
        </Suspense>
      </article>
    );
  }
  ```

### Testing

- Use Jest and React Testing Library for unit and component testing
- Use Cypress or Playwright for end-to-end testing
- Test both client and server components

## Examples

### Good App Router Page Example

```tsx
// app/blog/[slug]/page.tsx
import { notFound } from 'next/navigation';
import { Suspense } from 'react';
import PostContent from '@/components/features/blog/PostContent';
import CommentSection from '@/components/features/blog/CommentSection';
import RelatedPosts from '@/components/features/blog/RelatedPosts';
import Loading from './loading';

async function getPost(slug: string) {
  const res = await fetch(`https://api.example.com/posts/${slug}`, {
    next: { revalidate: 3600 } // Revalidate every hour
  });
  
  if (!res.ok) {
    return null;
  }
  
  return res.json();
}

export async function generateMetadata({ params }) {
  const post = await getPost(params.slug);
  
  if (!post) {
    return {
      title: 'Post Not Found',
      description: 'The requested post could not be found.'
    };
  }
  
  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      images: [{ url: post.image }],
    },
  };
}

export default async function BlogPost({ params }) {
  const post = await getPost(params.slug);
  
  if (!post) {
    notFound();
  }
  
  return (
    <article>
      <PostContent post={post} />
      
      <Suspense fallback={<Loading />}>
        <CommentSection postId={post.id} />
      </Suspense>
      
      <Suspense fallback={<Loading />}>
        <RelatedPosts tags={post.tags} currentPostId={post.id} />
      </Suspense>
    </article>
  );
}
```

### Good Pages Router Page Example

```tsx
// pages/blog/[slug].tsx
import { GetStaticProps, GetStaticPaths } from 'next';
import Head from 'next/head';
import { useRouter } from 'next/router';
import PostContent from '@/components/features/blog/PostContent';
import CommentSection from '@/components/features/blog/CommentSection';
import RelatedPosts from '@/components/features/blog/RelatedPosts';

export const getStaticPaths: GetStaticPaths = async () => {
  const res = await fetch('https://api.example.com/posts');
  const posts = await res.json();
  
  const paths = posts.map((post) => ({
    params: { slug: post.slug },
  }));
  
  return { paths, fallback: 'blocking' };
};

export const getStaticProps: GetStaticProps = async ({ params }) => {
  const res = await fetch(`https://api.example.com/posts/${params.slug}`);
  
  if (!res.ok) {
    return {
      notFound: true,
    };
  }
  
  const post = await res.json();
  
  return {
    props: {
      post,
    },
    revalidate: 3600, // Revalidate every hour
  };
};

export default function BlogPost({ post }) {
  const router = useRouter();
  
  if (router.isFallback) {
    return <div>Loading...</div>;
  }
  
  return (
    <>
      <Head>
        <title>{post.title}</title>
        <meta name="description" content={post.excerpt} />
        <meta property="og:title" content={post.title} />
        <meta property="og:description" content={post.excerpt} />
        <meta property="og:image" content={post.image} />
      </Head>
      
      <article>
        <PostContent post={post} />
        <CommentSection postId={post.id} />
        <RelatedPosts tags={post.tags} currentPostId={post.id} />
      </article>
    </>
  );
}
```

## Special Cases and Exceptions

- **Legacy Projects**: When working with existing Next.js projects using the Pages Router, follow the Pages Router patterns for consistency.
- **Hybrid Approach**: When migrating from Pages Router to App Router, you may need to use a hybrid approach temporarily.
- **Static Export**: For projects using `next export`, some features like API Routes and Image Optimization may have limitations.

## Related Rules

- [React Patterns](./react-patterns.md): Core React patterns that apply to all Next.js projects
- [Coding Standards](./coding-standards.md): General coding standards that apply to all code

## References

- [Next.js Documentation](https://nextjs.org/docs)
- [Next.js App Router Documentation](https://nextjs.org/docs/app)
- [Next.js Pages Router Documentation](https://nextjs.org/docs/pages)
- [Vercel Blog](https://vercel.com/blog)

## Changelog

- v1.0 (2025-05-18): Initial version
