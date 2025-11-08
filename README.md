# README

## Name
ExpirEase is a food management application designed to reduce food waste.

## Features
- Allows users to upload photos of food items, which are automatically detected and added to their inventory using AI.
- Allows users to manually add ingredients with custom expiration dates and categories.
- Organises and displays ingredients by expiration urgency with color-coded indicators.
- Generates AI-powered recipes based on available ingredients and serving size preferences.
- Tracks historical food data and allows users to delete items from their inventory.

## Installation

### Installing the Required Software
Node.js, Python, and Git need to be installed to run this application. If these are already installed, skip this section.

1. Install Node.js (v18 or higher) from [nodejs.org](https://nodejs.org/).
2. Install Python (v3.11 or higher) from [python.org](https://www.python.org/).
3. (Optional) Install Git from [git-scm.com](https://git-scm.com/).

### Cloning and Running ExpirEase

1. Open Terminal (macOS/Linux) or Command Prompt (Windows).
2. Clone the repository:
   ```
   git clone https://github.com/rena-liu-07/ExpirEase.git
   cd ExpirEase-4
   ```
3. Create a Python virtual environment and activate it:
   - **Windows**: `python -m venv .venv` then `.venv\Scripts\activate`
   - **macOS/Linux**: `python3 -m venv .venv` then `source .venv/bin/activate`
4. Install Python dependencies: `pip install -r requirements.txt`
5. Install Node.js dependencies: `npm install`
6. Create a Google Gemini API Key:
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey).
   - Sign in with your Google account and create an API key.
7. Create a `.env` file in the root directory and add your API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
8. Start the backend server (keep this terminal running):
   ```
   python server.py
   ```
9. Open a new terminal and start the frontend:
   ```
   npx expo start
   ```
10. Access the app:
    - **Web**: Press `w` in the Expo terminal.
    - **Mobile**: Install [Expo Go](https://expo.dev/client) and scan the QR code (ensure same Wi-Fi network).
    - **iOS Simulator** (macOS only): Press `i`.
    - **Android Emulator**: Press `a`.

## Known Bugs
- Temporary image files may occasionally fail to delete on Windows due to file locking, but this does not affect functionality.
- Metro bundler cache may require clearing (`npx expo start --clear`) if changes are not reflected immediately.

## Support
Contact the repository owner through GitHub issues if help is required.
