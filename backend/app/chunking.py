"""
# Chunking strategy with tiktoken library.

ticktock is to count exact numbers of tokens.
models: 
    - https://github.com/openai/tiktoken/blob/main/tiktoken/model.py
"""

import tiktoken

ENCODING_NAME = "o200k_base"


def chunk_text(text: str, max_tokens: int = 300, overlap_tokens: int = 50) -> list[str]:
    if not text.strip():
        return []
    
    # To avoid infinite loop in chunking creation loop.
    if overlap_tokens >= max_tokens:
        overlap_tokens = max_tokens - 1
    
    encoding = tiktoken.get_encoding(ENCODING_NAME)
    # Get exact embeddings of GPT models. You can get number of tokens by len(tokens)
    tokens = encoding.encode(text)
    len_tokens = len(tokens)

    # Total num of tokens is less than max_token, no need to split.
    if len_tokens <= max_tokens:
        return [encoding.decode(tokens).strip()]

    chunks = []
    start = 0
    while start < len_tokens:
        # Not to over actual number of tokens
        end = min(start + max_tokens, len_tokens)

        chunk_tokens = tokens[start:end]
        chunk = encoding.decode(chunk_tokens).strip()

        if chunk:
            chunks.append(chunk)

        if end >= len_tokens:
            break

        # Set start to a certain number of tokens before end
        # In order to avoid words or sentences being cut off.
        start = end - overlap_tokens

    return chunks