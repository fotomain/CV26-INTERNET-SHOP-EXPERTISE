/**
 * Application Constants (RUN5 Specification)
 */

export const DEFAULT_FILE_SIZE_LIMIT_MB = 1;
export const DEFAULT_FILE_SIZE_LIMIT_BYTES = DEFAULT_FILE_SIZE_LIMIT_MB * 1024 * 1024; // 1MB
export const DEFAULT_NUMBER_OF_FILES = 200;

export const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';
export const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL || 'https://czgrxgzdmodkkmbmraub.supabase.co';
export const SUPABASE_ANON_KEY = import.meta.env.VITE_SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN6Z3J4Z3pkbW9ka2ttYm1yYXViIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE1OTU3MzYsImV4cCI6MjA3NzE3MTczNn0.4aul_NOjMO_VEKOgxFE3-Z5plqH1g8aSN8xJEgHPYR8';

export const SUPPORTED_COUNTRIES = [
  { name: 'United States', code: 'USA', flag: '🇺🇸', defaultDir: 'step5_new_country' },
  { name: 'Germany', code: 'DEU', flag: '🇩🇪', defaultDir: 'step5_new_country' },
  { name: 'France', code: 'FRA', flag: '🇫🇷', defaultDir: 'step5_new_country' },
  { name: 'Italy', code: 'ITA', flag: '🇮🇹', defaultDir: 'step5_new_country' },
  { name: 'United Kingdom', code: 'GBR', flag: '🇬🇧', defaultDir: 'step5_new_country' },
  { name: 'Japan', code: 'JPN', flag: '🇯🇵', defaultDir: 'step5_new_country' },
  { name: 'Spain', code: 'ESP', flag: '🇪🇸', defaultDir: 'step5_new_country' },
  { name: 'Canada', code: 'CAN', flag: '🇨🇦', defaultDir: 'step5_new_country' },
  { name: 'Australia', code: 'AUS', flag: '🇦🇺', defaultDir: 'step5_new_country' },
];
