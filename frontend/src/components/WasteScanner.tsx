import React, { useState, useRef } from 'react';
import { Upload, Camera, Loader2, CheckCircle2, Sparkles } from 'lucide-react';
import { api } from '../api/client';
import type { VisionResult } from '../types';
import { DisposalCard } from './DisposalCard';

interface WasteScannerProps {
  onScanComplete?: (result: VisionResult) => void;
}

export const WasteScanner: React.FC<WasteScannerProps> = ({ onScanComplete }) => {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [preview, setPreview] = useState<string | null>(null);
  const [result, setResult] = useState<VisionResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = async (file: File) => {
    if (!file.type.startsWith('image/')) {
      setError('Please select a valid image file');
      return;
    }
    const reader = new FileReader();
    reader.onloadend = () => {
      setPreview(reader.result as string);
    };
    reader.readAsDataURL(file);

    setIsAnalyzing(true);
    setError(null);
    setResult(null);

    try {
      const visionResult = await api.classifyWaste(file);
      setResult(visionResult);
      if (onScanComplete) onScanComplete(visionResult);
    } catch (err: any) {
      setError(err.message || 'Failed to analyze image');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) handleFileSelect(file);
  };

  return (
    <div className="card bg-[#12121a]/85 backdrop-blur-md border border-white/10 shadow-xl">
      <div className="flex items-center gap-2 mb-6">
        <Sparkles className="h-5 w-5 text-eco-400" />
        <h2 className="text-xl font-bold text-white tracking-tight">Waste Scanner</h2>
      </div>

      <input ref={fileInputRef} type="file" accept="image/*" onChange={handleFileChange} className="hidden" />

      {!preview ? (
        <div className="border-2 border-dashed border-white/20 rounded-2xl p-8 text-center transition-colors hover:border-eco-400/60 group bg-white/[0.02]">
          <button onClick={() => fileInputRef.current?.click()} className="btn-primary mb-3">
            <Upload className="h-4 w-4 inline mr-2" />
            Upload Image
          </button>
          <p className="text-sm text-gray-300">Clear photo of a waste item — JPEG or PNG, up to 8MB</p>
        </div>
      ) : (
        <div className="space-y-5">
          <div className="relative rounded-xl overflow-hidden bg-black/40 border border-white/10 shadow-inner">
            <img src={preview} alt="Waste preview" className="w-full object-contain max-h-[280px]" />
            {isAnalyzing && (
              <div className="absolute inset-0 bg-black/60 backdrop-blur-[2px] flex items-center justify-center">
                <div className="flex items-center gap-3 text-white font-medium">
                  <Loader2 className="h-5 w-5 animate-spin text-eco-400" />
                  Analyzing...
                </div>
              </div>
            )}
            {result && (
              <div className="absolute top-3 right-3">
                <div className="bg-emerald-500 rounded-full p-1 shadow-lg">
                  <CheckCircle2 className="h-6 w-6 text-white" />
                </div>
              </div>
            )}
          </div>

          {result && (
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-bold text-white">{result.display_name}</h3>
                <span className="badge bg-eco-500/20 text-eco-300 border border-eco-500/30">
                  {Math.round(result.score * 100)}% confidence
                </span>
              </div>
              <p className="text-xs text-gray-400 uppercase tracking-wide">Source: {result.source}</p>
              {result.explanation && (
                <p className="text-sm text-gray-300 italic">{result.explanation}</p>
              )}
            </div>
          )}

          {error && (
            <div className="p-3 bg-red-950/40 border border-red-500/30 rounded-xl text-sm text-red-200">
              {error}
            </div>
          )}

          <button onClick={() => { setPreview(null); setResult(null); setError(null); fileInputRef.current!.value = ''; }} className="btn-secondary w-full">
            Scan Another Item
          </button>
        </div>
      )}

      {result && (
        <div className="mt-6">
          <DisposalCard
            category={result.category}
            displayName={result.display_name}
            disposal={result.disposal}
          />
        </div>
      )}
    </div>
  );
};
