import copy

from fastapi.testclient import TestClient

from src import app as app_module

client = TestClient(app_module.app)
INITIAL_ACTIVITIES = copy.deepcopy(app_module.activities)


def reset_activities():
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(INITIAL_ACTIVITIES))


def test_get_activities():
    # Arrange
    reset_activities()

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_for_activity():
    # Arrange
    reset_activities()
    email = "teststudent@mergington.edu"

    # Act
    response = client.post("/activities/Chess%20Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == "Signed up teststudent@mergington.edu for Chess Club"
    assert email in app_module.activities["Chess Club"]["participants"]


def test_signup_duplicate_fails():
    # Arrange
    reset_activities()
    email = "emma@mergington.edu"

    # Act
    response = client.post("/activities/Math%20Olympiad/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_remove_participant():
    # Arrange
    reset_activities()
    email = "michael@mergington.edu"

    # Act
    response = client.delete("/activities/Chess%20Club/participants", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == "Removed michael@mergington.edu from Chess Club"
    assert email not in app_module.activities["Chess Club"]["participants"]


def test_remove_missing_participant_returns_404():
    # Arrange
    reset_activities()
    email = "missing@student.edu"

    # Act
    response = client.delete("/activities/Chess%20Club/participants", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found for this activity"