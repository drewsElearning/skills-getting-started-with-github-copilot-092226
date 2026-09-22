from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_duplicate_signup_is_rejected():
    email = "student-duplicate-123@example.com"
    activity = "Chess Club"

    first_response = client.post(f"/activities/{activity}/signup?email={email}")
    assert first_response.status_code == 200

    second_response = client.post(f"/activities/{activity}/signup?email={email}")
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student already signed up for this activity"
