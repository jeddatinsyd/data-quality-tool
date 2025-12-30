import { create } from 'zustand';

export interface RuleConfig {
  check_null: boolean;
  null_threshold: number;
  check_schema: boolean;
  expected_schema: Record<string, string>;
  check_outliers: boolean;
  outlier_method: 'zscore' | 'iqr';
  sensitivity: number;
}

export interface ValidationResult {
  run_id: string;
  summary: {
    total_rows: number;
    failed_rows: number;
    passed_rows: number;
    overall_status: string;
    error_counts_by_rule: Record<string, number>;
    column_stats: any[];
  };
  sample_errors: any[];
}

interface ValidationState {
  step: 'upload' | 'config' | 'results';
  fileId: string | null;
  filename: string | null;
  previewData: any[];
  columns: string[];
  config: RuleConfig;
  results: ValidationResult | null;
  
  setStep: (step: 'upload' | 'config' | 'results') => void;
  setFileUploaded: (id: string, name: string, preview: any[], cols: string[]) => void;
  updateConfig: (config: Partial<RuleConfig>) => void;
  setResults: (results: ValidationResult) => void;
  reset: () => void;
}

export const useValidationStore = create<ValidationState>((set) => ({
  step: 'upload',
  fileId: null,
  filename: null,
  previewData: [],
  columns: [],
  config: {
    check_null: true,
    null_threshold: 0,
    check_schema: false,
    expected_schema: {},
    check_outliers: false,
    outlier_method: 'zscore',
    sensitivity: 3.0,
  },
  results: null,

  setStep: (step) => set({ step }),
  setFileUploaded: (id, name, preview, cols) => set({ 
    fileId: id, 
    filename: name, 
    previewData: preview, 
    columns: cols,
    step: 'config'
  }),
  updateConfig: (newConfig) => set((state) => ({ 
    config: { ...state.config, ...newConfig } 
  })),
  setResults: (results) => set({ 
    results, 
    step: 'results' 
  }),
  reset: () => set({
    step: 'upload',
    fileId: null,
    filename: null,
    previewData: [],
    columns: [],
    results: null
  })
}));
