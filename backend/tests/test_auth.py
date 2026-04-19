class TestRegister:
    def test_register_success(self, client):
        response = client.post("/register", json={
            "username": "newuser",
            "email": "new@example.com",
            "password": "password123",
        })
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "newuser"
        assert data["email"] == "new@example.com"
        assert "id" in data

    def test_register_duplicate_username(self, client, test_user):
        response = client.post("/register", json={
            "username": "testuser",
            "email": "other@example.com",
            "password": "password123",
        })
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()

    def test_register_duplicate_email(self, client, test_user):
        response = client.post("/register", json={
            "username": "otheruser",
            "email": "test@example.com",
            "password": "password123",
        })
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()

    def test_register_short_password(self, client):
        response = client.post("/register", json={
            "username": "user",
            "email": "u@example.com",
            "password": "123",
        })
        assert response.status_code == 422  # Validation error

    def test_register_invalid_email(self, client):
        response = client.post("/register", json={
            "username": "user",
            "email": "not-an-email",
            "password": "password123",
        })
        assert response.status_code == 422


class TestLogin:
    def test_login_success(self, client, test_user):
        response = client.post("/login", json=test_user)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client, test_user):
        response = client.post("/login", json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "wrongpassword",
        })
        assert response.status_code == 401

    def test_login_nonexistent_user(self, client):
        response = client.post("/login", json={
            "username": "nobody",
            "email": "nobody@example.com",
            "password": "password123",
        })
        assert response.status_code == 401
