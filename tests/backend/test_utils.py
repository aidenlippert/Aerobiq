from src.app.utils.pose_utils import calculate_angles, normalize_keypoints

def test_calculate_angles():
    keypoints = {
        "left_shoulder": [1, 2],
        "left_elbow": [3, 4],
        "left_wrist": [5, 6],
        "right_shoulder": [7, 8],
        "right_elbow": [9, 10],
        "right_wrist": [11, 12],
    }
    angles = calculate_angles(keypoints)
    assert "left_elbow" in angles
    assert "right_elbow" in angles

def test_normalize_keypoints():
    keypoints = {
        "left_hip": [1, 2],
        "right_hip": [3, 4],
        "left_knee": [5, 6]
    }
    normalized = normalize_keypoints(keypoints)
    assert "left_hip" in normalized
    assert "right_hip" in normalized
    assert "left_knee" in normalized