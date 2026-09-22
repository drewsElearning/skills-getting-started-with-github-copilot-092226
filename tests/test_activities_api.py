from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_duplicate_signup_is_rejected():
    # Arrange
    activity = "Chess Club"
    email = "student-duplicate-123@example.com"

    # Act
    first_response = client.post(f"/activities/{activity}/signup?email={email}")
    second_response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_participant_from_activity():
    # Arrange
    activity = "Chess Club"
    email = "student-remove-456@example.com"

    # Act
    signup_response = client.post(f"/activities/{activity}/signup?email={email}")
    delete_response = client.delete(f"/activities/{activity}/signup?email={email}")
    activity_data = client.get("/activities").json()[activity]

    # Assert
    assert signup_response.status_code == 200
    assert delete_response.status_code == 200
    assert delete_response.json()["detail"] == f"Removed {email} from {activity}"
    assert email not in activity_data["participants"]
