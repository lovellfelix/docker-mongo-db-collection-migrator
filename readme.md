# MongoDB collection migrator

Docker image for migrating collection from one database to another.

Usage:

```bash
docker run -ti  \
    -e MONGO_URI_SOURCE="mongodb+srv://user@pass:hostname/source?retryWrites=true&w=majority" \
    -e MONGO_SOURCE_DATABASE="source" \
    -e MONGO_SOURCE_Collection="collection_a" \
    -e MONGO_URI_DESTINATION="mongodb+srv://user@pass:hostname/destination?retryWrites=true&w=majority" \
    -e MONGO_DESTINATION_DATABASE="destination" \
    -e MONGO_DESTINATION_Collection="collection_b" \
    lovellfelix/mongo-col-migrator
```