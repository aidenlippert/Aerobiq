import React from 'react';
import Navbar from './components/Navbar';
import ExerciseTracker from './components/ExerciseTracker';

const App = () => {
  return (
    <div className="app-container">
      <Navbar />
      <div className="main-content p-4">
        <ExerciseTracker />
      </div>
    </div>
  );
};

export default App;