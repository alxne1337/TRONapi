import pytest
from fastapi.testclient import TestClient
from sqlmodel import select
from src.database.models import Query
from unittest.mock import patch

@pytest.mark.asyncio
async def test_get_info_from_api(test_app, test_session):
    # Мокаем Tron клиент
    with patch("src.api.view.AsyncTron") as MockTron:
        mock_client = MockTron.return_value.__aenter__.return_value
        
        # Настраиваем мок-ответы
        mock_client.get_account.return_value = {
            "account_name": "test_name",
            "balance": 1000000,
            "account_resource": {"energy_window_size": 5000}
        }
        mock_client.get_bandwidth.return_value = 1000

        # Используем синхронный TestClient для FastAPI
        client = TestClient(test_app)
        response = client.post(
            "/API/fromAPI",
            json={"addr": "TXYZabcdef1234567890"}
        )

        # Проверяем ответ API
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "test_name"
        assert data["adress"] == "TXYZabcdef1234567890"
        assert data["bandwidth"] == 1000
        assert data["energy"] == 5000
        assert data["trx"] == 1000000

        # Проверяем запись в БД
        result = await test_session.execute(select(Query))
        db_record = result.scalars().first()
        
        assert db_record.name == "test_name"
        assert db_record.adress == "TXYZabcdef1234567890"
        assert db_record.bandwidth == 1000
        assert db_record.energy == 5000
        assert db_record.trx == 1000000