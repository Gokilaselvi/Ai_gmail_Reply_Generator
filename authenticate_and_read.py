import os
import pickle
import urllib.parse
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from flask import Flask, request, jsonify

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Authenticate Gmail
def authenticate_gmail():
    creds = None

    # Load token if it exists
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If no valid token, get new one from user
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # ⚠️ Replace 'path/to/credentials.json' with your own client secret file
            flow = InstalledAppFlow.from_client_secrets_file(
                'path/to/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save token for future use
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('gmail', 'v1', credentials=creds)

# Fetch and generate HTML
def fetch_and_generate_html():
    service = authenticate_gmail()
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=1).execute()
    messages = results.get('messages', [])

    if not messages:
        print("No emails found.")
        return

    message = service.users().messages().get(userId='me', id=messages[0]['id']).execute()

    email_info = {'subject': '(No Subject)', 'from': '(Unknown Sender)', 'snippet': ''}
    for header in message['payload']['headers']:
        if header['name'] == 'Subject':
            email_info['subject'] = header['value']
        elif header['name'] == 'From':
            email_info['from'] = header['value']
    email_info['snippet'] = message.get('snippet', '')

    search_query = urllib.parse.quote(email_info['subject'] or email_info['snippet'])
    gmail_url = f"https://mail.google.com/mail/u/0/#search/{search_query}"

    # HTML content
    html_content = f"""
    <html>
    <head>
        <title>Latest Email</title>
        <style>
            body {{ font-family: Arial; margin: 20px; background-color: #f0f0f0; }}
            .email-box {{ background: #fff; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px #ccc; }}
            .btn {{
                margin-top: 20px;
                padding: 10px 20px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }}
        </style>
    </head>
    <body>
        <div class="email-box">
            <h2>{email_info['subject']}</h2>
            <p><strong>From:</strong> {email_info['from']}</p>
            <p>{email_info['snippet']}</p>
            <a href="{gmail_url}" target="_blank" class="btn">Open in Gmail</a>
            <br><br>
            <button class="btn" onclick="replyWithAI()">Reply with AI</button>
            <div id="ai-reply" style="margin-top:20px;"></div>
        </div>
        <script>
            function replyWithAI() {{
                fetch('/generate_reply', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ email_snippet: `{email_info['snippet']}` }})
                }})
                .then(response => response.json())
                .then(data => {{
                    document.getElementById('ai-reply').innerText = data.reply;
                }})
                .catch(err => {{
                    document.getElementById('ai-reply').innerText = 'Error: ' + err;
                }});
            }}
        </script>
    </body>
    </html>
    """

    with open("latest_email.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("✅ latest_email.html generated.")

# Run this script to generate the HTML
if __name__ == '__main__':
    fetch_and_generate_html()
