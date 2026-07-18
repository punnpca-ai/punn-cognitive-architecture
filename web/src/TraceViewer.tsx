import { useState } from "react";
import { ChevronDown, ChevronUp } from "lucide-react";
import { Badge } from "@/components/ui/badge";

interface TraceEntry {
  stage: string;
  data: Record<string, unknown>;
}

interface TraceViewerProps {
  trace: TraceEntry[];
}

const STAGE_LABELS: Record<string, { label: string; icon: string; color: string; bgColor: string; description: string }> = {
  observation: {
    label: "Observation",
    icon: "👁️",
    color: "text-blue-400",
    bgColor: "bg-blue-500/10",
    description: "Initial perception and data gathering",
  },
  understanding: {
    label: "Understanding",
    icon: "🧠",
    color: "text-purple-400",
    bgColor: "bg-purple-500/10",
    description: "Comprehension of the question's context",
  },
  purpose: {
    label: "Purpose",
    icon: "🎯",
    color: "text-green-400",
    bgColor: "bg-green-500/10",
    description: "Identification of the goal and intent",
  },
  memory: {
    label: "Memory",
    icon: "💾",
    color: "text-yellow-400",
    bgColor: "bg-yellow-500/10",
    description: "Retrieval of relevant past knowledge",
  },
  mental_model: {
    label: "Mental Model",
    icon: "🔧",
    color: "text-orange-400",
    bgColor: "bg-orange-500/10",
    description: "Construction of a working model",
  },
  hypothesis: {
    label: "Hypothesis",
    icon: "💡",
    color: "text-pink-400",
    bgColor: "bg-pink-500/10",
    description: "Formation of initial theories",
  },
  evidence_evaluation: {
    label: "Evidence",
    icon: "⚖️",
    color: "text-indigo-400",
    bgColor: "bg-indigo-500/10",
    description: "Assessment of supporting evidence",
  },
  critique: {
    label: "Critique",
    icon: "🔍",
    color: "text-red-400",
    bgColor: "bg-red-500/10",
    description: "Critical examination of assumptions",
  },
  decision: {
    label: "Decision",
    icon: "✅",
    color: "text-teal-400",
    bgColor: "bg-teal-500/10",
    description: "Final choice and commitment",
  },
  communication: {
    label: "Communication",
    icon: "💬",
    color: "text-cyan-400",
    bgColor: "bg-cyan-500/10",
    description: "Formulation of the response",
  },
  reflection: {
    label: "Reflection",
    icon: "🪞",
    color: "text-violet-400",
    bgColor: "bg-violet-500/10",
    description: "Self-assessment and learning",
  },
  learning: {
    label: "Learning",
    icon: "📚",
    color: "text-lime-400",
    bgColor: "bg-lime-500/10",
    description: "Memory consolidation",
  },
};

const formatValue = (value: unknown): string => {
  if (value === null || value === undefined) return "—";
  if (typeof value === "string") return value;
  if (typeof value === "number") return value.toString();
  if (typeof value === "boolean") return value ? "true" : "false";
  if (Array.isArray(value)) return `[${value.length} items]`;
  if (typeof value === "object") return JSON.stringify(value, null, 2);
  return String(value);
};

export default function TraceViewer({ trace }: TraceViewerProps) {
  const [expandedStages, setExpandedStages] = useState<Set<number>>(new Set());

  const toggleStage = (index: number) => {
    const newExpanded = new Set(expandedStages);
    if (newExpanded.has(index)) {
      newExpanded.delete(index);
    } else {
      newExpanded.add(index);
    }
    setExpandedStages(newExpanded);
  };

  return (
    <div className="space-y-2">
      {trace.map((entry, index) => {
        const stageKey = entry.stage.toLowerCase().replace(/ /g, "_");
        const stageInfo = STAGE_LABELS[stageKey] || {
          label: entry.stage,
          icon: "🔹",
          color: "text-slate-400",
          bgColor: "bg-slate-700/20",
          description: "Unknown stage",
        };
        const isExpanded = expandedStages.has(index);

        return (
          <div
            key={index}
            className={`border rounded-lg transition-all duration-200 ${
              isExpanded
                ? `${stageInfo.bgColor} border-slate-600/50`
                : "border-slate-700/30 hover:border-slate-600/50 bg-slate-700/10"
            }`}
          >
            {/* Header */}
            <button
              onClick={() => toggleStage(index)}
              className="w-full px-4 py-3 flex items-center justify-between hover:bg-slate-700/20 transition-colors group"
            >
              <div className="flex items-center gap-3 flex-1 text-left">
                <span className="text-lg flex-shrink-0 group-hover:scale-110 transition-transform">
                  {stageInfo.icon}
                </span>
                <div className="flex-1 min-w-0">
                  <p className={`text-sm font-semibold ${stageInfo.color}`}>
                    {stageInfo.label}
                  </p>
                  <p className="text-xs text-slate-500 truncate">
                    {stageInfo.description}
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-2 flex-shrink-0">
                <Badge variant="secondary" className="text-xs font-mono">
                  {String(index + 1).padStart(2, "0")}
                </Badge>
                {isExpanded ? (
                  <ChevronUp className="w-4 h-4 text-slate-400" />
                ) : (
                  <ChevronDown className="w-4 h-4 text-slate-400" />
                )}
              </div>
            </button>

            {/* Expanded Content */}
            {isExpanded && (
              <div className="px-4 py-3 border-t border-slate-700/30 bg-slate-800/30 space-y-3 animate-slide-up">
                {Object.entries(entry.data).length > 0 ? (
                  <div className="space-y-2">
                    {Object.entries(entry.data).map(([key, value]) => (
                      <div key={key} className="text-sm">
                        <p className="text-slate-400 font-mono text-xs uppercase tracking-wider mb-1">
                          {key}
                        </p>
                        <div className="bg-slate-900/50 border border-slate-700/30 rounded p-2 font-mono text-xs text-slate-300 overflow-auto max-h-32">
                          <pre className="whitespace-pre-wrap break-words">
                            {formatValue(value)}
                          </pre>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-sm text-slate-500 italic">No data for this stage</p>
                )}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
