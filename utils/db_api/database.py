from gino import Gino
from data.config import POSTGRES_URI
import logging
db = Gino()


async def connect_to_db():
    await db.set_bind(POSTGRES_URI)
    return db


async def drop_tables(db):
    try:
        await db.gino.drop_all()
        logging.info("Tables dropped successfully.")
    except Exception as e:
        logging.error(f"Failed to drop tables: {e}")


async def create_tables(db):
    try:
        await db.gino.create_all()
        logging.info("Tables created successfully.")
    except Exception as e:
        logging.error(f"Failed to create tables: {e}")


async def create_db():
    try:
        db = await connect_to_db()
        # await drop_tables(db)
        await create_tables(db)
    except Exception as e:
        logging.error(f"Failed to create database: {e}")









