'use client';

import React, { useState } from 'react';
import { useValidationStore } from '@/store/useValidationStore';

export default function RuleConfigPanel() {
    const { config, updateConfig, fileId, setResults } = useValidationStore();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleRunValidation = async () => {
        if (!fileId) return;
        setLoading(true);
        setError(null);
        try {
            const res = await fetch(`http://localhost:8000/api/validate/${fileId}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(config),
            });

            if (!res.ok) throw new Error('Validation failed');

            const data = await res.json();
            setResults(data);
        } catch (err) {
            setError('Error running validation');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 space-y-6">
            <h2 className="text-xl font-semibold text-gray-800">Configure Validation Rules</h2>

            {/* Null Checks */}
            <div className="space-y-3">
                <label className="flex items-center space-x-3">
                    <input
                        type="checkbox"
                        checked={config.check_null}
                        onChange={(e) => updateConfig({ check_null: e.target.checked })}
                        className="h-5 w-5 text-blue-600 rounded"
                    />
                    <span className="font-medium text-gray-700">Check for Missing Values</span>
                </label>
                {config.check_null && (
                    <div className="ml-8">
                        <label className="block text-sm text-gray-600 mb-1">Row Failure Threshold (% nulls per row? No, implementation is binary row check currently)</label>
                        <p className="text-xs text-gray-500">Currently flags any row containing nulls.</p>
                    </div>
                )}
            </div>

            <hr />

            {/* Outlier Checks */}
            <div className="space-y-3">
                <label className="flex items-center space-x-3">
                    <input
                        type="checkbox"
                        checked={config.check_outliers}
                        onChange={(e) => updateConfig({ check_outliers: e.target.checked })}
                        className="h-5 w-5 text-blue-600 rounded"
                    />
                    <span className="font-medium text-gray-700">Outlier Detection (Numeric)</span>
                </label>

                {config.check_outliers && (
                    <div className="ml-8 grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label className="block text-sm text-gray-600 mb-1">Method</label>
                            <select
                                value={config.outlier_method}
                                onChange={(e) => updateConfig({ outlier_method: e.target.value as 'zscore' | 'iqr' })}
                                className="w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border"
                            >
                                <option value="zscore">Z-Score</option>
                                <option value="iqr">IQR (Interquartile Range)</option>
                            </select>
                        </div>

                        {config.outlier_method === 'zscore' && (
                            <div>
                                <label className="block text-sm text-gray-600 mb-1">Sensitivity (Std Dev)</label>
                                <input
                                    type="number"
                                    value={config.sensitivity}
                                    onChange={(e) => updateConfig({ sensitivity: parseFloat(e.target.value) })}
                                    className="w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border"
                                    min="1"
                                    step="0.5"
                                />
                            </div>
                        )}
                    </div>
                )}
            </div>

            <div className="pt-4">
                {error && <p className="text-red-500 text-sm mb-2">{error}</p>}
                <button
                    onClick={handleRunValidation}
                    disabled={loading}
                    className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline disabled:opacity-50 transition"
                >
                    {loading ? 'Running Validation...' : 'Run Validation'}
                </button>
            </div>
        </div>
    );
}
