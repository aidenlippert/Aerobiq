from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_analyze_pose():
    payload = {
        "keypoints": {
            "left_shoulder": [100, 200],
            "left_elbow": [150, 250],
            "left_wrist": [200, 200],
            "right_shoulder": [300, 200],
            "right_elbow": [350, 250],
            "right_wrist": [400, 200],
            "left_hip": [120, 400],
            "right_hip": [280, 400],
            "left_knee": [120, 500],
            "right_knee": [280, 500],
            "left_ankle": [120, 600],
            "right_ankle": [280, 600]
        }
    }
    response = client.post("/api/analyze-pose", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "insights" in data
    assert "angles" in data["insights"]
    assert "tempo" in data["insights"]
    assert "feedback" in data
    assert isinstance(data["feedback"], list)