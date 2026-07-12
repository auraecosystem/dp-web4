// auraecosystem/ai-workspace/web4/components/IdentityTelemetry.jsx
import React from 'react';

export default function IdentityTelemetry({ parsedLCT }) {
  if (!parsedLCT) {
    return <div className="p-4 bg-gray-800 text-gray-400 rounded-lg">No active identity payload streaming.</div>;
  }

  const { agentId, t3Tensor, coherence, metabolism, isValid, isAlive } = parsedLCT;

  // Helper calculation to compute average trust for threshold warnings
  const t3Average = (t3Tensor.competence + t3Tensor.reliability + t3Tensor.integrity + t3Tensor.alignment + t3Tensor.transparency) / 5;

  return (
    <div className="p-6 bg-slate-900 border border-slate-800 rounded-xl shadow-2xl text-slate-100 max-w-xl font-mono text-sm">
      
      {/* Component Header Identity Banner */}
      <div className="flex justify-between items-center border-b border-slate-800 pb-4 mb-4">
        <div>
          <span className="text-xs text-slate-500 block uppercase tracking-wider">Agent Identifier</span>
          <h2 className="text-base font-bold text-sky-400">{agentId}</h2>
        </div>
        <div className="flex gap-2">
          <span className={`px-2.5 py-1 text-xs rounded-full font-bold uppercase ${isValid ? 'bg-emerald-950 text-emerald-400 border border-emerald-800' : 'bg-rose-950 text-rose-400 border border-rose-800'}`}>
            {isValid ? 'Coherent' : 'Fractured'}
          </span>
          <span className={`px-2.5 py-1 text-xs rounded-full font-bold uppercase ${isAlive ? 'bg-teal-950 text-teal-400 border border-teal-800' : 'bg-red-950 text-red-400 border border-red-800 animate-pulse'}`}>
            {isAlive ? 'Active Agent' : 'Metabolic Death'}
          </span>
        </div>
      </div>

      {/* Grid displaying the primary metrics metrics matrices */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        {/* Metabolism Column Section */}
        <div className="bg-slate-950 p-4 border border-slate-800/60 rounded-lg">
          <h3 className="text-xs font-bold text-amber-500 uppercase tracking-widest mb-3">Metabolic Budget</h3>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-slate-500">ATP Balance:</span>
              <span className={`font-bold ${metabolism.atp > 20 ? 'text-amber-400' : 'text-rose-500 font-extrabold'}`}>{metabolism.atp} Packets</span>
            </div>
            <div className="w-full bg-slate-900 rounded-full h-1.5 overflow-hidden">
              <div className="bg-amber-500 h-1.5 rounded-full" style={{ width: `${Math.min(100, metabolism.atp)}%` }}></div>
            </div>
            <div className="flex justify-between text-xs text-slate-400 mt-1">
              <span>ADP Debt: {metabolism.adp}</span>
              <span>Burn Rate: {metabolism.burnRate}/tick</span>
            </div>
          </div>
        </div>

        {/* 4D Coherence Metrics Section */}
        <div className="bg-slate-950 p-4 border border-slate-800/60 rounded-lg">
          <h3 className="text-xs font-bold text-emerald-500 uppercase tracking-widest mb-3">4D Coherence Matrix</h3>
          <div className="grid grid-cols-2 gap-2 text-xs">
            <div className="p-2 bg-slate-900/60 rounded border border-slate-800">
              <span className="text-slate-500 block">Spatial:</span>
              <span className="font-bold text-emerald-400">{coherence.spatial.toFixed(2)}</span>
            </div>
            <div className="p-2 bg-slate-900/60 rounded border border-slate-800">
              <span className="text-slate-500 block">Capability:</span>
              <span className="font-bold text-emerald-400">{coherence.capability.toFixed(2)}</span>
            </div>
            <div className="p-2 bg-slate-900/60 rounded border border-slate-800">
              <span className="text-slate-500 block">Temporal:</span>
              <span className="font-bold text-emerald-400">{coherence.temporal.toFixed(2)}</span>
            </div>
            <div className="p-2 bg-slate-900/60 rounded border border-slate-800">
              <span className="text-slate-500 block">Relational:</span>
              <span className={`font-bold ${coherence.relational < 0.4 ? 'text-rose-400' : 'text-emerald-400'}`}>{coherence.relational.toFixed(2)}</span>
            </div>
          </div>
        </div>

      </div>

      {/* 5D Trust Tensor Vector Breakdown Block */}
      <div className="mt-4 bg-slate-950 p-4 border border-slate-800/60 rounded-lg">
        <div className="flex justify-between items-center mb-3">
          <h3 className="text-xs font-bold text-sky-500 uppercase tracking-widest">5D Trust Tensor Vectors</h3>
          <span className={`text-xs px-2 py-0.5 rounded ${t3Average > 0.5 ? 'text-sky-400 bg-sky-950/40' : 'text-rose-400 bg-rose-950/40'}`}>
            Avg: {t3Average.toFixed(2)} / Threshold: 0.50
          </span>
        </div>
        <div className="space-y-1.5 text-xs">
          {[
            { label: 'Competence', val: t3Tensor.competence },
            { label: 'Reliability', val: t3Tensor.reliability },
            { label: 'Integrity', val: t3Tensor.integrity },
            { label: 'Alignment', val: t3Tensor.alignment },
            { label: 'Transparency', val: t3Tensor.transparency }
          ].map((vector) => (
            <div key={vector.label} className="flex items-center gap-3">
              <span className="text-slate-400 w-24">{vector.label}:</span>
              <div className="flex-1 bg-slate-900 h-2 rounded-full overflow-hidden flex">
                <div 
                  className={`h-full rounded-full ${vector.val > 0.5 ? 'bg-sky-500' : 'bg-rose-500'}`} 
                  style={{ width: `${vector.val * 100}%` }}
                />
              </div>
              <span className={`w-8 text-right font-bold ${vector.val > 0.5 ? 'text-sky-400' : 'text-rose-400'}`}>
                {vector.val.toFixed(2)}
              </span>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
}
