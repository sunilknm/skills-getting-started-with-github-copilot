# AI Agent Instructions for Mergington High School Activities API

## Project Overview
This is a FastAPI-based web application for managing high school extracurricular activities. It consists of a Python backend API (`src/app.py`) and a vanilla JavaScript frontend (`src/static/`).

## Key Architecture Points
- **Backend**: Single FastAPI application in `src/app.py` with in-memory data storage
- **Frontend**: Static HTML/CSS/JS served from `src/static/` directory
- **Data Model**: Activities stored in dictionary with activity names as keys
  ```python
  activities = {
    "activity_name": {
      "description": str,
      "schedule": str,
      "max_participants": int,
      "participants": List[str]  # Student emails
    }
  }
  ```

## Development Workflow
1. Install dependencies:
   ```bash
   pip install fastapi uvicorn
   ```
2. Run server (from src directory):
   ```bash
   python app.py
   ```
3. Access:
   - Web UI: http://localhost:8000
   - API docs: http://localhost:8000/docs

## Project Conventions
- Student identifiers are email addresses ending in `@mergington.edu`
- Activity names are used as unique identifiers (no separate IDs)
- All data is transient (in-memory only, resets on server restart)
- Frontend uses vanilla JS without build tools

## Common Operations
1. Adding new activities:
   - Add to `activities` dictionary in `src/app.py`
   - Follow existing structure with required fields
2. Frontend changes:
   - Update HTML in `src/static/index.html`
   - Styles in `src/static/styles.css`
   - JavaScript in `src/static/app.js`

## Testing
- Project uses pytest (see `pytest.ini`)
- Add tests to `tests/` directory following pytest conventions

## Integration Points
1. Frontend-Backend Communication:
   - GET `/activities` - List all activities
   - POST `/activities/{activity_name}/signup?email=student@mergington.edu` - Sign up for activity

The project prioritizes simplicity and educational use over production-level concerns like persistence or authentication.