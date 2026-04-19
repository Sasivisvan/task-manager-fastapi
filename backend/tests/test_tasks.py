class TestCreateTask:
    def test_create_task(self, client, auth_headers):
        response = client.post("/tasks/", json={
            "title": "Test Task",
            "description": "A test task",
        }, headers=auth_headers)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Task"
        assert data["completed"] is False

    def test_create_task_no_auth(self, client):
        response = client.post("/tasks/", json={"title": "Test"})
        assert response.status_code == 401

    def test_create_task_no_title(self, client, auth_headers):
        response = client.post("/tasks/", json={
            "description": "Missing title",
        }, headers=auth_headers)
        assert response.status_code == 422


class TestGetTasks:
    def test_get_tasks_empty(self, client, auth_headers):
        response = client.get("/tasks/", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["tasks"] == []
        assert data["total"] == 0

    def test_get_tasks_with_data(self, client, auth_headers):
        # Create 3 tasks
        for i in range(3):
            client.post("/tasks/", json={"title": f"Task {i}"}, headers=auth_headers)

        response = client.get("/tasks/", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 3
        assert len(data["tasks"]) == 3

    def test_get_tasks_pagination(self, client, auth_headers):
        for i in range(5):
            client.post("/tasks/", json={"title": f"Task {i}"}, headers=auth_headers)

        response = client.get("/tasks/?skip=0&limit=2", headers=auth_headers)
        data = response.json()
        assert len(data["tasks"]) == 2
        assert data["total"] == 5

    def test_filter_completed(self, client, auth_headers):
        # Create and complete a task
        res = client.post("/tasks/", json={"title": "Done"}, headers=auth_headers)
        task_id = res.json()["id"]
        client.put(f"/tasks/{task_id}", json={"completed": True}, headers=auth_headers)

        # Create an active task
        client.post("/tasks/", json={"title": "Active"}, headers=auth_headers)

        # Filter completed
        response = client.get("/tasks/?completed=true", headers=auth_headers)
        data = response.json()
        assert data["total"] == 1
        assert data["tasks"][0]["completed"] is True

        # Filter active
        response = client.get("/tasks/?completed=false", headers=auth_headers)
        data = response.json()
        assert data["total"] == 1
        assert data["tasks"][0]["completed"] is False


class TestGetTask:
    def test_get_task_by_id(self, client, auth_headers):
        res = client.post("/tasks/", json={"title": "My Task"}, headers=auth_headers)
        task_id = res.json()["id"]

        response = client.get(f"/tasks/{task_id}", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["title"] == "My Task"

    def test_get_nonexistent_task(self, client, auth_headers):
        response = client.get("/tasks/99999", headers=auth_headers)
        assert response.status_code == 404


class TestUpdateTask:
    def test_mark_completed(self, client, auth_headers):
        res = client.post("/tasks/", json={"title": "Do it"}, headers=auth_headers)
        task_id = res.json()["id"]

        response = client.put(f"/tasks/{task_id}", json={"completed": True}, headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["completed"] is True

    def test_update_title(self, client, auth_headers):
        res = client.post("/tasks/", json={"title": "Old"}, headers=auth_headers)
        task_id = res.json()["id"]

        response = client.put(f"/tasks/{task_id}", json={"title": "New"}, headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["title"] == "New"

    def test_update_nonexistent(self, client, auth_headers):
        response = client.put("/tasks/99999", json={"completed": True}, headers=auth_headers)
        assert response.status_code == 404


class TestDeleteTask:
    def test_delete_task(self, client, auth_headers):
        res = client.post("/tasks/", json={"title": "Delete me"}, headers=auth_headers)
        task_id = res.json()["id"]

        response = client.delete(f"/tasks/{task_id}", headers=auth_headers)
        assert response.status_code == 200

        # Verify it's gone
        response = client.get(f"/tasks/{task_id}", headers=auth_headers)
        assert response.status_code == 404

    def test_delete_nonexistent(self, client, auth_headers):
        response = client.delete("/tasks/99999", headers=auth_headers)
        assert response.status_code == 404


class TestTaskOwnership:
    def test_cannot_access_other_users_tasks(self, client):
        """A user should not be able to see another user's tasks."""
        # Create user A
        client.post("/register", json={
            "username": "userA",
            "email": "a@example.com",
            "password": "password123",
        })
        res = client.post("/login", json={
            "username": "userA",
            "email": "a@example.com",
            "password": "password123",
        })
        headers_a = {"Authorization": f"Bearer {res.json()['access_token']}"}

        # User A creates a task
        res = client.post("/tasks/", json={"title": "A's task"}, headers=headers_a)
        task_id = res.json()["id"]

        # Create user B
        client.post("/register", json={
            "username": "userB",
            "email": "b@example.com",
            "password": "password123",
        })
        res = client.post("/login", json={
            "username": "userB",
            "email": "b@example.com",
            "password": "password123",
        })
        headers_b = {"Authorization": f"Bearer {res.json()['access_token']}"}

        # User B tries to access user A's task → 404
        response = client.get(f"/tasks/{task_id}", headers=headers_b)
        assert response.status_code == 404

        # User B's task list is empty
        response = client.get("/tasks/", headers=headers_b)
        assert response.json()["total"] == 0
