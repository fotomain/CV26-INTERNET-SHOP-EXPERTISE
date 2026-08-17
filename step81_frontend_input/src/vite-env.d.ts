/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_BACKEND_URL: string;
  readonly VITE_SUPABASE_URL: string;
  readonly VITE_SUPABASE_ANON_KEY: string;
  readonly VITE_DEFAULT_FILE_SIZE_LIMIT_MB: string;
  readonly VITE_DEFAULT_NUMBER_OF_FILES: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
