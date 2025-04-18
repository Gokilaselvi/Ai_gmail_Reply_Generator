# AI Email Assistant Web App

## Features
- Fetch recent Gmail messages using Gmail API.
- Display each email with a "Reply with AI" button.
- Generate professional AI replies using Google Gemini Pro API.
- Optional: Save AI-generated replies in a local SQLite database.
- Simple and clean Flask-based web interface.

## Tech Stack
- **Frontend**: HTML, CSS (Bootstrap)
- **Backend**: Python, Flask
- **AI Integration**: Google Gemini Pro API
- **Google Services**: Gmail API (OAuth 2.0)
- **Database (Optional)**: SQLite

## Requirements
- Python 3.8 or above
- Google Cloud Project
- Gmail API enabled
- OAuth 2.0 credentials (client ID and secret)
- Gemini API Key (Generative Language API)

## Setup Instructions

### Step 1: Install Dependencies
First, make sure you have `pip` installed. Then, run the following command to install the required Python packages:

```bash
pip install -r requirements.txt
