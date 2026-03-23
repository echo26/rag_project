# MongoDB

Local MongoDB instance for the RAG project.

## Quick Start

Pull the image:

```bash
docker pull mongo
```

Run the container:

```bash
docker run --name some-mongo -d \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=secret \
  -p 27017:27017 \
  mongo
```
