"""Bypass bot-detection to view SocialBlade ranks for YouTube"""
from seleniumbase import SB

import gspread
from google.oauth2.service_account import Credentials
import os
import tempfile
import json

def append_row_to_sheet_from_secret(spreadsheet_id, sheet_name, row_data, secret_name='GOOGLE_SERVICE_ACCOUNT_JSON'):
    """
    Appends a row to a Google Sheet using credentials from a GitHub secret.
    """
    try:
        # Get the JSON content from the GitHub secret.
        service_account_json_content = os.environ.get(secret_name)
        if not service_account_json_content:
            raise ValueError(f"GitHub secret '{secret_name}' not found.")

        # Create a temporary file to store the JSON content.
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.json') as temp_file:
            temp_file.write(service_account_json_content)
            temp_file_path = temp_file.name

        # Authenticate with Google Sheets API.
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_file(temp_file_path, scopes=scope)
        client = gspread.authorize(creds)

        # Open the Google Sheet and worksheet.
        sheet = client.open_by_key(spreadsheet_id)
        worksheet = sheet.worksheet(sheet_name)

        # Append the row to the worksheet.
        worksheet.append_row(row_data)

        print(f"Row appended successfully to '{sheet_name}' in spreadsheet '{spreadsheet_id}'.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Clean up the temporary file.
        if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
            os.remove(temp_file_path)



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

    spreadsheet_id = '1HShysq6qscXxQJHmf9uY3U_wKI1qgmuD54qw9EqXRsE'
    sheet_name = 'Sheet1'
    row_to_append = [name, link, subscribers, video_views, rankings]
    print("calling the append_row_func")
    append_row_to_sheet_from_secret(spreadsheet_id, sheet_name, row_to_append)
    print("append func finished")
    
    for i in range(17):
        sb.cdp.scroll_down(6)
        sb.sleep(0.1)
    sb.sleep(2)
