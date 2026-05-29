from app.chunking import chunk_text


if __name__ == "__main__":
    text = "RDS timeout troubleshooting. " 
    chunks = chunk_text(text)

    print("chunks: ", len(chunks))
    print(chunks[0][:200])
