from sqlalchemy import create_engine, text
from config import settings
import logging

logger = logging.getLogger(__name__)

def migrate_add_error_message():
    engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
    
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE documents ADD COLUMN error_message TEXT"))
            conn.commit()
            logger.info("Added error_message column to documents table")
        except Exception as e:
            if "duplicate column name" in str(e).lower():
                logger.info("error_message column already exists")
            else:
                logger.error(f"Migration failed: {e}")
                raise

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    migrate_add_error_message()
    print("Migration completed!")
