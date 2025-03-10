"""Bypass bot-detection to view SocialBlade ranks for YouTube"""
from seleniumbase import SB

import requests
import csv
import os

def upload_csv(api_key, file_path, file_name, parent_folder_id=None):
    """Uploads a CSV file to Google Drive using an API key (less recommended)."""
    url = f"https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&key={api_key}" #Added key to url
    metadata = {
        "name": file_name,
        "mimeType": "text/csv"
    }
    if parent_folder_id:
        metadata["parents"] = [parent_folder_id]
    files = {
        "metadata": (None, str(metadata), "application/json; charset=UTF-8"),
        "file": (file_name, open(file_path, "rb"), "text/csv"),
    }
    response = requests.post(url, files=files) #Removed authorization header

    if response.status_code == 200:
        print("CSV file uploaded successfully.")
    else:
        print(f"Error uploading CSV: {response.status_code}, {response.text}")


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

    csv_file_path = "my_data.csv"
    print("writing csv")
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
    
        # Write the header row (keys of the dictionary).
        header = [name, link, subscribers, video_views, rankings] #list(data_dict.keys())
        writer.writerow(header)
    
        # Write the data row (values of the dictionary).
        values = ['name', 'link', 'subscribers', 'video_views', 'rankings'] # list(data_dict.values())
        writer.writerow(values)
    
    api_key = GSHEETS_API_KEY
    csv_file_name = "my_uploaded_data.csv"
    parent_folder_id = "1h45IQ7HZrr-HQf6hCmLt88MGlOKLurfc" # Optional
    print("sending csv")
    upload_csv(api_key, csv_file_path, csv_file_name, parent_folder_id)
    print("finished!")
    
    for i in range(17):
        sb.cdp.scroll_down(6)
        sb.sleep(0.1)
    sb.sleep(2)
