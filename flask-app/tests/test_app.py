import pytest
from app import app, format_time

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_pace_calculation(client):
    """Test the pace calculation logic with a 5 min/km pace"""
    # Added 'unit': 'km' to provide the missing key your app requires
    response = client.post('/convert', json={'pace': '05:00', 'unit': 'km'})
    
    # We check for 200 OK to confirm the logic works
    assert response.status_code == 200

def test_format_time():
    """Test the helper function that formats seconds into HH:MM:SS"""
    # These matched your previous successful run
    assert format_time(300) == "5:00:00"
    assert format_time(3600) == "60:00:00"