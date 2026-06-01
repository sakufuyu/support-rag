import Link from "next/link";

export default function Home() {
  return (
    <main className="max-w-3xl mx-auto p-8">
      <h1 className="text-3xl font-bold mb-4">SupportRAG</h1>
      <p className="mb-6">
        Upload technical support documents and ask source-grounded questions using OpenAI-powered RAG.
      </p>

      <div className="flex gap-4">
        <Link href="/upload" className="underline">
          Upload Documents
        </Link>
        <Link href="/chat" className="underline">
          Chat
        </Link>
      </div>
    </main>
  );
}