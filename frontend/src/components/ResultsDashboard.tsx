'use client';

import React, { useState } from 'react';
import { useValidationStore } from '@/store/useValidationStore';
import ExportPanel from './ExportPanel';

export default function ResultsDashboard() {
    const { results, reset } = useValidationStore();
    const [activeTab, setActiveTab] = useState<'summary' | 'details' | 'stats'>('summary');

    if (!results) return null;

    const { summary, sample_errors } = results;

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-2xl font-bold text-gray-800">Validation Results</h2>
                <button onClick={reset} className="text-sm text-gray-500 hover:text-gray-700 underline">Start Over</button>
            </div>

            {/* Summary Cards */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className={`p-4 rounded-lg shadow-sm border-l-4 ${summary.overall_status === 'pass' ? 'bg-green-50 border-green-500' : 'bg-red-50 border-red-500'}`}>
                    <div className="text-sm text-gray-500">Status</div>
                    <div className="text-2xl font-bold capitalize">{summary.overall_status}</div>
                </div>
                <div className="p-4 bg-white rounded-lg shadow-sm border border-gray-200">
                    <div className="text-sm text-gray-500">Total Rows</div>
                    <div className="text-2xl font-bold">{summary.total_rows}</div>
                </div>
                <div className="p-4 bg-white rounded-lg shadow-sm border border-gray-200">
                    <div className="text-sm text-gray-500">Passed</div>
                    <div className="text-2xl font-bold text-green-600">{summary.passed_rows}</div>
                </div>
                <div className="p-4 bg-white rounded-lg shadow-sm border border-gray-200">
                    <div className="text-sm text-gray-500">Failed</div>
                    <div className="text-2xl font-bold text-red-600">{summary.failed_rows}</div>
                </div>
            </div>

            {/* Tabs */}
            <div className="border-b border-gray-200">
                <nav className="-mb-px flex space-x-8">
                    {['summary', 'details', 'stats'].map((tab) => (
                        <button
                            key={tab}
                            onClick={() => setActiveTab(tab as any)}
                            className={`whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm ${activeTab === tab
                                    ? 'border-blue-500 text-blue-600'
                                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                                }`}
                        >
                            {tab.charAt(0).toUpperCase() + tab.slice(1)}
                        </button>
                    ))}
                </nav>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 min-h-[300px]">
                {activeTab === 'summary' && (
                    <div>
                        <h3 className="text-lg font-medium mb-4">Errors by Rule</h3>
                        {Object.keys(summary.error_counts_by_rule).length === 0 ? (
                            <p className="text-gray-500">No errors found.</p>
                        ) : (
                            <ul className="space-y-2">
                                {Object.entries(summary.error_counts_by_rule).map(([rule, count]) => (
                                    <li key={rule} className="flex justify-between items-center border-b pb-2">
                                        <span className="capitalize">{rule.replace('_', ' ')}</span>
                                        <span className="font-mono bg-gray-100 px-2 py-1 rounded">{count} rows failed</span>
                                    </li>
                                ))}
                            </ul>
                        )}
                    </div>
                )}

                {activeTab === 'details' && (
                    <div>
                        <h3 className="text-lg font-medium mb-4">Sample Failed Rows (First 10)</h3>
                        {sample_errors && sample_errors.length > 0 ? (
                            <div className="overflow-x-auto">
                                <table className="min-w-full divide-y divide-gray-200 text-sm">
                                    <thead className="bg-gray-50">
                                        <tr>
                                            {Object.keys(sample_errors[0]).map((key) => (
                                                <th key={key} className="px-3 py-2 text-left font-medium text-gray-500 uppercase tracking-wider">{key}</th>
                                            ))}
                                        </tr>
                                    </thead>
                                    <tbody className="bg-white divide-y divide-gray-200">
                                        {sample_errors.map((row: any, idx: number) => (
                                            <tr key={idx} className="hover:bg-gray-50">
                                                {Object.values(row).map((val: any, i) => (
                                                    <td key={i} className="px-3 py-2 whitespace-nowrap text-gray-700">{val?.toString() ?? 'NULL'}</td>
                                                ))}
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        ) : (
                            <p className="text-gray-500">No failures to display.</p>
                        )}
                    </div>
                )}

                {activeTab === 'stats' && (
                    <div>
                        <h3 className="text-lg font-medium mb-4">Column Statistics</h3>
                        <div className="grid grid-cols-1 gap-4">
                            {summary.column_stats.map((stat: any) => (
                                <div key={stat.column} className="border p-4 rounded bg-gray-50">
                                    <div className="font-bold text-gray-800">{stat.column}</div>
                                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 mt-2 text-xs text-gray-600">
                                        <div>Nulls: {stat.null_count} ({stat.null_percentage.toFixed(1)}%)</div>
                                        <div>Unique: {stat.unique_count}</div>
                                        {stat.mean !== 0 && <div>Mean: {stat.mean?.toFixed(2)}</div>}
                                        {stat.min !== 0 && <div>Min: {stat.min}</div>}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </div>

            <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
                <h3 className="text-lg font-medium mb-4">Export Report</h3>
                <ExportPanel />
            </div>
        </div>
    );
}
