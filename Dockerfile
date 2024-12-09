# Stage 1: Build React frontend
FROM node:14-alpine AS frontend-build

WORKDIR /app/frontend

# Install dependencies
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install

# Build the frontend
COPY frontend/ ./
RUN npm run build

# Stage 2: Setup Python backend
FROM python:3.8-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY src/ ./src/
COPY config/ ./config/

# Copy frontend build
COPY --from=frontend-build /app/frontend/build ./frontend/build

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]