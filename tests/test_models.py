import pytest
from src.database.models import Query, AddrRequest, Pagination

def test_addr_request_model():
    model = AddrRequest(addr="TEST_ADDRESS")
    assert model.addr == "TEST_ADDRESS"

def test_query_model():
    query = Query(
        name="Test",
        adress="ADDR",
        bandwidth=100,
        energy=200,
        trx=300
    )
    assert query.name == "Test"
    assert query.adress == "ADDR"
    assert query.bandwidth == 100
    assert query.energy == 200
    assert query.trx == 300

def test_pagination_model():
    pagination = Pagination(limit=10, offset=5)
    assert pagination.limit == 10
    assert pagination.offset == 5
    
    # Проверка валидации
    with pytest.raises(ValueError):
        Pagination(limit=0)
    
    with pytest.raises(ValueError):
        Pagination(limit=21)
    
    with pytest.raises(ValueError):
        Pagination(offset=-1)