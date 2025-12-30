from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any, Union

class RuleConfig(BaseModel):
    check_null: bool = True
    null_threshold: float = 0.0  # 0 to 1
    
    check_schema: bool = False
    expected_schema: Dict[str, str] = {} # {"col_name": "dtype"}
    
    check_outliers: bool = False
    outlier_method: str = "zscore" # "zscore" or "iqr"
    sensitivity: float = 3.0 # Standard deviations for Z-score

class ValidationRequest(BaseModel):
    # For now, we might receive config via JSON in a separate field if using FormData for file upload
    rules: RuleConfig

class ColumnStats(BaseModel):
    column: str
    null_count: int
    null_percentage: float
    min: Optional[float] = None
    max: Optional[float] = None
    mean: Optional[float] = None
    unique_count: int

class ValidationResultSummary(BaseModel):
    total_rows: int
    failed_rows: int
    passed_rows: int
    overall_status: str # "pass", "fail", "warning"
    error_counts_by_rule: Dict[str, int]
    column_stats: List[ColumnStats]

class ValidationResult(BaseModel):
    run_id: str
    summary: ValidationResultSummary
    # Detailed results might be stored/returned differently to avoid huge payloads
    # This could be a preview of errors
    sample_errors: List[Dict[str, Any]] = []
