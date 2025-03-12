from seleniumbase import SB
from selenium.webdriver.common.by import By

import json


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


with SB(uc=False, headless=True, demo=True, incognito=True, maximize=True, block_images=True, ad_block_on=True, timeout_multiplier=2) as sb:
    starturl = "https://www.flashscore.com/tennis"
    sb.open(starturl)
    sb.click("#onetrust-reject-all-handler")
    # sb.uc_gui_press_keys("\t ")
    # sb.reconnect(3)
    # print(sb.get_current_url())
    # sb.assert_text("ATP - Singles", "h1")
    sb.click("span:contains('ATP - Singles')")
    
    # get box
    box = {}
    cup_fin_list = []
    sb.wait(3)
    sb.scroll_to_bottom()
    sb.scroll_into_view("a.lmc__templateHref")
    for el in sb.find_elements("a.lmc__templateHref"):
         box.update({el.get_attribute("href") : {}})
        #  print(box)
    for cup in box.keys():
        if cup in cup_fin_list:
            continue
        # ensure the box is opened
        try:
            sb.find_element("span:contains('Acapulco')") # ("span.lmc__template:nth-child(202) > a:nth-child(1)"): ##### not sure it returns bool
        except:
            sb.click("span:contains('ATP - Singles')")
            sb.wait(3)
            sb.scroll_to_bottom()
        cup_slice = cup[ cup.find("/tennis/atp-singles/" ) ::]
        print(cup_slice)
        sb.scroll_into_view('a.lmc__templateHref[href*="' + cup_slice + '"]')
        sb.find_element('a.lmc__templateHref[href*="' + cup_slice + '"]').click()
        sb.wait(3)
        # click "archive"
        sb.scroll_into_view("div.tabs__group a:contains('Archive')")
        sb.wait(2)
        sb.save_screenshot("1.png")
        sb.find_element("div.tabs__group a:contains('Archive')").click()
        sb.wait_for_element("#tournament-page-archiv")
    #     get present-2022 box2
        box2temp = sb.find_elements("div.archive__season a.archive__text.archive__text--clickable")
        
        box2 = []
        try:
            if not box2temp[0].text[-4::].isdigit():
                box2=[box2temp[0]] #.text]
        except: pass
        for el in box2temp:
            if any (year in el.text for year in ["2022", "2023", "2024", "2025"]):
                box2.append(el) #.get_attribute("href"))
                # sb.activate_messenger()
                # sb.post_message(f"{el.text}  APPENDED", duration=3, pause=True, style="info")
            
        # print(box2)
        finlist2 = []
        for el in box2:
            if el in finlist2:
                continue
            el.location_once_scrolled_into_view
            # sb.activate_messenger()
            # sb.post_message("GOING TO CLICK EL TO MATCHES", duration=3, pause=True, style="info")
            sb.wait(3)
            el.click()
            sb.wait(3)
            
            # click "show more matches" if exists
            # while sb.is_element_present("a:contains('Show more matches')"):
            #     smm = sb.find_element("a:contains('Show more matches')")
            #     smm.location_once_scrolled_into_view
            #     smm.click()
            #     sb.wait(3)
            #     print("show more matches done")
            sb.scroll_into_view("div.tabs__group a:contains('Results')")
            sb.find_element("div.tabs__group a:contains('Results')").click()
                
            # get matches
            box3 = sb.find_elements("a.eventRowLink") 
                
            data2send = {}
            finlist3 = []
            for match in box3:
                if match in finlist3:
                    continue
                sb.wait(3)
                match.location_once_scrolled_into_view
                sb.wait(1)
                match.click()
                sb.wait(3)
                # get match_id
                sb.switch_to_newest_window()
                match_id = sb.get_current_url().split("/")[4]
                # get topgeneral data if exists
                try:
                    data2send.update({
                        "CUP | tournamentHeader__country"
                        : sb.find_element("span.tournamentHeader__country").text,
                    })
                except: pass
                try:
                    data2send.update({
                        "TIME | duelParticipant__startTime"
                        : sb.find_element("div.duelParticipant__startTime").text,
                    })
                except: pass
                try:
                    data2send.update({
                        "SCORE | detailScore__matchInfo"
                        : sb.find_element("div.detailScore__matchInfo").text,
                    })
                except: pass
                try:
                    data2send.update({
                        "PLAYER HOME | duelParticipant__home"
                        : sb.find_element("div.duelParticipant__home a.participant__participantName").text,
                    })
                except: pass
                try:
                    data2send.update({
                        "PLAYER AWAY | duelParticipant__away"
                        : sb.find_element("div.duelParticipant__away a.participant__participantName").text,
                    })
                except: pass
                
                # get matchsummary data if exists
                try:
                    data2send.update({
                        "TOTAL SCORE HOME | smh__home smh__part--current" 
                        : sb.find_element("div.smh__home.smh__part--current").text,
                    })
                except: pass
                try:
                    data2send.update({
                        "S1 | smh__part  smh__home smh__part--1" 
                        : sb.find_element("div.smh__home.smh__part--1").text,
                    })
                except: pass
                try:
                    data2send.update({
                        "S2 | smh__part  smh__home smh__part--2" 
                        : sb.find_element("div.smh__home.smh__part--2").text,
                    })
                except: pass
                try:
                    data2send.update({
                        "S3 | smh__part  smh__home smh__part--3" 
                        : sb.find_element("div.smh__home.smh__part--3").text,
                    })
                except: pass
                try:
                    data2send.update({
                        "S4 | smh__part  smh__home smh__part--4" 
                        : sb.find_element("div.smh__home.smh__part--4").text,
                    })
                except: pass
                try:
                    data2send.update({
                        "S5 | smh__part  smh__home smh__part--5" 
                        : sb.find_element("div.smh__home.smh__part--5").text,
                    })
                except: pass                                                                
                try:
                    data2send.update({
                        "TOTAL SCORE away | smh__away smh__part--current" 
                        : sb.find_element("div.smh__away.smh__part--current").text,
                    })
                except: pass
                try:
                    data2send.update({
                        "S1 | smh__part  smh__away smh__part--1" 
                        : sb.find_element("div.smh__away.smh__part--1").text,
                    })
                except: pass
                try:
                    data2send.update({
                        "S2 | smh__part  smh__away smh__part--2" 
                        : sb.find_element("div.smh__away.smh__part--2").text,
                    })
                except: pass
                try:
                    data2send.update({
                        "S3 | smh__part  smh__away smh__part--3" 
                        : sb.find_element("div.smh__away.smh__part--3").text,
                    })
                except: pass
                try:
                    data2send.update({
                        "S4 | smh__part  smh__away smh__part--4" 
                        : sb.find_element("div.smh__away.smh__part--4").text,
                    })
                except: pass
                try:
                    data2send.update({
                        "S5 | smh__part  smh__away smh__part--5" 
                        : sb.find_element("div.smh__away.smh__part--5").text,
                    })
                except: pass
                try:
                    data2send.update({
                        "TOTAL TIME | smh__time--overall" 
                        : sb.find_element("div.smh__time--overall").text,
                    })
                except: pass        
                try:
                    data2send.update({
                        "S1 TIME | smh__time--0" 
                        : sb.find_element("div.smh__time--0").text,
                    })
                except: pass
                try:
                    data2send.update({
                        "S2 TIME | smh__time--1" 
                        : sb.find_element("div.smh__time--1").text,
                    })
                except: pass
                try:
                    data2send.update({
                        "S3 TIME | smh__time--2" 
                        : sb.find_element("div.smh__time--2").text,
                    })
                except: pass
                try:
                    data2send.update({
                        "S4 TIME | smh__time--3" 
                        : sb.find_element("div.smh__time--3").text,
                    })
                except: pass
                try:
                    data2send.update({
                        "S5 TIME | smh__time--4" 
                        : sb.find_element("div.smh__time--4").text,
                    })
                except: pass                        
                # click "stats"
                try:
                  sb.find_element("button:contains('Stats')").click()
                except: pass
                sb.wait(3)
                
                statdata = {}
                # get statdata whatever it is    # section div.section:nth-child(9) 
                # try:                             # Aces div.section:nth-child(9) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2)
                #                            #Total games div.section:nth-child(12) > div:nth-child(4) > div:nth-child(1) > div:nth-child(2)
                #     sections = sb.find_elements("div.section")
                #     sections = sections[8::]
                #     for section in sections:
                #         rows = section.find_elements("div")
                #         rows = rows[1::]
                #         for row in rows:
                #             txtrow = row.find_element("div:nth-child(1)")
                #             statdata.update({
                #                 txtrow.find_element("div:nth-child(2)").text + " HOME |"
                #                 : txtrow.find_element("div:nth-child(1)").text,
                #                 txtrow.find_element("div:nth-child(2)").text + " AWAY |"
                #                 : txtrow.find_element("div:nth-child(3)").text,
                                
                #             })                    
                # except: pass
                
                # rows = sb.find_elements('xpath', '//div[starts-with(@class, "wcl-row")]')
                # for row in rows:
                    
                #     category = row.find_element('xpath', '//div[starts-with(@class, "wcl-category")]')
                #     values = category.find_elements('xpath', '//div[starts-with(@class, "wcl-value")]')
                #     title = category.find_element('xpath', '//div[starts-with(@class, "wcl-category")]')
                #     # print(f"{title.text}: {values[0].text}, {values[1].text}")
                #     statdata.update({
                #         f"{title.text} HOME"
                #         : values[0].text,
                #         f"{title.text} AWAY"
                #         : values[1].text,
                #     })
                
                statdata ={}
                rows = sb.find_elements('[class^="wcl-row"]')
                print(len(rows))
                for row in rows:
                    # print(row.text)
                    category = row.find_element(By.CSS_SELECTOR, '[class^="wcl-category"]')
                    values = category.find_elements(By.CSS_SELECTOR, '[class^="wcl-value"]')
                    title = category.find_element(By.CSS_SELECTOR, '[class^="wcl-category"]')

                    if len(values) >= 2:
                        print(f"{title.text}: {values[0].text}, {values[1].text}")
                    else:
                        print(f"Warning: Expected at least 2 values, found {len(values)} for title: {title.text}")
                    statdata.update({
                        f"{title.text} HOME"
                        : values[0].text,
                        f"{title.text} AWAY"
                        : values[1].text,
                    })
                    
                # print(json.dumps(statdata, indent=4))

                
                # print-send all 4 data
                # print(match_id, topgeneral, matchsummary, statdata) # TODO
                data2send.update(statdata)
                data2send.update({"match_id" : match_id})
                file_path = match_id + ".json"
                # with open(file_path, "w") as json_file:
                #     json.dump(data2send, json_file, indent=4)
                webhook_url = os.environ["WEBHOOK_URL"]
                # data_to_send = {
                #     "name": name,
                #     "link": link,
                #     "subscribers" : subscribers,
                #     "video_views" : video_views,
                #     "rankings" : rankings
                # }
                
                response_data = send_webhook_data(webhook_url, data2send) #data_to_send)
                
                if response_data:
                  print("Returned JSON data:")
                  print(response_data)                
                # close wind2
                sb.driver.close()
                sb.switch_to_default_window()
                sb.wait(3)
                
                # add match to finlist3
                finlist3.append(match)
            sb.go_back()
            sb.wait(1)
            sb.go_back()
            sb.wait(3)
            finlist2.append(el)
        cup_fin_list.append(cup)
        #     for match in box3 if match is not in finlist3:
        #         click match
        #         switch to wind2
        #         get match_id
        #         get topgeneral data if exists
        #         get matchsummary data if exists
        #         click "stats"
        #         get statdata whatever it is
        #         close wind2
        #         print-send all 4 data
        #         switch to wind1
        #         add match to finlist3
        #         sb.go_back()
        #         sb.wait(3)
        #     add year to finlist2
        #     click archive
        # add cup to finlist
            
    
    
