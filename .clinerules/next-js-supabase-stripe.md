---
description: "A comprehensive guide and workflow for integrating Next.js, Supabase (OAuth), and Stripe to build SaaS applications. Includes setup, configuration, code examples, and best practices."
author: "Cline (AI Assistant)"
version: "1.0"
tags: ["nextjs", "supabase", "stripe", "oauth", "saas", "fullstack", "workflow", "guide", "integration", "typescript"]
globs: ["/next.config.{js,ts}", "/middleware.{js,ts}", "/app/api//.ts", "/utils/supabase/.ts", ".env.local", "/app/auth/callback/route.ts"]
---

# Next.js, Supabase (OAuth), and Stripe for SaaS Applications ("20 Minute SaaS")

*Objective:* This rule provides a comprehensive, step-by-step guide and reference for setting up a Software-as-a-Service (SaaS) application using Next.js (App Router), Supabase for authentication (with a focus on OAuth providers), and Stripe for subscription management. The aim is to streamline the development process, inspired by the "20 Minute SaaS" concept for efficiency.

*Cline Usage:* Cline SHOULD use this rule as a primary reference when assisting users in building SaaS applications with this stack. This includes generating code snippets, explaining configuration steps, troubleshooting integration issues, and advising on best practices.

## I. Prerequisites and Initial Setup

Before starting, ensure you have the following:

*   *Node.js:* LTS version or higher.
*   *Package Manager:* npm, yarn, or pnpm.
*   *Supabase Account:* Create an account at [supabase.com](https://supabase.com) and set up a new project.
    *   Note your Project URL and anon key.
*   *Stripe Account:* Create an account at [stripe.com](https://stripe.com).
    *   Access your API keys (publishable and secret).
    *   Set up your business details and branding in the Stripe dashboard.

## II. Next.js Project Initialization

Bootstrap your Next.js application using the create-next-app CLI.

bash
npx create-next-app@latest my-saas-app --ts --tailwind --eslint --app --src-dir
# Follow the prompts, selecting preferred options.
# --ts: TypeScript
# --tailwind: Tailwind CSS
# --eslint: ESLint
# --app: App Router
# --src-dir: Use src/ directory


Navigate into your project directory: cd my-saas-app

## III. Supabase Authentication (OAuth Focus)

Integrate Supabase for robust user authentication.

### 1. Install Supabase Packages

bash
npm install @supabase/supabase-js @supabase/ssr
# or
yarn add @supabase/supabase-js @supabase/ssr
# or
pnpm add @supabase/supabase-js @supabase/ssr

The @supabase/ssr package provides helpers for server-side rendering and App Router integration.

### 2. Configure Environment Variables

Create a .env.local file in your project root and add your Supabase credentials:

env
NEXT_PUBLIC_SUPABASE_URL=YOUR_SUPABASE_PROJECT_URL
NEXT_PUBLIC_SUPABASE_ANON_KEY=YOUR_SUPABASE_ANON_KEY
SUPABASE_SERVICE_ROLE_KEY=YOUR_SUPABASE_SERVICE_ROLE_KEY # Optional, for admin tasks

*Security Note:* NEXT_PUBLIC_ variables are exposed to the browser. The SUPABASE_SERVICE_ROLE_KEY MUST NOT be prefixed with NEXT_PUBLIC_ and should only be used in secure server-side environments.

### 3. Set up OAuth Providers in Supabase

1.  Go to your Supabase project dashboard.
2.  Navigate to "Authentication" -> "Providers".
3.  Enable and configure your desired OAuth providers (e.g., Google, GitHub, GitLab).
    *   You'll need to provide Client ID and Client Secret from the respective OAuth provider's developer console.
    *   *Crucially, set the "Redirect URI"* in your OAuth provider's settings to:
        YOUR_SUPABASE_PROJECT_URL/auth/v1/callback
    *   Supabase handles the OAuth flow and redirects back to your application. You will define this application callback route later.

### 4. Create Supabase Client Utilities

Create utility files to instantiate Supabase clients for different contexts.

*Client Component Client:*
src/utils/supabase/client.ts
typescript
import { createBrowserClient } from '@supabase/ssr'

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  )
}


*Server Component / Route Handler / Server Action Client:*
src/utils/supabase/server.ts
typescript
import { createServerClient, type CookieOptions } from '@supabase/ssr'
import { cookies } from 'next/headers'

export function createServerSupabaseClient() {
  const cookieStore = cookies()

  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        get(name: string) {
          return cookieStore.get(name)?.value
        },
        set(name:string, value: string, options: CookieOptions) {
          try {
            cookieStore.set({ name, value, ...options })
          } catch (error) {
            // The `set` method was called from a Server Component.
            // This can be ignored if you have middleware refreshing
            // user sessions.
          }
        },
        remove(name: string, options: CookieOptions) {
          try {
            cookieStore.set({ name, value: '', ...options })
          } catch (error) {
            // The `delete` method was called from a Server Component.
            // This can be ignored if you have middleware refreshing
            // user sessions.
          }
        },
      },
    }
  )
}


### 5. Implement Middleware for Session Management

Create a middleware file to manage user sessions and refresh tokens.
src/middleware.ts
typescript
import { createServerClient, type CookieOptions } from '@supabase/ssr'
import { NextResponse, type NextRequest } from 'next/server'

export async function middleware(request: NextRequest) {
  let response = NextResponse.next({
    request: {
      headers: request.headers,
    },
  })

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        get(name: string) {
          return request.cookies.get(name)?.value
        },
        set(name: string, value: string, options: CookieOptions) {
          request.cookies.set({
            name,
            value,
            ...options,
          })
          response = NextResponse.next({
            request: {
              headers: request.headers,
            },
          })
          response.cookies.set({
            name,
            value,
            ...options,
          })
        },
        remove(name: string, options: CookieOptions) {
          request.cookies.set({
            name,
            value: '',
            ...options,
          })
          response = NextResponse.next({
            request: {
              headers: request.headers,
            },
          })
          response.cookies.set({
            name,
            value: '',
            ...options,
          })
        },
      },
    }
  )

  // IMPORTANT: Avoid running middleware on static assets and API routes
  if (
    request.nextUrl.pathname.startsWith('/_next') ||
    request.nextUrl.pathname.startsWith('/api') || // Exclude all API routes
    request.nextUrl.pathname.startsWith('/static') ||
    /\.(.*)$/.test(request.nextUrl.pathname) // Exclude files with extensions
  ) {
    return response
  }

  await supabase.auth.getSession() // Refreshes the session cookie

  return response
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * Feel free to modify this pattern to include more paths.
     */
    '/((?!_next/static|_next/image|favicon.ico|auth).*)', // Exclude /auth routes from middleware session refresh if they handle redirects
  ],
}

*Note:* The matcher config in middleware.ts is crucial. Adjust it to ensure it doesn't interfere with Supabase's own auth routes or static file serving.

### 6. Create Application Auth Callback Route

When a user authenticates via an OAuth provider, Supabase redirects them to YOUR_SUPABASE_PROJECT_URL/auth/v1/callback. After Supabase processes this, it redirects the user back to your application at a URL you specify in the Supabase Dashboard (Authentication -> URL Configuration -> Site URL and Additional Redirect URLs). A common pattern is to use a route like /auth/callback.

Create src/app/auth/callback/route.ts:
typescript
import { createServerSupabaseClient } from '@/utils/supabase/server'
import { NextResponse } from 'next/server'
import { NextRequest } from 'next/server'

export async function GET(request: NextRequest) {
  const { searchParams, origin } = new URL(request.url)
  const code = searchParams.get('code')
  // if "next" is in param, use it as the redirect URL
  const next = searchParams.get('next') ?? '/'

  if (code) {
    const supabase = createServerSupabaseClient()
    const { error } = await supabase.auth.exchangeCodeForSession(code)
    if (!error) {
      return NextResponse.redirect(`${origin}${next}`)
    }
  }

  // return the user to an error page with instructions
  console.error('Error exchanging code for session or no code found');
  return NextResponse.redirect(`${origin}/auth/auth-code-error`)
}

Ensure your "Site URL" in Supabase Auth settings (e.g., http://localhost:3000) is correct for local development. For production, update this to your production URL.

### 7. Implement OAuth Login UI

In your frontend components, provide buttons to initiate OAuth login.

Example: src/components/LoginButtons.tsx
tsx
'use client'

import { createClient } from '@/utils/supabase/client'

export default function LoginButtons() {
  const supabase = createClient()

  const handleGoogleLogin = async () => {
    await supabase.auth.signInWithOAuth({
      provider: 'google',
      options: {
        redirectTo: `${window.location.origin}/auth/callback`, // Supabase redirects here after its own /auth/v1/callback
      },
    })
  }

  const handleGitHubLogin = async () => {
    await supabase.auth.signInWithOAuth({
      provider: 'github',
      options: {
        redirectTo: `${window.location.origin}/auth/callback`,
      },
    })
  }

  return (
    <div>
      <button onClick={handleGoogleLogin}>Login with Google</button>
      <button onClick={handleGitHubLogin}>Login with GitHub</button>
    </div>
  )
}


### 8. Protect Pages and Server-Side Auth

To protect pages, check for an active session in Server Components.

Example: src/app/dashboard/page.tsx
tsx
import { createServerSupabaseClient } from '@/utils/supabase/server'
import { redirect } from 'next/navigation'

export default async function DashboardPage() {
  const supabase = createServerSupabaseClient()

  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    return redirect('/login') // Or your login page
  }

  return (
    <div>
      <h1>Welcome to your Dashboard, {user.email}!</h1>
      {/* Display user-specific content */}
    </div>
  )
}


## IV. Stripe Integration for Subscriptions

### 1. Install Stripe SDK

bash
npm install stripe
# or
yarn add stripe
# or
pnpm add stripe


### 2. Configure Stripe Environment Variables

Add your Stripe keys to .env.local:
env
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=YOUR_STRIPE_PUBLISHABLE_KEY
STRIPE_SECRET_KEY=YOUR_STRIPE_SECRET_KEY
STRIPE_WEBHOOK_SECRET=YOUR_STRIPE_WEBHOOK_SECRET # For verifying webhook events

*Security Note:* STRIPE_SECRET_KEY and STRIPE_WEBHOOK_SECRET MUST NOT be prefixed with NEXT_PUBLIC_.

### 3. Create Stripe Products and Prices

In your Stripe Dashboard:
1.  Go to "Products".
2.  Click "+ Add product". Define your SaaS plans (e.g., Basic, Pro, Enterprise).
3.  For each product, add pricing (recurring subscriptions). Note the Price ID (e.g., price_xxxxxxxxxxxxxx).

### 4. Database Schema for Subscriptions (Supabase)

It's essential to store subscription status in your Supabase database, synced with Stripe.
Create a table, e.g., user_subscriptions:

| Column Name             | Data Type     | Constraints                               | Description                                     |
| :---------------------- | :------------ | :---------------------------------------- | :---------------------------------------------- |
| id                    | uuid        | Primary Key, Default: uuid_generate_v4()| Unique ID for the subscription record           |
| user_id               | uuid        | Foreign Key to auth.users(id), Unique   | Links to the Supabase user                      |
| stripe_customer_id    | text        | Unique                                    | Stripe Customer ID                              |
| stripe_subscription_id| text        | Unique                                    | Stripe Subscription ID                          |
| status                | text        |                                           | e.g., active, canceled, past_due, trialing|
| current_period_ends_at| timestamptz |                                           | When the current billing period ends            |
| price_id              | text        |                                           | Stripe Price ID of the subscribed plan          |
| created_at            | timestamptz | Default: now()                          | Timestamp of creation                           |
| updated_at            | timestamptz | Default: now()                          | Timestamp of last update                        |

*SQL for creating the table (run in Supabase SQL Editor):*
sql
CREATE TABLE public.user_subscriptions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID UNIQUE NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  stripe_customer_id TEXT UNIQUE,
  stripe_subscription_id TEXT UNIQUE,
  status TEXT,
  current_period_ends_at TIMESTAMPTZ,
  price_id TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Optional: Create a function to update updated_at timestamp automatically
CREATE OR REPLACE FUNCTION public.update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_user_subscriptions_updated_at
BEFORE UPDATE ON public.user_subscriptions
FOR EACH ROW
EXECUTE FUNCTION public.update_updated_at_column();


### 5. API Endpoint: Create Checkout Session

src/app/api/stripe/create-checkout-session/route.ts
typescript
import { NextResponse, NextRequest } from 'next/server'
import { stripe } from '@/utils/stripe/config' // We'll create this config file next
import { createServerSupabaseClient } from '@/utils/supabase/server'

export async function POST(req: NextRequest) {
  const supabase = createServerSupabaseClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }

  const { priceId, quantity = 1, metadata = {} } = await req.json()

  try {
    // Check if user already has a Stripe customer ID in your DB
    // If not, create one. This logic might be in a shared utility.
    let { data: profile } = await supabase
      .from('user_subscriptions') // Or your profiles table
      .select('stripe_customer_id')
      .eq('user_id', user.id)
      .single()

    let customerId = profile?.stripe_customer_id

    if (!customerId) {
      const customer = await stripe.customers.create({
        email: user.email,
        metadata: { userId: user.id }, // Link Stripe customer to Supabase user
      })
      customerId = customer.id
      // Save customerId to your database
      await supabase
        .from('user_subscriptions') // Or profiles table
        .upsert({ user_id: user.id, stripe_customer_id: customerId }, { onConflict: 'user_id' })
    }
    
    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      billing_address_collection: 'required',
      customer: customerId,
      line_items: [
        {
          price: priceId,
          quantity: quantity,
        },
      ],
      mode: 'subscription',
      allow_promotion_codes: true,
      subscription_data: {
        metadata: { userId: user.id } // Link subscription to Supabase user
      },
      success_url: `${req.headers.get('origin')}/payment/success?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${req.headers.get('origin')}/subscribe`, // Or your pricing page
    })

    return NextResponse.json({ sessionId: session.id })
  } catch (error: any) {
    console.error('Error creating checkout session:', error)
    return NextResponse.json({ error: error.message }, { status: 500 })
  }
}


*Stripe Config Utility:*
src/utils/stripe/config.ts
typescript
import Stripe from 'stripe'

export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2024-04-10', // Use the latest API version
  typescript: true,
})


### 6. API Endpoint: Create Customer Portal Session

src/app/api/stripe/create-portal-session/route.ts
typescript
import { NextResponse, NextRequest } from 'next/server'
import { stripe } from '@/utils/stripe/config'
import { createServerSupabaseClient } from '@/utils/supabase/server'

export async function POST(req: NextRequest) {
  const supabase = createServerSupabaseClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }

  try {
    const { data: profile } = await supabase
      .from('user_subscriptions') // Or your profiles table
      .select('stripe_customer_id')
      .eq('user_id', user.id)
      .single()

    if (!profile?.stripe_customer_id) {
      return NextResponse.json({ error: 'Stripe customer not found for this user.' }, { status: 404 })
    }

    const portalSession = await stripe.billingPortal.sessions.create({
      customer: profile.stripe_customer_id,
      return_url: `${req.headers.get('origin')}/account`, // Your account page
    })

    return NextResponse.json({ url: portalSession.url })
  } catch (error: any) {
    console.error('Error creating portal session:', error)
    return NextResponse.json({ error: error.message }, { status: 500 })
  }
}


### 7. API Endpoint: Stripe Webhooks

This is critical for keeping your database in sync with Stripe.
src/app/api/stripe/webhooks/route.ts
typescript
import { NextResponse, NextRequest } from 'next/server'
import { stripe } from '@/utils/stripe/config'
import Stripe from 'stripe'
import { createClient } from '@supabase/supabase-js' // Use standard client for webhooks

// Initialize Supabase client for webhook handler (cannot use SSR client here)
// Ensure service_role key is used for admin-level access if needed for DB updates
const supabaseAdmin = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY! // IMPORTANT: Use service role key for backend operations
);


async function relevantEventsHandler(event: Stripe.Event) {
  const { type, data } = event;
  const object = data.object as any; // Cast to any to access properties dynamically

  switch (type) {
    case 'customer.subscription.created':
    case 'customer.subscription.updated':
    case 'customer.subscription.deleted': // Handles cancellations
      const subscription = object as Stripe.Subscription;
      await supabaseAdmin
        .from('user_subscriptions')
        .upsert({
          user_id: subscription.metadata?.userId || object.customer.metadata?.userId, // Ensure userId is in metadata
          stripe_subscription_id: subscription.id,
          stripe_customer_id: subscription.customer as string,
          status: subscription.status,
          price_id: subscription.items.data[0].price.id,
          current_period_ends_at: new Date(subscription.current_period_end * 1000).toISOString(),
        }, { onConflict: 'stripe_subscription_id' }); // Use stripe_subscription_id for upsert conflict
      console.log(`Subscription ${type}: ${subscription.id}, Status: ${subscription.status}`);
      break;

    case 'checkout.session.completed':
      const checkoutSession = object as Stripe.Checkout.Session;
      if (checkoutSession.mode === 'subscription' && checkoutSession.subscription) {
        // If it's a new subscription, the customer.subscription.created event will handle DB update.
        // But you might want to log or perform other actions here.
        // Ensure metadata.userId is set on the session or subscription.
        const subscriptionId = checkoutSession.subscription as string;
        const subscription = await stripe.subscriptions.retrieve(subscriptionId);

        await supabaseAdmin
          .from('user_subscriptions')
          .upsert({
            user_id: checkoutSession.metadata?.userId || subscription.metadata?.userId,
            stripe_subscription_id: subscription.id,
            stripe_customer_id: subscription.customer as string,
            status: subscription.status,
            price_id: subscription.items.data[0].price.id,
            current_period_ends_at: new Date(subscription.current_period_end * 1000).toISOString(),
          }, { onConflict: 'stripe_subscription_id' });
        console.log(`Checkout session completed for subscription: ${subscription.id}`);
      }
      break;
    
    case 'invoice.payment_succeeded':
      // If a subscription payment succeeds, update current_period_end
      const invoice = object as Stripe.Invoice;
      if (invoice.subscription) {
        const subscriptionId = invoice.subscription as string;
        const subscriptionDetails = await stripe.subscriptions.retrieve(subscriptionId);
        await supabaseAdmin
          .from('user_subscriptions')
          .update({
            status: subscriptionDetails.status, // Should be 'active'
            current_period_ends_at: new Date(subscriptionDetails.current_period_end * 1000).toISOString(),
          })
          .eq('stripe_subscription_id', subscriptionId);
        console.log(`Invoice payment succeeded for subscription: ${subscriptionId}`);
      }
      break;

    case 'invoice.payment_failed':
      // Handle failed payments, potentially update status to 'past_due' or 'unpaid'
      const failedInvoice = object as Stripe.Invoice;
      if (failedInvoice.subscription) {
         const subscriptionId = failedInvoice.subscription as string;
         await supabaseAdmin
          .from('user_subscriptions')
          .update({ status: 'past_due' }) // Or as per your logic
          .eq('stripe_subscription_id', subscriptionId);
        console.log(`Invoice payment failed for subscription: ${subscriptionId}`);
      }
      break;

    default:
      console.log(`Unhandled Stripe event type: ${type}`);
  }
}


export async function POST(req: NextRequest) {
  const body = await req.text()
  const sig = req.headers.get('stripe-signature') as string
  const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET!
  let event: Stripe.Event

  try {
    if (!sig || !webhookSecret) {
      console.error('Stripe webhook secret or signature not found.')
      return NextResponse.json({ error: 'Webhook secret not configured.' }, { status: 400 })
    }
    event = stripe.webhooks.constructEvent(body, sig, webhookSecret)
  } catch (err: any) {
    console.error(`❌ Error message: ${err.message}`)
    return NextResponse.json({ error: `Webhook Error: ${err.message}` }, { status: 400 })
  }

  console.log('✅ Stripe event received:', event.type, event.id)
  
  try {
    await relevantEventsHandler(event);
  } catch (error: any) {
    console.error('Error handling webhook event:', error.message);
    return NextResponse.json({ error: 'Webhook handler failed.' }, { status: 500 });
  }

  return NextResponse.json({ received: true })
}

// Disable body parsing for this route, as Stripe sends raw body
export const config = {
  api: {
    bodyParser: false,
  },
}

*CRITICAL:*
*   Ensure userId is passed in metadata when creating Stripe Checkout Sessions and Subscriptions to link them back to your Supabase user.
*   Test webhooks thoroughly using the Stripe CLI: stripe listen --forward-to localhost:3000/api/stripe/webhooks.
*   The webhook handler MUST use SUPABASE_SERVICE_ROLE_KEY for database operations as it's a backend process.

## V. Frontend Implementation Snippets

Provide UI elements for users to manage subscriptions.

Example: src/components/SubscriptionManager.tsx
tsx
'use client'

import { useState, useEffect } from 'react'
import { createClient } from '@/utils/supabase/client'
import { User } from '@supabase/supabase-js'

// Assume you have a Price ID for your main subscription plan
const SUBSCRIPTION_PRICE_ID = 'price_YOUR_STRIPE_PRICE_ID' 

export default function SubscriptionManager() {
  const supabase = createClient()
  const [user, setUser] = useState<User | null>(null)
  const [subscription, setSubscription] = useState<any | null>(null) // Define a type for subscription
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    const getUserAndSubscription = async () => {
      const { data: { user: currentUser } } = await supabase.auth.getUser()
      setUser(currentUser)

      if (currentUser) {
        // Fetch subscription status from your database
        const { data: subData, error } = await supabase
          .from('user_subscriptions')
          .select('*')
          .eq('user_id', currentUser.id)
          .single()
        
        if (subData) setSubscription(subData)
        if (error && error.code !== 'PGRST116') { // PGRST116: no rows found
            console.error('Error fetching subscription:', error)
        }
      }
    }
    getUserAndSubscription()
  }, [])

  const handleSubscribe = async () => {
    if (!user) return alert('Please log in to subscribe.')
    setIsLoading(true)
    try {
      const response = await fetch('/api/stripe/create-checkout-session', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ priceId: SUBSCRIPTION_PRICE_ID }),
      })
      const { sessionId, error } = await response.json()
      if (error) throw new Error(error)

      const stripe = (await import('@stripe/stripe-js')).loadStripe(
        process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!
      )
      if (!stripe) throw new Error('Stripe.js not loaded')
      
      await stripe.redirectToCheckout({ sessionId })
    } catch (error: any) {
      alert(`Error: ${error.message}`)
    } finally {
      setIsLoading(false)
    }
  }

  const handleManageSubscription = async () => {
    if (!user || !subscription) return alert('No active subscription found.')
    setIsLoading(true)
    try {
      const response = await fetch('/api/stripe/create-portal-session', {
        method: 'POST',
      })
      const { url, error } = await response.json()
      if (error) throw new Error(error)
      window.location.href = url
    } catch (error: any) {
      alert(`Error: ${error.message}`)
    } finally {
      setIsLoading(false)
    }
  }

  if (!user) return <p>Please log in.</p>

  return (
    <div>
      <h2>Subscription Status</h2>
      {subscription && subscription.status === 'active' ? (
        <div>
          <p>Plan: Active ({subscription.price_id})</p>
          <p>Renews on: {new Date(subscription.current_period_ends_at).toLocaleDateString()}</p>
          <button onClick={handleManageSubscription} disabled={isLoading}>
            {isLoading ? 'Loading...' : 'Manage Subscription'}
          </button>
        </div>
      ) : (
        <div>
          <p>No active subscription.</p>
          <button onClick={handleSubscribe} disabled={isLoading}>
            {isLoading ? 'Loading...' : 'Subscribe Now'}
          </button>
        </div>
      )}
    </div>
  )
}


## VI. Deployment Considerations

*   *Environment Variables:* Securely set all NEXT_PUBLIC_SUPABASE_URL, NEXT_PUBLIC_SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY, NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY, STRIPE_SECRET_KEY, and STRIPE_WEBHOOK_SECRET on your hosting platform (e.g., Vercel, Netlify).
*   *Stripe Webhook Endpoint:* In your Stripe Dashboard (Developers -> Webhooks), add an endpoint for your deployed application: https://yourdomain.com/api/stripe/webhooks. Select the events you want to listen to (e.g., customer.subscription.*, checkout.session.completed, invoice.payment_succeeded, invoice.payment_failed).
*   *Supabase URLs:* Update "Site URL" and "Additional Redirect URLs" in Supabase Auth settings to your production domain.

## VII. Best Practices and .clinerule Usage

*   *Security:*
    *   NEVER expose secret keys on the client-side.
    *   Always validate user authentication and authorization for sensitive operations.
    *   Verify Stripe webhook signatures.
*   *Error Handling:* Implement robust error handling and logging for API routes and client-side operations.
*   *Modularity:* Keep functions and components small and focused.
*   *Testing:* Test the entire flow: OAuth signup -> subscription -> webhook updates -> customer portal.
*   *Cline Guidance:*
    *   Cline SHOULD refer to specific sections of this rule when asked about parts of the integration.
    *   Cline MUST emphasize secure handling of API keys and webhook secrets.
    *   Cline SHOULD provide code snippets from this rule and explain their purpose.
    *   Cline MAY suggest alternative approaches if appropriate but SHOULD highlight this rule as a standard path.
*   *Official Documentation:* Always refer to the latest official documentation for Next.js, Supabase, and Stripe as APIs and best practices evolve.
    *   [Next.js Docs](https://nextjs.org/docs)
    *   [Supabase Docs](https://supabase.com/docs)
    *   [Stripe Docs](https://stripe.com/docs)

## VIII. (Optional) Mermaid Diagram - Simplified Flow

mermaid
sequenceDiagram
    participant User
    participant NextApp as Next.js App (Client)
    participant NextAPI as Next.js API Routes
    participant SupabaseAuth as Supabase Auth
    participant StripeAPI as Stripe API
    participant SupabaseDB as Supabase DB

    User->>NextApp: Clicks Login with Google
    NextApp->>SupabaseAuth: Initiates OAuth (signInWithOAuth)
    SupabaseAuth-->>User: Redirects to Google
    User->>Google: Authenticates
    Google-->>SupabaseAuth: Redirects with auth code (via Supabase callback)
    SupabaseAuth-->>NextApp: Redirects to /auth/callback (App's callback)
    NextApp->>NextAPI: GET /auth/callback (code)
    NextAPI->>SupabaseAuth: exchangeCodeForSession(code)
    SupabaseAuth-->>NextAPI: Session created
    NextAPI-->>NextApp: Redirect to dashboard (user logged in)

    User->>NextApp: Clicks Subscribe
    NextApp->>NextAPI: POST /api/stripe/create-checkout-session (priceId)
    NextAPI->>SupabaseDB: Get/Create Stripe Customer ID for user
    NextAPI->>StripeAPI: Create Checkout Session
    StripeAPI-->>NextAPI: Returns sessionId
    NextAPI-->>NextApp: Returns sessionId
    NextApp->>StripeAPI: redirectToCheckout(sessionId)
    User->>StripeAPI: Completes Payment on Stripe Page
    StripeAPI-->>User: Redirects to success_url

    StripeAPI->>NextAPI: POST /api/stripe/webhooks (e.g., checkout.session.completed)
    NextAPI->>StripeAPI: Verifies webhook signature
    NextAPI->>SupabaseDB: Upserts subscription details (status, dates, etc.)
    SupabaseDB-->>NextAPI: DB updated
    NextAPI-->>StripeAPI: Returns 200 OK

    User->>NextApp: Clicks Manage Subscription
    NextApp->>NextAPI: POST /api/stripe/create-portal-session
    NextAPI->>SupabaseDB: Get Stripe Customer ID
    NextAPI->>StripeAPI: Create Billing Portal Session
    StripeAPI-->>NextAPI: Returns portal URL
    NextAPI-->>NextApp: Returns portal URL
    NextApp-->>User: Redirects to Stripe Billing Portal


This rule provides a solid foundation. Cline should adapt and elaborate on these steps based on specific user queries and project contexts.