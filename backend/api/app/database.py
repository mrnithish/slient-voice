"""
MongoDB database connection and utilities
"""

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
import logging

from app.config import settings

logger = logging.getLogger(__name__)

# Global database client
client: AsyncIOMotorClient = None
database = None


async def init_db():
    """Initialize MongoDB connection"""
    global client, database
    
    try:
        client = AsyncIOMotorClient(
            settings.MONGODB_URI,
            serverSelectionTimeoutMS=5000
        )
        
        # Test connection
        await client.admin.command('ping')
        database = client[settings.DATABASE_NAME]
        
        # Create indexes
        await create_indexes()
        
        logger.info(f"Connected to MongoDB: {settings.DATABASE_NAME}")
        
    except ConnectionFailure as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise
    except Exception as e:
        logger.error(f"Database initialization error: {e}")
        raise


async def close_db():
    """Close MongoDB connection"""
    global client
    
    if client:
        client.close()
        logger.info("MongoDB connection closed")


async def create_indexes():
    """Create database indexes for performance"""
    if not database:
        return
    
    try:
        # Users collection indexes
        users_collection = database.users
        await users_collection.create_index("email", unique=True)
        await users_collection.create_index("provider_id")
        
        # Voice entries collection indexes
        entries_collection = database.voice_entries
        await entries_collection.create_index("user_id")
        await entries_collection.create_index([("user_id", 1), ("created_at", -1)])
        
        logger.info("Database indexes created")
        
    except Exception as e:
        logger.warning(f"Error creating indexes: {e}")


def get_database():
    """Get database instance"""
    return database



