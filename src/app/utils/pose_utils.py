import numpy as np
import mediapipe as mp

mp_pose = mp.solutions.pose

def get_pose_keypoints(image):
    """
    Extract pose keypoints using MediaPipe BlazePose.

    Args:
        image (numpy.ndarray): Input image.

    Returns:
        dict: Normalized pose keypoints.
    """
    with mp_pose.Pose(static_image_mode=True, model_complexity=2) as pose:
        results = pose.process(image)
        if results.pose_landmarks:
            keypoints = {}
            for idx, landmark in enumerate(results.pose_landmarks.landmark):
                keypoints[mp_pose.PoseLandmark(idx).name] = [landmark.x, landmark.y, landmark.z]
            normalized_keypoints = normalize_keypoints(keypoints)
            return normalized_keypoints
        else:
            return {}

def calculate_angles(keypoints):
    """
    Calculate angles between joints.

    Args:
        keypoints (dict): Normalized keypoints.

    Returns:
        dict: Angles at specific joints.
    """
    angles = {}
    # Joints needed for squat analysis
    joints = {
        'left_knee': ('LEFT_HIP', 'LEFT_KNEE', 'LEFT_ANKLE'),
        'right_knee': ('RIGHT_HIP', 'RIGHT_KNEE', 'RIGHT_ANKLE'),
        'hip': ('LEFT_SHOULDER', 'LEFT_HIP', 'LEFT_KNEE'),
    }

    for angle_name, (a, b, c) in joints.items():
        if a in keypoints and b in keypoints and c in keypoints:
            angles[angle_name] = angle_between_points(
                keypoints[a][:2],
                keypoints[b][:2],
                keypoints[c][:2]
            )

    return angles

def angle_between_points(a, b, c):
    """
    Calculate the angle at point b formed by points a, b, and c.

    Args:
        a (list): Coordinates of point a.
        b (list): Coordinates of point b.
        c (list): Coordinates of point c.

    Returns:
        float: Angle in degrees.
    """
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.degrees(np.arccos(np.clip(cosine_angle, -1.0, 1.0)))

    return angle

def normalize_keypoints(keypoints):
    """
    Normalize keypoints based on the center of the hips.

    Args:
        keypoints (dict): Original keypoints.

    Returns:
        dict: Normalized keypoints.
    """
    left_hip = keypoints.get('LEFT_HIP')
    right_hip = keypoints.get('RIGHT_HIP')

    if left_hip and right_hip:
        hip_center = np.mean([left_hip, right_hip], axis=0)
    else:
        hip_center = np.zeros(3)

    normalized_keypoints = {}
    for key, value in keypoints.items():
        normalized_value = (np.array(value) - hip_center).tolist()
        normalized_keypoints[key] = normalized_value

    return normalized_keypoints

def detect_squat_correctness(angles):
    """
    Determine if the squat is performed correctly based on angle thresholds.

    Args:
        angles (dict): Dictionary of joint angles.

    Returns:
        bool: True if squat is correct, False otherwise.
        dict: Details about any issues detected.
    """
    feedback = {}
    correct_squat = True

    # Commonly accepted angle thresholds for squats
    knee_angle_threshold = 90  # Degrees
    hip_angle_threshold = 90   # Degrees

    # Check knee angles
    for side in ['left_knee', 'right_knee']:
        knee_angle = angles.get(side, 180)
        if knee_angle > knee_angle_threshold:
            feedback[f"{side}_issue"] = f"{side.replace('_', ' ').capitalize()} angle is too open: {knee_angle:.1f}°."
            correct_squat = False

    # Check hip angle
    hip_angle = angles.get('hip', 180)
    if hip_angle < hip_angle_threshold:
        feedback['hip_issue'] = f"Hip angle is too closed: {hip_angle:.1f}°."
        correct_squat = False

    return correct_squat, feedback