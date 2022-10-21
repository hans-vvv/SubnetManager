from fastapi.testclient import TestClient

from app.db.session import TestingSessionLocal
from app.tests.init_test_db import create_test_db

from main import app, get_db

create_test_db()


def override_get_db(db=None):
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_read_main():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'msg': 'Hello World'}


# Create two pools and reserve subnets until pools are depleted
def test_create_subnet_pool():
    data = {'prefixname': '10.7.0.0/24', 'description': 'test', 'prefixlen_subnets': 25}
    response = client.post('/subnetpool', json=data)
    assert response.status_code == 200


def test_get_subnetpools():
    response = client.get('/subnetpool')
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_create_subnet_pool_1():
    data = {'prefixname': '10.8.0.0/24', 'description': 'test', 'prefixlen_subnets': 25}
    response = client.post('/subnetpool', json=data)
    assert response.status_code == 200


def test_get_subnetpools_1():
    response = client.get('/subnetpool')
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_subnets():
    response = client.get('/subnet')
    assert response.status_code == 200
    assert len(response.json()) == 4


def test_reserve_subnet():
    data = {"status": "in_use", "cid": "klant-1", "prefixlen_subnets": 25}
    response = client.post('/reserve_subnet', json=data)
    assert response.status_code == 200


def test_reserve_subnet_1():
    data = {"status": "in_use", "cid": "klant-2", "prefixlen_subnets": 25}
    response = client.post('/reserve_subnet', json=data)
    assert response.status_code == 200


def test_reserve_subnet_2():
    data = {"status": "in_use", "cid": "klant-3", "prefixlen_subnets": 25}
    response = client.post('/reserve_subnet', json=data)
    assert response.status_code == 200


def test_reserve_subnet_3():
    data = {"status": "in_use", "cid": "klant-4", "prefixlen_subnets": 25}
    response = client.post('/reserve_subnet', json=data)
    assert response.status_code == 200


def test_reserve_subnet_4():
    data = {"status": "in_use", "cid": "klant-5", "prefixlen_subnets": 25}
    response = client.post('/reserve_subnet', json=data)
    assert response.status_code == 403
    assert response.json() == {"detail": "No free IPv4 resources available."}


# Create pool with existing name
def test_create_subnet_pool_2():
    data = {'prefixname': '10.8.0.0/24', 'description': 'test', 'prefixlen_subnets': 25}
    response = client.post('/subnetpool', json=data)
    assert response.status_code == 403


#





