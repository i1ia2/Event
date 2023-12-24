import atexit
from sqlalchemy import JSON, String
from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base, mapped_column, Mapped, DeclarativeBase

PG_DSN = "postgresql+asyncpg://postgres:153268425Zz@localhost:5431/flask"
engine = create_async_engine(PG_DSN, echo=False)
Session = sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase, AsyncAttrs):
     pass

class SwapiPeople(Base):
    __tablename__ = "swapi_people"

    id: Mapped[int] = mapped_column(primary_key=True)
    birth_year: Mapped[str] = mapped_column(String)
    films: Mapped[dict] = mapped_column(String)
    gender: Mapped[str] = mapped_column(String)
    hair_color: Mapped[str] = mapped_column(String)
    height: Mapped[str] = mapped_column(String)
    homeworld: Mapped[str] = mapped_column(String)
    mass: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String)
    skin_color: Mapped[str] = mapped_column(String)
    created: Mapped[str] = mapped_column(String)
    edited: Mapped[str] = mapped_column(String)
    species: Mapped[dict] = mapped_column(String)
    starships: Mapped[dict] = mapped_column(String)
    url: Mapped[str] = mapped_column(String)
    vehicles: Mapped[dict] = mapped_column(String)
    json: Mapped[dict] = mapped_column(JSON, nullable=True)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_db():
    await engine.dispose()

atexit.register(close_db)

# import atexit
# from sqlalchemy import JSON
# from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, async_sessionmaker
# from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, Mapped
#
#
# # POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "153268425Zz")
# # POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
# # POSTGRES_DB = os.getenv("POSTGRES_DB", "flask")
# # POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
# # POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5431")
#
# PG_DSN = "postgresql+asyncpg://postgres:153268425Zz@localhost:5431/flask"
#
#
# engine = create_async_engine(PG_DSN)
# Session = async_sessionmaker(engine, expire_on_commit=False)
#
#
# class Base(DeclarativeBase, AsyncAttrs):
#     pass
#
#
# class SwapiPeople(Base):
#     __tablename__ = "swapi_people"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     json: Mapped[dict] = mapped_column(JSON, nullable=True)
#
#
# async def init_db():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)
#
#
# async def close_db():
#     await engine.dispose()
