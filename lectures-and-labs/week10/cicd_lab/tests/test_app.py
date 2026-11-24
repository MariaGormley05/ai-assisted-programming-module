import pytest
from hello_app.webapp import app

def test_home_route():
    """Test the home route returns 200 OK."""
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
