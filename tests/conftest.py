import pytest
from fastapi import FastAPI
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.main import app as main_app  # Импортируем основное приложение
from src.database.database import get_session

# Настройка тестовой БД (SQLite в памяти)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Создаем движок для тестовой БД
test_engine = create_async_engine(TEST_DATABASE_URL, echo=True)

# Создаем фабрику сессий для тестов
TestingSessionLocal = sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Фикстура для инициализации БД
@pytest.fixture(autouse=True, scope="function")
async def init_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

# Фикстура для тестовой сессии
@pytest.fixture
async def test_session(init_db):
    async with TestingSessionLocal() as session:
        yield session

# Фикстура для тестового приложения
@pytest.fixture
def test_app(test_session):
    # Переопределяем зависимость для БД
    async def override_get_session():
        yield test_session

    # Создаем копию приложения
    app = FastAPI()
    app.include_router(main_app.router)
    app.dependency_overrides[get_session] = override_get_session
    
    return app