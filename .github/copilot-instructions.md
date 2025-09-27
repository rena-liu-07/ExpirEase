# ExpirEase AI Coding Agent Instructions

## Project Overview
ExpirEase is a cross-platform food management app built with Expo (React Native) for the frontend and Python (Flask) for backend services. It uses AI (Google Gemini) for food recognition and recipe generation, and manages food data in a local SQLite database.

## Architecture & Data Flow
- **Frontend (Expo/React Native):**
  - Located in the `app/` directory, uses file-based routing.
  - Communicates with backend via HTTP endpoints (see `server.py`).
- **Backend (Python/Flask):**
  - Main entry: `server.py` exposes `/photo_scanner` and `/recipe_maker` endpoints.
  - AI logic in `photo_scanner.py` (food recognition) and `recipe_maker.py` (recipe generation).
  - Food data managed in `food_data.py` (SQLite DB: `foodapp.db`).
  - Shelf life estimation via web scraping in `shelf_life_api.py`.

## Developer Workflows
- **Start Frontend:**
  - `npm install` then `npx expo start` (see `README.md`).
- **Start Backend:**
  - Run `python server.py` (Flask app, port 8080).
- **Linting:**
  - `npm run lint` for frontend code.
- **Reset Project:**
  - `npm run reset-project` to clear starter code (see `README.md`).

## Key Patterns & Conventions
- **AI Integration:**
  - Google Gemini API key loaded from `.env` (see `photo_scanner.py`, `recipe_maker.py`).
  - Image analysis and recipe prompts are structured for Gemini's generative model.
- **Database Usage:**
  - All food data is stored in `foodapp.db` via `food_data.py` functions.
  - Catalog and sample data are loaded on startup; tables are cleared and repopulated each run.
- **Backend Endpoints:**
  - `/photo_scanner`: POST with `paths` (image file paths), returns detected items and expiration info.
  - `/recipe_maker`: POST with `paths` and `size`, returns recipes using detected food items.
- **Shelf Life Estimation:**
  - Uses StillTasty.com scraping (`shelf_life_api.py`) to estimate expiration if not labeled.
- **Frontend Routing:**
  - All screens/components are in `app/` and `app/(tabs)/` using Expo Router conventions.

## Integration Points
- **Image Files:**
  - Images for scanning are in `pictures/`.
- **Environment Variables:**
  - `.env` required for Gemini API key.
- **External APIs:**
  - Google Gemini (AI), StillTasty (web scraping).

## Examples
- To add a new food item, use `add_food(name, expire_days, nutrition)` in `food_data.py`.
- To analyze an image, call `analyze_image(image_path)` in `photo_scanner.py`.
- To estimate shelf life, use `estimate_expiration(item)` in `shelf_life_api.py`.

## Tips for AI Agents
- Always check for `.env` and required API keys before running AI features.
- Backend tables are cleared and repopulated on each run—avoid relying on persistent DB state.
- Use the provided endpoints and functions for cross-component communication.
- Reference `README.md` for setup and workflow commands.

---

Please review and suggest any additions or clarifications for your team's workflows or conventions.