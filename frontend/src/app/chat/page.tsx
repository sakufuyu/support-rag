"use client";

import { useState } from "react";
import { queryDocuments } from "@/lib/api";

type Source = {
  filename: string;
  chunk_index: number;
  content: string;
  distance: number;
};

export default function ChatPage() {
  const [question, setQuestion] = useState("");
  const [accessCode, setAccessCode] = useState("demo-access-code");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState<Source[]>([]);
  const [loading, setLoading] = useState(false);

  async function handleAsk() {
    setLoading(true);
    setAnswer("");
    setSources([]);

    try {
      const result = await queryDocuments(question, accessCode);
      setAnswer(result.answer);
      setSources(result.sources);
    } catch (error) {
      setAnswer(`Error: ${String(error)}`);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="max-w-4xl mx-auto p-8">
      <h1 className="text-2xl font-bold mb-4">Ask SupportRAG</h1>

      <label className="block mb-2 font-medium">Access Code</label>
      <input
        value={accessCode}
        onChange={(e) => setAccessCode(e.target.value)}
        className="border rounded p-2 w-full mb-4"
      />

      <label className="block mb-2 font-medium">Question</label>
      <textarea
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        className="border rounded p-2 w-full h-32 mb-4"
        placeholder="What should I check when an RDS connection times out?"
      />

      <button
        onClick={handleAsk}
        disabled={loading}
        className="border px-4 py-2 rounded"
      >
        {loading ? "Thinking..." : "Ask"}
      </button>

      {answer && (
        <section className="mt-8">
          <h2 className="text-xl font-bold mb-2">Answer</h2>
          <p className="whitespace-pre-wrap border rounded p-4">{answer}</p>
        </section>
      )}

      {sources.length > 0 && (
        <section className="mt-8">
          <h2 className="text-xl font-bold mb-2">Sources</h2>
          <div className="space-y-4">
            {sources.map((source, index) => (
              <div key={index} className="border rounded p-4">
                <p className="font-semibold">
                  {source.filename} — chunk {source.chunk_index}
                </p>
                <p className="text-sm text-gray-600">
                  distance: {source.distance.toFixed(4)}
                </p>
                <p className="mt-2 whitespace-pre-wrap">{source.content}</p>
              </div>
            ))}
          </div>
        </section>
      )}
    </main>
  );
}