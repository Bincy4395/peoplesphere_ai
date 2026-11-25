import chromadb


# --------------------------------------------------
# 1. Connect to ChromaDB
# --------------------------------------------------

client = chromadb.PersistentClient(
    path="./chroma_db"
)


# --------------------------------------------------
# 2. Get Existing Collection
# --------------------------------------------------

collection = client.get_collection(
    name="peoplesphere_documents"
)


# --------------------------------------------------
# 3. Display Current Records
# --------------------------------------------------

print("Records before deletion:", collection.count())


# --------------------------------------------------
# 4. Delete All Records
# --------------------------------------------------

collection.delete(
    ids=collection.get()["ids"]
)


# --------------------------------------------------
# 5. Verify Deletion
# --------------------------------------------------

print("Records after deletion:", collection.count())