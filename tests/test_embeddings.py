from app.rag.embeddings import generate_embedding

text = "Heavy rainfall can cause flooding."

embedding = generate_embedding(text)

print("Embedding generated successfully!")
print("Dimensions:", len(embedding))
print("First 5 values:", embedding[:5])