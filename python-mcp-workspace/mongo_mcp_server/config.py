import os


MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DEFAULT_DATABASE_NAME = os.getenv("MONGO_DEFAULT_DATABASE", "users")
