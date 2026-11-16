from src.app import activities

EMAIL = "new.student@mergington.edu"


def test_root_redirects_to_static_index(client):
    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_all_activities_with_details(client):
    # Arrange
    expected_names = set(activities)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert set(data) == expected_names
    chess = data["Chess Club"]
    assert set(chess) == {"description", "schedule", "max_participants", "participants"}


def test_signup_adds_student_to_activity(client):
    # Arrange
    activity_name = "Art Club"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": EMAIL})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {EMAIL} for {activity_name}"}
    assert EMAIL in activities[activity_name]["participants"]


def test_signup_unknown_activity_returns_404(client):
    # Arrange
    activity_name = "Underwater Basket Weaving"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": EMAIL})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_twice_returns_400_and_does_not_duplicate(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = activities[activity_name]["participants"][0]
    before = list(activities[activity_name]["participants"])

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": existing_email})

    # Assert
    assert response.status_code == 400
    assert activities[activity_name]["participants"] == before


def test_cancel_signup_removes_student_from_activity(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = activities[activity_name]["participants"][0]

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": existing_email})

    # Assert
    assert response.status_code == 200
    assert existing_email not in activities[activity_name]["participants"]


def test_cancel_signup_unknown_activity_returns_404(client):
    # Arrange
    activity_name = "Underwater Basket Weaving"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": EMAIL})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_cancel_signup_for_student_not_enrolled_returns_404(client):
    # Arrange
    activity_name = "Chess Club"
    before = list(activities[activity_name]["participants"])

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": EMAIL})

    # Assert
    assert response.status_code == 404
    assert activities[activity_name]["participants"] == before
