'use client';

import React from 'react';
import { useValidationStore } from '@/store/useValidationStore';

import { apiUrl } from '@/lib/api';

export default function ExportPanel() {
    const { results } = useValidationStore();

    if (!results) return null;

    const handleExport = (format: 'csv' | 'json') => {
        const runId = results.run_id;
        window.open(apiUrl(`/api/export/${runId}?format=${format}`), '_blank');
    };

    return (
        <div className="flex space-x-4 mt-6">
            <button
                onClick={() => handleExport('json')}
                className="bg-gray-100 hover:bg-gray-200 text-gray-800 font-semibold py-2 px-4 rounded border border-gray-300 shadow-sm"
            >
                Export JSON Report
            </button>
            <button
                onClick={() => handleExport('csv')}
                className="bg-gray-100 hover:bg-gray-200 text-gray-800 font-semibold py-2 px-4 rounded border border-gray-300 shadow-sm"
            >
                Export CSV Errors
            </button>
        </div>
    );
}
