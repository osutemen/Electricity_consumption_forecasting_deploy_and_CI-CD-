from fastapi.testclient import TestClient

try:
    from main import app
except:
    from fastapi_energy_prediction.main import app

client = TestClient(app)


def test_predict_advertising():
    response = client.post("/prediction/energy_prediction_for_5days", json={
        "Date": '23.07.2024 10:00'
    })

    assert response.status_code == 200
    assert isinstance(response.json()['result'], str), 'Result wrong type!'