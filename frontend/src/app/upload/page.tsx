"use client";

import { useState } from "react";
import { uploadDocument } from "@/lib/api";

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<string>("");

  async function handleUpload() {
    if (!file) return;

    setStatus("Uploading...");

    try {
      const result = await uploadDocument(file);
      setStatus(`Uploaded: ${result.filename}`);
    } catch (error) {
      setStatus(`Error: ${String(error)}`);
    }
  }

  return (
    <main className="max-w-3xl mx-auto p-8">
      <h1 className="text-2xl font-bold mb-4">Upload Document</h1>

      <input
        type="file"
        accept=".txt,.md"
        onChange={(e) => setFile(e.target.files?.[0] ?? null)}
        className="mb-4"
      />

      <button
        onClick={handleUpload}
        className="border px-4 py-2 rounded"
      >
        Upload
      </button>

      {status && <p className="mt-4 whitespace-pre-wrap">{status}</p>}
    </main>
  );
}