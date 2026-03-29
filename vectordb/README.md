# Vector DB

Start Qdrant with persistent storage:

```bash
docker run -d -p 6333:6333 -v $(pwd)/qdrant_storage:/qdrant/storage qdrant/qdrant
```
