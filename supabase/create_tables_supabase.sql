-- ==============================================================================
-- CV26 E-COMMERCE SHOP & DSS EXPERTISE - SUPABASE DATABASE SCHEMA
-- RUN5 Specification
-- ==============================================================================

-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ------------------------------------------------------------------------------
-- 1. cv26ShopUserSessionTable
-- Tracks user session lifecycle, execution timings, and metadata
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public."cv26ShopUserSessionTable" (
    "userSessionGUID" TEXT PRIMARY KEY,
    "userSessionJSON" JSONB NOT NULL DEFAULT '{}'::jsonb,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE public."cv26ShopUserSessionTable" ENABLE ROW LEVEL SECURITY;

-- Drop existing policies if re-running
DROP POLICY IF EXISTS "Allow public CRUD on cv26ShopUserSessionTable" ON public."cv26ShopUserSessionTable";

-- Create full CRUD policy for anon key
CREATE POLICY "Allow public CRUD on cv26ShopUserSessionTable" 
ON public."cv26ShopUserSessionTable"
FOR ALL 
TO anon, authenticated 
USING (true) 
WITH CHECK (true);

-- ------------------------------------------------------------------------------
-- 2. cv26ShopProgressTable
-- Tracks real-time ML execution step, percentage, and status
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public."cv26ShopProgressTable" (
    "userSessionGUID" TEXT PRIMARY KEY,
    "progressDataJSON" JSONB NOT NULL DEFAULT '{"percent": 0, "stepId": 0, "stepName": "Idle", "details": ""}'::jsonb,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE public."cv26ShopProgressTable" ENABLE ROW LEVEL SECURITY;

-- Drop existing policies if re-running
DROP POLICY IF EXISTS "Allow public CRUD on cv26ShopProgressTable" ON public."cv26ShopProgressTable";

-- Create full CRUD policy for anon key
CREATE POLICY "Allow public CRUD on cv26ShopProgressTable" 
ON public."cv26ShopProgressTable"
FOR ALL 
TO anon, authenticated 
USING (true) 
WITH CHECK (true);

-- ------------------------------------------------------------------------------
-- 3. cv26ShopResultsTable
-- Stores full DSS results and Capstone Report dataset
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public."cv26ShopResultsTable" (
    "userSessionGUID" TEXT PRIMARY KEY,
    "resultDataJSON" JSONB NOT NULL DEFAULT '{}'::jsonb,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE public."cv26ShopResultsTable" ENABLE ROW LEVEL SECURITY;

-- Drop existing policies if re-running
DROP POLICY IF EXISTS "Allow public CRUD on cv26ShopResultsTable" ON public."cv26ShopResultsTable";

-- Create full CRUD policy for anon key
CREATE POLICY "Allow public CRUD on cv26ShopResultsTable" 
ON public."cv26ShopResultsTable"
FOR ALL 
TO anon, authenticated 
USING (true) 
WITH CHECK (true);

-- ------------------------------------------------------------------------------
-- 4. cv26ShopErrorsTable
-- Logs errors encountered during preprocessing or ML execution
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public."cv26ShopErrorsTable" (
    "id" UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    "userSessionGUID" TEXT NOT NULL,
    "errorJSON" JSONB NOT NULL DEFAULT '{}'::jsonb,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE public."cv26ShopErrorsTable" ENABLE ROW LEVEL SECURITY;

-- Drop existing policies if re-running
DROP POLICY IF EXISTS "Allow public CRUD on cv26ShopErrorsTable" ON public."cv26ShopErrorsTable";

-- Create full CRUD policy for anon key
CREATE POLICY "Allow public CRUD on cv26ShopErrorsTable" 
ON public."cv26ShopErrorsTable"
FOR ALL 
TO anon, authenticated 
USING (true) 
WITH CHECK (true);

-- ------------------------------------------------------------------------------
-- Grant table permissions to public roles (anon and authenticated)
-- ------------------------------------------------------------------------------
GRANT ALL ON TABLE public."cv26ShopUserSessionTable" TO anon, authenticated, service_role;
GRANT ALL ON TABLE public."cv26ShopProgressTable" TO anon, authenticated, service_role;
GRANT ALL ON TABLE public."cv26ShopResultsTable" TO anon, authenticated, service_role;
GRANT ALL ON TABLE public."cv26ShopErrorsTable" TO anon, authenticated, service_role;

-- Enable Realtime for all tables in publication
ALTER PUBLICATION supabase_realtime ADD TABLE public."cv26ShopUserSessionTable";
ALTER PUBLICATION supabase_realtime ADD TABLE public."cv26ShopProgressTable";
ALTER PUBLICATION supabase_realtime ADD TABLE public."cv26ShopResultsTable";
ALTER PUBLICATION supabase_realtime ADD TABLE public."cv26ShopErrorsTable";
