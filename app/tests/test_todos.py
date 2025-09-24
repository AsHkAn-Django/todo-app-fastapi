

def test_create_todo(client):
    response = client.post("/todo/", json={
        "title": "Test Todo",
        "description": "Testing create",
        "completed": False
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Todo"
    assert data["completed"] is False


def test_list_todos_pagination(client):
    # create multiple todos and assert creation
    for i in range(12):
        resp = client.post("/todo/", json={
            "title": f"Todo {i}",
            "description": "desc",
            "completed": False
        })
        assert resp.status_code == 201

    # First page
    r1 = client.get("/todo/?skip=0&limit=5")
    assert r1.status_code == 200
    data1 = r1.json()
    assert data1["total"] == 12
    assert data1["skip"] == 0
    assert data1["limit"] == 5
    assert isinstance(data1["items"], list)
    assert len(data1["items"]) == 5

    # Second page
    r2 = client.get("/todo/?skip=5&limit=5")
    assert r2.status_code == 200
    data2 = r2.json()
    assert len(data2["items"]) == 5


def test_get_single_todo(client):
    r = client.post("/todo/", json={
        "title": "Test Todo",
        "description": "Testing create",
        "completed": False
    })
    response = client.get("/todo/1/")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1


def test_update_todo(client):
    r = client.post("/todo/", json={
        "title": "Test Todo",
        "description": "Testing create",
        "completed": False
    })

    response = client.put("/todo/1", json={"title": "Updated Todo"})
    assert response.status_code == 200
    data = response.json()
    assert data['title'] == "Updated Todo"


def test_delete_todo(client):
    r = client.post("/todo/", json={
        "title": "Test Todo",
        "description": "Testing create",
        "completed": False
    })

    response = client.delete("/todo/1")
    assert response.status_code == 204

    # Confirm deletion
    response = client.get("/todo/1")
    assert response.status_code == 404