import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import Webcam from 'react-webcam';
import * as mpPose from '@mediapipe/pose';
import * as cam from '@mediapipe/camera_utils';
import FeedbackPanel from './FeedbackPanel';

const ExerciseTracker = () => {
  const webcamRef = useRef(null);
  const [feedback, setFeedback] = useState([]);
  
  const pose = new mpPose.Pose({
    locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/pose/${file}`,
  });
  
  const onResults = async (results) => {
    if (results.poseLandmarks) {
      const keypoints = {};
      results.poseLandmarks.forEach((landmark, idx) => {
        keypoints[mpPose.POSE_LANDMARKS[idx]] = [landmark.x, landmark.y, landmark.z];
      });
      
      try {
        // Send keypoints to backend for analysis
        const response = await axios.post('/api/analyze-pose', { keypoints });
        setFeedback(response.data.feedback);
      } catch (error) {
        console.error('Error analyzing pose:', error);
      }
    }
  };

  useEffect(() => {
    if (typeof webcamRef.current !== 'undefined' && webcamRef.current !== null) {
      pose.setOptions({
        modelComplexity: 1,
        smoothLandmarks: true,
        enableSegmentation: false,
        smoothSegmentation: false,
        minDetectionConfidence: 0.5,
        minTrackingConfidence: 0.5,
      });
      pose.onResults(onResults);
      
      const camera = new cam.Camera(webcamRef.current.video, {
        onFrame: async () => {
          await pose.send({ image: webcamRef.current.video });
        },
        width: 640,
        height: 480,
      });
      camera.start();
    }
  }, []);

  return (
    <div className="exercise-tracker">
      <h2 className="text-2xl font-bold mb-4">Exercise Tracker</h2>
      <div className="relative">
        <Webcam
          audio={false}
          ref={webcamRef}
          screenshotFormat="image/jpeg"
          className="border-2 border-gray-300 rounded"
          width={640}
          height={480}
        />
      </div>
      <FeedbackPanel feedback={feedback} />
    </div>
  );
};

export default ExerciseTracker;