"""Bypass bot-detection to view SocialBlade ranks for YouTube"""
from seleniumbase import SB

import gspread
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import json
import tempfile

def append_row_oauth_from_secret_correct(spreadsheet_id, sheet_name, row_data, secret_name='CREDENTIALS_JSON'):
    """Appends a row to a Google Sheet using OAuth 2.0 credentials from a GitHub secret."""

    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Get the JSON content directly from the GitHub secret.
            credentials_json_str = os.environ.get(secret_name)
            if not credentials_json_str:
                raise ValueError(f"GitHub secret '{secret_name}' not found.")

            # Load the JSON string into a dictionary.
            credentials_data = json.loads(credentials_json_str)

            # Create a temporary credentials file.
            with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.json') as temp_file:
                json.dump(credentials_data, temp_file)
                temp_file_path = temp_file.name

            flow = InstalledAppFlow.from_client_secrets_file(temp_file_path, SCOPES)
            creds = flow.run_local_server(port=0)

            os.remove(temp_file_path) #delete temp file.

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        client = gspread.authorize(creds)
        sheet = client.open_by_key(spreadsheet_id)
        worksheet = sheet.worksheet(sheet_name)
        worksheet.append_row(row_data)
        print(f"Row appended successfully to '{sheet_name}' in spreadsheet '{spreadsheet_id}'.")

    except Exception as e:
        print(f"An error occurred: {e}")

with SB(uc=True, test=True, ad_block=True, pls="none") as sb:
    url = "https://socialblade.com/"
    sb.activate_cdp_mode(url)
    sb.sleep(2)
    sb.uc_gui_click_captcha()
    sb.sleep(1)
    channel_name = "michaelmintz"
    sb.cdp.press_keys('input[name="query"]', channel_name)
    sb.sleep(1)
    sb.cdp.gui_click_element('form[action*="/search"] button')
    sb.sleep(2)
    if not sb.cdp.is_element_visible('a[title="%s"] h2' % channel_name):
        sb.cdp.open(
            "https://socialblade.com/youtube/channel/UCSQElO8vQmNPuTgdd83BHdw"
        )
        sb.sleep(1)
        sb.uc_gui_click_captcha()
    else:
        sb.cdp.click('a[title="%s"] h2' % channel_name)
    sb.sleep(1.5)
    sb.cdp.remove_elements("#lngtd-top-sticky")
    sb.sleep(1.5)
    name = sb.cdp.get_text("h1")
    link = sb.cdp.get_attribute("#YouTubeUserTopInfoBlockTop h4 a", "href")
    subscribers = sb.cdp.get_text("#youtube-stats-header-subs")
    video_views = sb.cdp.get_text("#youtube-stats-header-views")
    rankings = sb.cdp.get_text(
        '#socialblade-user-content [style*="border-bottom"]'
    ).replace("\xa0", "").replace("   ", " ").replace("  ", " ")
    print("********** SocialBlade Stats for %s: **********" % name)
    print(">>> (Link: %s) <<<" % link)
    print("* YouTube Subscribers: %s" % subscribers)
    print("* YouTube Video Views: %s" % video_views)
    print("********** SocialBlade Ranks: **********")
    for row in rankings.split("\n"):
        if len(row.strip()) > 8:
            print("-->  " + row.strip())

    spreadsheet_id = '1HShysq6qscXxQJHmf9uY3U_wKI1qgmuD54qw9EqXRsE' # Replace with your spreadsheet ID
    sheet_name = 'Sheet1'
    row_to_append = ['value1', 'value2', 'value3']
    append_row_oauth_from_secret_correct(spreadsheet_id, sheet_name, row_to_append)
    
    for i in range(17):
        sb.cdp.scroll_down(6)
        sb.sleep(0.1)
    sb.sleep(2)
