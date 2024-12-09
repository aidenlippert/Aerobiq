import React from 'react';
import { render, screen } from '@testing-library/react';
import ExerciseTracker from '../../src/components/ExerciseTracker';

test('renders Exercise Tracker heading', () => {
  render(<ExerciseTracker />);
  const headingElement = screen.getByText(/Exercise Tracker/i);
  expect(headingElement).toBeInTheDocument();
});