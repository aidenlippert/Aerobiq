import React from 'react';

const Navbar = () => {
  return (
    <nav className="bg-blue-600 p-4">
      <div className="container mx-auto flex justify-between items-center">
        <h1 className="text-white text-xl font-bold">AI Personal Trainer</h1>
        <div className="flex space-x-4">
          <a href="/" className="text-white hover:text-gray-200">
            Home
          </a>
          <a href="/exercise-tracker" className="text-white hover:text-gray-200">
            Exercise Tracker
          </a>
          <a href="/profile" className="text-white hover:text-gray-200">
            Profile
          </a>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;