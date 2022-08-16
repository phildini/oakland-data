import requests
from bs4 import BeautifulSoup
import os

from xhtml2pdf import pisa


def main():

    base_api_url = "http://webapi.legistar.com/v1/oakland/"
    base_url = "http://oakland.legistar.com/"

    # Records go back to 2000, minutes only start in 2003
    years = [
        "2003",
        "2004",
        "2005",
        "2006",
        "2007",
        "2008",
        "2009",
        "2010",
        "2011",
        "2012",
        "2013",
        "2014",
        "2015",
        "2016",
        "2017",
        "2018",
        "2019",
        "2020",
        "2021",
        "2022",
    ]
    total = 0

    for year in years:
        print(f"Fetching {year}")
        event_listing_url = f"{base_api_url}events?$filter=EventDate+ge+datetime%27{year}-01-01%27+and+EventDate+lt+datetime%27{year}-12-31%27"
        list_response = list_response = requests.get(event_listing_url)
        total += len(list_response.json())
        print(f"{total} events fetched so far")

        for event in list_response.json():
            body = (
                event["EventBodyName"]
                .replace(" ", "")
                .replace("*", "")
                .replace("&", "And")
                .replace("/", "And")
                .replace("SpecialConcurrentMeetingofthe", "")
                .replace("ConcurrentMeetingofthe", "")
                .replace("Meetingofthe", "")
            )
            # print(f"ID: {event['EventId']}, Body: {body}")
            directory = f"./data/{body}"
            if not os.path.exists(directory):
                os.makedirs(directory)
            filename = event["EventDate"].split("T")[0] + ".pdf"
            filepath = f"{directory}/{filename}"
            if os.path.exists(filepath):
                continue
            page_url = event["EventInSiteURL"]
            try:
                page_response = requests.get(page_url)
            except:
                continue
            soup = BeautifulSoup(page_response.text, "html.parser")
            try:
                minutes_url = (
                    base_url
                    + soup.find(id="ctl00_ContentPlaceHolder1_hypMinutes").attrs["href"]
                )
            except:
                # print(page_url)
                continue
            try:
                minutes_response = requests.get(minutes_url, allow_redirects=True)
            except:
                print(minutes_url)
                continue
            if "pdf" in minutes_response.headers["content-type"].lower():
                print(f"Writing file {filepath}, body: {body}")
                with open(filepath, "wb") as minutes_pdf:
                    minutes_pdf.write(minutes_response.content)
            elif "html" in minutes_response.headers["content-type"].lower():
                print(f"Converting from HTML and writing file {filepath}, body: {body}")
                with open(filepath, "wb") as minutes_pdf:
                    pisa_status = pisa.CreatePDF(
                        minutes_response.content, dest=minutes_pdf
                    )
                if pisa_status.err:
                    print(f"Error converting {filepath}, body: {body}")


if __name__ == "__main__":
    main()
