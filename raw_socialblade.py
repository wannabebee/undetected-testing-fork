"""Bypass bot-detection to view SocialBlade ranks for YouTube"""
from seleniumbase import SB

import requests
import json
import os

def send_webhook_data(url, data):
    """
    Sends a POST request to a webhook URL with JSON data.

    Args:
        url: The webhook URL.
        data: A Python dictionary containing the data to send.
    """
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)

        print("Webhook request successful!")
        print("Response:", response.text) #Print response content.
        return response.json() #return json content if possible.

    except requests.exceptions.RequestException as e:
        print(f"Error sending webhook request: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding json response: {e}")
        return None

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
    
    webhook_url = os.environ["WEBHOOK_URL"]
    data_to_send = {
        "name": name,
        "link": link,
        "subscribers" : subscribers,
        "video_views" : video_views,
        "rankings" : rankings
    }
    
    response_data = send_webhook_data(webhook_url, data_to_send)
    
    if response_data:
      print("Returned JSON data:")
      print(response_data)
    
    for i in range(17):
        sb.cdp.scroll_down(6)
        sb.sleep(0.1)
    sb.sleep(2)
