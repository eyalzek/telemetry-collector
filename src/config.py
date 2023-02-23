import os


class Config:
    # DATABASE_API = os.getenv('DATABASE_API', 'postgresql+asyncpg')
    DATABASE_API = os.getenv('DATABASE_API', 'postgresql')
    DATABASE_HOST = os.getenv('DATABASE_HOST')
    DATABASE_NAME = os.getenv('DATABASE_NAME', 'requests')
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
    DATABASE_PORT = os.getenv('DATABASE_PORT', '5432')
    DATABASE_USER = os.getenv('DATABASE_USER')
    DATABASE_CONFIG = f'{DATABASE_API}://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'
