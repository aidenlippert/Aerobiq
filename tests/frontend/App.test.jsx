import React from 'react';
import { render, screen } from '@testing-library/react';
import App from '../../src/App';

test('renders AI Personal Trainer title', () => {
  render(<App />);
  const titleElement = screen.getByText(/AI Personal Trainer/i);
  expect(titleElement).toBeInTheDocument();
});