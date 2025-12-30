'use client';

import { useValidationStore } from '@/store/useValidationStore';
import FileUpload from '@/components/FileUpload';
import RuleConfigPanel from '@/components/RuleConfig';
import ResultsDashboard from '@/components/ResultsDashboard';

export default function Home() {
  const { step, filename, previewData, reset } = useValidationStore();

  return (
    <main className="min-h-screen bg-gray-50 text-gray-900 font-sans">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900 tracking-tight">Data Quality & Validation Tool v.1</h1>
          {step !== 'upload' && (
            <button onClick={reset} className="text-sm text-gray-500 hover:text-blue-600">New Upload</button>
          )}
        </div>
      </header>

      <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">

        {/* Stepper */}
        <div className="mb-8">
          <div className="flex items-center justify-center space-x-4">
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${step === 'upload' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-600'}`}>1. Upload</span>
            <div className="w-8 h-px bg-gray-300"></div>
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${step === 'config' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-600'}`}>2. Configure</span>
            <div className="w-8 h-px bg-gray-300"></div>
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${step === 'results' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-600'}`}>3. Results</span>
          </div>
        </div>

        {step === 'upload' && (
          <div className="max-w-xl mx-auto">
            <h2 className="text-lg font-medium text-gray-700 mb-4 text-center">Get started by uploading your dataset</h2>
            <FileUpload />
          </div>
        )}

        {step === 'config' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="lg:col-span-1">
              <RuleConfigPanel />
            </div>
            <div className="lg:col-span-2">
              <div className="bg-white rounded-lg shadow-sm border p-6">
                <h3 className="text-lg font-medium mb-4">File Preview: {filename}</h3>
                <div className="overflow-x-auto">
                  <table className="min-w-full text-sm divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        {previewData.length > 0 && Object.keys(previewData[0]).map(k => (
                          <th key={k} className="px-3 py-2 text-left font-semibold text-gray-600">{k}</th>
                        ))}
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200">
                      {previewData.map((row, i) => (
                        <tr key={i}>
                          {Object.values(row).map((v: any, j) => (
                            <td key={j} className="px-3 py-2 whitespace-nowrap text-gray-500">{v?.toString()}</td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        )}

        {step === 'results' && (
          <ResultsDashboard />
        )}

      </div>
    </main>
  );
}
