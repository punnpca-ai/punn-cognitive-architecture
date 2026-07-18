import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Spinner } from "@/components/ui/spinner";
import { AlertCircle, Brain, CheckCircle2, Zap, Copy, Check } from "lucide-react";
import { Streamdown } from "streamdown";

interface TraceEntry {
  stage: string;
  data: Record<string, unknown>;
}

interface AnalyzeResponse {
  question: string;
  response: string;
  trace: TraceEntry[];
  notes: string[];
}

const STAGE_LABELS: Record<string, { label: string; icon: string; color: string; bgColor: string }> = {
  observation: { label: "Observation", icon: "👁️", color: "text-blue-400", bgColor: "bg-blue-500/10" },
  understanding: { label: "Understanding", icon: "🧠", color: "text-purple-400", bgColor: "bg-purple-500/10" },
  purpose: { label: "Purpose", icon: "🎯", color: "text-green-400", bgColor: "bg-green-500/10" },
  memory: { label: "Memory", icon: "💾", color: "text-yellow-400", bgColor: "bg-yellow-500/10" },
  mental_model: { label: "Mental Model", icon: "🔧", color: "text-orange-400", bgColor: "bg-orange-500/10" },
  hypothesis: { label: "Hypothesis", icon: "💡", color: "text-pink-400", bgColor: "bg-pink-500/10" },
  evidence_evaluation: { label: "Evidence", icon: "⚖️", color: "text-indigo-400", bgColor: "bg-indigo-500/10" },
  critique: { label: "Critique", icon: "🔍", color: "text-red-400", bgColor: "bg-red-500/10" },
  decision: { label: "Decision", icon: "✅", color: "text-teal-400", bgColor: "bg-teal-500/10" },
  communication: { label: "Communication", icon: "💬", color: "text-cyan-400", bgColor: "bg-cyan-500/10" },
  reflection: { label: "Reflection", icon: "🪞", color: "text-violet-400", bgColor: "bg-violet-500/10" },
  learning: { label: "Learning", icon: "📚", color: "text-lime-400", bgColor: "bg-lime-500/10" },
};

export default function Dashboard() {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalyzeResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);

  const handleAnalyze = async () => {
    if (!question.trim()) {
      setError("Please enter a question");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // Use environment variable or fallback to localhost for development
      const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:8000/analyze";
      const response = await fetch(apiUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.statusText}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to analyze question");
    } finally {
      setLoading(false);
    }
  };

  const handleCopyResponse = () => {
    if (result?.response) {
      navigator.clipboard.writeText(result.response);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950">
      {/* Animated background elements */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-10 w-72 h-72 bg-cyan-500/5 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-20 right-10 w-96 h-96 bg-purple-500/5 rounded-full blur-3xl animate-pulse" />
      </div>

      {/* Header */}
      <header className="border-b border-slate-700/50 bg-slate-900/40 backdrop-blur-xl sticky top-0 z-40">
        <div className="container py-5">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-lg">
                <Brain className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent">
                  PCA Cognitive DNA
                </h1>
                <p className="text-xs text-slate-400">Transparent AI Decision Making</p>
              </div>
            </div>
            <Badge variant="outline" className="text-cyan-400 border-cyan-400/50 bg-cyan-400/5">
              <Zap className="w-3 h-3 mr-1" />
              v0.2.0
            </Badge>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container py-8 relative z-10">
        {/* Input Section */}
        <Card className="mb-8 border-slate-700/50 bg-slate-800/30 backdrop-blur-sm shadow-2xl hover:shadow-cyan-500/10 transition-shadow duration-300">
          <div className="p-6 md:p-8">
            <label className="block text-sm font-semibold text-slate-200 mb-4 flex items-center gap-2">
              <Brain className="w-4 h-4 text-cyan-400" />
              What's your question?
            </label>
            <Textarea
              placeholder="Ask anything... (e.g., 'Should I change jobs?' or 'How do I make this decision?')"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && e.ctrlKey && !loading && question.trim()) {
                  handleAnalyze();
                }
              }}
              className="min-h-28 bg-slate-700/30 border-slate-600/50 text-white placeholder:text-slate-500 focus:border-cyan-400 focus:ring-cyan-400/20 resize-none text-base leading-relaxed"
              disabled={loading}
            />
            <div className="flex flex-col sm:flex-row gap-3 mt-6">
              <Button
                onClick={handleAnalyze}
                disabled={loading || !question.trim()}
                className="bg-gradient-to-r from-cyan-500 to-blue-500 hover:from-cyan-600 hover:to-blue-600 text-white font-semibold shadow-lg hover:shadow-cyan-500/50 transition-all duration-200 disabled:opacity-50"
              >
                {loading ? (
                  <>
                    <Spinner className="w-4 h-4 mr-2" />
                    Analyzing...
                  </>
                ) : (
                  <>
                    <Zap className="w-4 h-4 mr-2" />
                    Analyze
                  </>
                )}
              </Button>
              <Button
                variant="outline"
                onClick={() => {
                  setQuestion("");
                  setResult(null);
                  setError(null);
                }}
                disabled={loading}
                className="border-slate-600/50 text-slate-300 hover:bg-slate-700/50 hover:text-slate-200"
              >
                Clear
              </Button>
            </div>
            {error && (
              <div className="mt-6 flex gap-3 p-4 bg-red-900/20 border border-red-700/50 rounded-lg animate-fade-in">
                <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
                <p className="text-sm text-red-300">{error}</p>
              </div>
            )}
          </div>
        </Card>

        {/* Results Section */}
        {result && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 animate-slide-up">
            {/* Left: Response */}
            <div className="lg:col-span-2">
              <Card className="border-slate-700/50 bg-slate-800/30 backdrop-blur-sm h-full shadow-2xl">
                <div className="p-6 md:p-8">
                  <div className="flex items-center justify-between mb-6">
                    <h2 className="text-lg font-semibold text-white flex items-center gap-2">
                      <CheckCircle2 className="w-5 h-5 text-green-400" />
                      Response
                    </h2>
                    <button
                      onClick={handleCopyResponse}
                      className="p-2 hover:bg-slate-700/50 rounded-lg transition-colors"
                      title="Copy response"
                    >
                      {copied ? (
                        <Check className="w-4 h-4 text-green-400" />
                      ) : (
                        <Copy className="w-4 h-4 text-slate-400 hover:text-slate-300" />
                      )}
                    </button>
                  </div>
                  <div className="prose prose-invert max-w-none text-slate-300 [&_*]:text-slate-300 [&_a]:text-cyan-400 [&_a]:hover:text-cyan-300 [&_strong]:text-slate-100 [&_code]:text-cyan-300 [&_code]:bg-slate-700/50 [&_code]:px-2 [&_code]:py-1 [&_code]:rounded">
                    <Streamdown>{result.response}</Streamdown>
                  </div>
                  {result.notes.length > 0 && (
                    <div className="mt-8 pt-6 border-t border-slate-700/50">
                      <p className="text-xs font-semibold text-slate-400 mb-3 uppercase tracking-wider">
                        📌 Notes
                      </p>
                      <ul className="space-y-2">
                        {result.notes.map((note, i) => (
                          <li key={i} className="text-sm text-slate-400 flex gap-3">
                            <span className="text-slate-600 flex-shrink-0">•</span>
                            <span>{note}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </Card>
            </div>

            {/* Right: Cognitive DNA Trace */}
            <div className="lg:col-span-1">
              <Card className="border-slate-700/50 bg-slate-800/30 backdrop-blur-sm h-full shadow-2xl">
                <div className="p-6 md:p-8">
                  <h2 className="text-lg font-semibold text-white mb-6 flex items-center gap-2">
                    <Brain className="w-5 h-5 text-cyan-400" />
                    <span>Cognitive DNA</span>
                    <Badge variant="secondary" className="ml-auto text-xs">
                      {result.trace.length} steps
                    </Badge>
                  </h2>
                  <div className="space-y-3">
                    {result.trace.map((entry, index) => {
                      const stageKey = entry.stage.toLowerCase().replace(/ /g, "_");
                      const stageInfo = STAGE_LABELS[stageKey] || {
                        label: entry.stage,
                        icon: "🔹",
                        color: "text-slate-400",
                        bgColor: "bg-slate-700/20",
                      };
                      return (
                        <div
                          key={index}
                          className={`flex items-start gap-3 p-3 rounded-lg ${stageInfo.bgColor} border border-slate-700/30 hover:border-slate-600/50 transition-all duration-200 group`}
                        >
                          <div className="text-lg flex-shrink-0 group-hover:scale-110 transition-transform">
                            {stageInfo.icon}
                          </div>
                          <div className="flex-1 min-w-0">
                            <p className={`text-xs font-semibold ${stageInfo.color}`}>
                              {stageInfo.label}
                            </p>
                            <p className="text-xs text-slate-500 truncate mt-1">
                              {typeof entry.data === "object"
                                ? Object.keys(entry.data).join(", ")
                                : String(entry.data)}
                            </p>
                          </div>
                          <div className="text-xs text-slate-600 flex-shrink-0 font-mono">
                            {String(index + 1).padStart(2, "0")}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              </Card>
            </div>
          </div>
        )}

        {/* Empty State */}
        {!result && !loading && (
          <Card className="border-slate-700/50 bg-slate-800/20 backdrop-blur-sm">
            <div className="p-16 text-center">
              <div className="inline-block p-4 bg-gradient-to-br from-cyan-500/20 to-blue-500/20 rounded-full mb-6">
                <Brain className="w-12 h-12 text-cyan-400" />
              </div>
              <h3 className="text-xl font-semibold text-slate-200 mb-2">Ready to think together</h3>
              <p className="text-slate-400 max-w-sm mx-auto">
                Ask a question above and watch the Cognitive DNA trace unfold step by step
              </p>
              <p className="text-xs text-slate-500 mt-6">
                💡 Tip: Press <kbd className="px-2 py-1 bg-slate-700/50 rounded text-slate-300">Ctrl+Enter</kbd> to analyze
              </p>
            </div>
          </Card>
        )}
      </main>
    </div>
  );
}
