import { createClient } from '@supabase/supabase-js';
import { SUPABASE_URL, SUPABASE_ANON_KEY } from '../constants/config';

export const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY, {
  realtime: {
    params: {
      eventsPerSecond: 10,
    },
  },
});

export interface SupabaseProgressPayload {
  percent: number;
  stepId: number;
  stepName: string;
  details: string;
  timestamp?: string;
}

export interface SupabaseResultPayload {
  metadata: any;
  targetCountry: any;
  kpis: any;
  categoryBreakdown: any[];
  tierDistribution: Record<string, number>;
  paletteAffinityDistribution: Record<string, number>;
  products: any[];
  stepTimings: Record<string, number>;
  mlModelStats: any;
}

/**
 * Subscribes to real-time progress updates on cv26ShopProgressTable for a specific userSessionGUID.
 */
export function subscribeToProgress(
  userSessionGUID: string,
  onProgress: (progress: SupabaseProgressPayload) => void
) {
  const channel = supabase
    .channel(`progress-${userSessionGUID}`)
    .on(
      'postgres_changes',
      {
        event: '*',
        schema: 'public',
        table: 'cv26ShopProgressTable',
        filter: `userSessionGUID=eq.${userSessionGUID}`,
      },
      (payload) => {
        if (payload.new && (payload.new as any).progressDataJSON) {
          onProgress((payload.new as any).progressDataJSON);
        }
      }
    )
    .subscribe();

  return () => {
    supabase.removeChannel(channel);
  };
}

/**
 * Subscribes to real-time result completion on cv26ShopResultsTable for a specific userSessionGUID.
 */
export function subscribeToResults(
  userSessionGUID: string,
  onResult: (results: SupabaseResultPayload) => void
) {
  const channel = supabase
    .channel(`results-${userSessionGUID}`)
    .on(
      'postgres_changes',
      {
        event: '*',
        schema: 'public',
        table: 'cv26ShopResultsTable',
        filter: `userSessionGUID=eq.${userSessionGUID}`,
      },
      (payload) => {
        if (payload.new && (payload.new as any).resultDataJSON) {
          onResult((payload.new as any).resultDataJSON);
        }
      }
    )
    .subscribe();

  return () => {
    supabase.removeChannel(channel);
  };
}
