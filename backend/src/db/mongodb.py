import os, asyncio

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE = os.getenv("DATABASE")
USERS_COLLECTION = os.getenv("USERS_COLLECTION")
MESSAGES_COLLECTION = os.getenv("MESSAGES_COLLECTION")

if not all([MONGODB_URI, USERS_COLLECTION, MESSAGES_COLLECTION]):
    raise ValueError("One or more required environment variables are not set")


async def get_client():
    try:
        client = AsyncIOMotorClient(
            MONGODB_URI, serverSelectionTimeoutMS=5000, retryWrites=True
        )
        await client.server_info()
        # Check for connection
        # print("✅ MongoDB connection success")
        return client
    except Exception as e:
        raise RuntimeError(f"Failed to connect to MongoDB: {str(e)}")


async def get_user_collection():
    client = get_client()
    database = client[DATABASE]
    users_collection = database[USERS_COLLECTION]
    return users_collection


async def get_messages_collection():
    client = get_client()
    database = client[DATABASE]
    messages_collection = database[MESSAGES_COLLECTION]
    return messages_collection


# if __name__ == "__main__":
#     asyncio.run(get_client())
