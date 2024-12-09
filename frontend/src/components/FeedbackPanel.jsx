import React from 'react';

const FeedbackPanel = ({ feedback }) => {
  if (!feedback || feedback.length === 0) return null;

  return (
    <div className="feedback-panel mt-4 p-4 bg-yellow-100 border border-yellow-300 rounded">
      <h3 className="text-xl font-semibold">Feedback:</h3>
      <ul className="list-disc list-inside">
        {feedback.map((item, index) => (
          <li key={index} className="text-gray-700">{item}</li>
        ))}
      </ul>
    </div>
  );
};

export default FeedbackPanel;