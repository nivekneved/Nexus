# SiteSpeak - Nexus Turnkey Software
**Pitch:** Voice-first daily reporting for construction
**Architecture:** React Native (Expo) + Supabase (PostgreSQL)

## Intellectual Property Transfer Complete
Congratulations on securing the IP for SiteSpeak. You now own 100% of this source code and are free to white-label, re-sell, or deploy it for your clients.

## Backend Deployment Instructions (5 Minutes)
We have completely decoupled the backend so you can host it securely on your own infrastructure.

1. Create a free account at [Supabase](https://supabase.com/).
2. Create a new Project.
3. Navigate to the **SQL Editor** in your Supabase dashboard.
4. Copy the entire contents of `supabase/schema.sql` and run it. This will automatically build your customized relational database tables.
5. Get your API Keys (Project URL and anon public key) from Settings -> API.
6. Open `src/lib/supabase.ts` and paste your keys into the configuration variables.

## Compiling the App
Run the following commands to test the app locally:
```bash
npm install
npx expo start
```
