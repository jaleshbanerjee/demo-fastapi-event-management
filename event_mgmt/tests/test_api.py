def test_create_event(client):
    response = client.post("/events", json={
        "name": "Test Event",
        "location": "Mumbai",
        "start_time": "2025-06-12",
        "end_time": "2025-06-12",
        "max_capacity": 50
    })
    assert response.status_code == 200
