import pandas as pd
import numpy as np
import io
from typing import Dict, List, Any, Tuple
from app.schemas.validation import RuleConfig, ValidationResultSummary, ColumnStats

def process_file(file_content: bytes, filename: str) -> pd.DataFrame:
    if filename.endswith('.csv'):
        try:
            df = pd.read_csv(io.BytesIO(file_content))
            return df
        except Exception as e:
            raise ValueError(f"Error reading CSV: {e}")
    elif filename.endswith('.json'):
        try:
            df = pd.read_json(io.BytesIO(file_content))
            return df
        except Exception as e:
            raise ValueError(f"Error reading JSON: {e}")
    else:
        raise ValueError("Unsupported file format")

def validate_dataframe(df: pd.DataFrame, config: RuleConfig) -> Tuple[ValidationResultSummary, List[Dict]]:
    total_rows = len(df)
    failed_indices = set()
    errors_by_rule = {"null_check": 0, "schema_check": 0, "outlier_check": 0}
    
    # 1. Null Checks
    if config.check_null:
        # Check row-level null threshold or col-level? Req says "Null threshold (%)"
        # Usually implies: if col has > X% nulls, flag it? OR if row has nulls?
        # User req: "Null threshold (%)". Let's assume per-column check for now to flag columns,
        # OR per-row check (if row has nulls > X% ?? usually row has ANY null).
        # Let's interpret: If a row has nulls in critical columns?
        # Let's keep it simple: Flag rows that contain Nulls if strict.
        # But threshold usually applies to acceptable noise.
        # Implementation: Flag ROWS that have nulls.
        is_null = df.isnull()
        rows_with_nulls = is_null.any(axis=1)
        # If we need to fail based on threshold:
        # We'll just count them as "failed rows" for this rule
        failed_indices.update(df[rows_with_nulls].index)
        errors_by_rule["null_check"] += rows_with_nulls.sum()

    # 2. Schema Check
    # This is tricky without explicit schema mapping from user for every column early on.
    # We will skip complex schema validation implementation for MVP unless provided.
    
    # 3. Outlier Detection
    if config.check_outliers:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if config.outlier_method == "zscore":
            z_scores = np.abs((df[numeric_cols] - df[numeric_cols].mean()) / df[numeric_cols].std())
            outliers = (z_scores > config.sensitivity).any(axis=1)
            failed_indices.update(df[outliers].index)
            errors_by_rule["outlier_check"] += outliers.sum()
        elif config.outlier_method == "iqr":
            Q1 = df[numeric_cols].quantile(0.25)
            Q3 = df[numeric_cols].quantile(0.75)
            IQR = Q3 - Q1
            outliers = ((df[numeric_cols] < (Q1 - 1.5 * IQR)) | (df[numeric_cols] > (Q3 + 1.5 * IQR))).any(axis=1)
            failed_indices.update(df[outliers].index)
            errors_by_rule["outlier_check"] += outliers.sum()

    failed_rows_count = len(failed_indices)
    passed_rows_count = total_rows - failed_rows_count
    
    # Calculate Stats
    col_stats = []
    for col in df.columns:
        null_count = int(df[col].isnull().sum())
        stats = ColumnStats(
            column=col,
            null_count=null_count,
            null_percentage=(null_count / total_rows * 100) if total_rows > 0 else 0,
            unique_count=int(df[col].nunique())
        )
        if pd.api.types.is_numeric_dtype(df[col]):
            stats.min = float(df[col].min()) if not df[col].empty else 0
            stats.max = float(df[col].max()) if not df[col].empty else 0
            stats.mean = float(df[col].mean()) if not df[col].empty else 0
        
        col_stats.append(stats)

    summary = ValidationResultSummary(
        total_rows=total_rows,
        failed_rows=failed_rows_count,
        passed_rows=passed_rows_count,
        overall_status="fail" if failed_rows_count > 0 else "pass", # Simplistic
        error_counts_by_rule=errors_by_rule,
        column_stats=col_stats
    )
    
    # Sample errors (rows)
    sample_errors = df.iloc[list(failed_indices)[:10]].to_dict(orient='records') if failed_indices else []
    
    return summary, sample_errors
