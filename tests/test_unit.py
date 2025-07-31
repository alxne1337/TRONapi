import pytest
from src.api.view import get_info
from src.database.models import AddrRequest, Query  # Добавили импорт Query
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_get_info_db_write(test_session):
    # Создаем мок Tron клиента
    mock_client = AsyncMock()
    mock_client.get_account.return_value = {
        "account_name": "unit_test",
        "balance": 500000,
        "account_resource": {"energy_window_size": 3000}
    }
    mock_client.get_bandwidth.return_value = 2000

    # Вызываем тестируемую функцию
    with patch("src.api.view.AsyncTron", 
               return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_client))):
        addr_request = AddrRequest(addr="TESTADDRESS123")
        response = await get_info(addr_request, test_session)

    # Проверяем возвращаемый объект
    assert response.name == "unit_test"
    assert response.adress == "TESTADDRESS123"
    assert response.bandwidth == 2000
    assert response.energy == 3000
    assert response.trx == 500000

    # Проверяем запись в БД
    assert response.id is not None
    db_record = await test_session.get(Query, response.id)
    
    assert db_record.name == "unit_test"
    assert db_record.adress == "TESTADDRESS123"
    assert db_record.bandwidth == 2000
    assert db_record.energy == 3000
    assert db_record.trx == 500000