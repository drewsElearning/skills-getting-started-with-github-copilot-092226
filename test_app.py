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


def test_unregister_participant_from_activity():
    email = "student-remove-456@example.com"
    activity = "Chess Club"

    signup_response = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_response.status_code == 200

    delete_response = client.delete(f"/activities/{activity}/signup?email={email}")
    assert delete_response.status_code == 200
    assert delete_response.json()["detail"] == f"Removed {email} from {activity}"

    activity_data = client.get("/activities").json()[activity]
    assert email not in activity_data["participants"]
