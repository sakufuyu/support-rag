# Failure Cases

## 1. Vague Questions
If the user asks vague questions, retrieval may return broadly related but not directly useful chunks.

Mitigation:
- query rewriting
- asking clarifying questions
- showing retrieved sources clearly

## 2. Similar Documents
If multiple runbooks contain similar wording, top-k retrieval may select the wrong document.

Mitigation:
- hybrid search
- metadata filtering
- reranking

## 3. Outdated Documents
If older and newer documents conflict, the model may use outdated instructions.

Mitigation:
- document version metadata
- recency filtering
- conflict detection

## 4. Chunk Size Problems
Chunks that are too small lose context. Chunks that are too large reduce retrieval precision.

Mitigation:
- evaluate different chunk sizes
- use overlap
- measure retrieval hit rate

## 5. Prompt Injection in Documents
A malicious document could contain instructions such as "Ignore previous instructions."

Mitigation:
- system prompt tells the model to treat retrieved text as untrusted content
- do not allow documents to override system instructions
- add prompt injection test cases

## 6. No-Answer Questions
If the documents do not contain enough information, the model may hallucinate.

Mitigation:
- require the model to answer only from context
- return "I don't know based on the provided documents"
- add no-answer eval cases