# --------------------------------------------------
# 1. Import ChromaDB
# --------------------------------------------------

import chromadb


# --------------------------------------------------
# 2. Connect to Existing ChromaDB
# --------------------------------------------------

client = chromadb.PersistentClient(
    path="./chroma_db"
)


# --------------------------------------------------
# 3. Get Existing Collection
# --------------------------------------------------

collection = client.get_collection(
    name="peoplesphere_documents"
)


# --------------------------------------------------
# 4. Display Collection Information
# --------------------------------------------------

print("Total chunks:", collection.count())


# --------------------------------------------------
# 5. Display Stored Documents
# --------------------------------------------------

data = collection.get(
    include=["documents", "metadatas"]
)

for i in range(len(data["ids"])):
    print("\n--------------------------------")
    print("ID:", data["ids"][i])
    print("Document:", data["documents"][i])
    print("Metadata:", data["metadatas"][i])