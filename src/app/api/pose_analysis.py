from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.app.utils.pose_utils import calculate_angles, normalize_keypoints, detect_squat_correctness
from src.app.analytics.tempo_analysis import TempoAnalyzer
from src.ai_coaching.coaching import CoachingEngine
from src.app.config.settings import settings
import base64
import cv2
import numpy as np

router = APIRouter()
tempo_analyzer = TempoAnalyzer()

class PoseData(BaseModel):
    image: str  # Base64 encoded image

@router.post("/analyze-pose")
async def analyze_pose(data: PoseData):
    try:
        # Decode image
        image_data = base64.b64decode(data.image)
        np_image = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(np_image, cv2.IMREAD_COLOR)

        # Get pose keypoints
        keypoints = get_pose_keypoints(image)

        if not keypoints:
            raise ValueError("No keypoints detected.")

        # Normalize keypoints
        normalized_keypoints = normalize_keypoints(keypoints)

        # Calculate angles
        angles = calculate_angles(normalized_keypoints)

        # Detect squat correctness
        correct_squat, squat_feedback = detect_squat_correctness(angles)

        # Analyze tempo
        knee_angle = (angles.get('left_knee', 0) + angles.get('right_knee', 0)) / 2
        tempo_results = tempo_analyzer.analyze_tempo(knee_angle)

        # Generate feedback
        coaching_engine = CoachingEngine(template_path=settings.FEEDBACK_TEMPLATE_PATH)
        feedback = coaching_engine.generate_feedback({
            "correct_squat": correct_squat,
            "squat_feedback": squat_feedback,
            "tempo_results": tempo_results
        })

        # Prepare insights
        insights = {
            "angles": angles,
            "tempo": tempo_results,
            "squat_correct": correct_squat
        }

        return {"insights": insights, "feedback": feedback}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))