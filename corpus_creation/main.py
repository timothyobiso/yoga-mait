# Author Justin Lewman
from Scraper import Scraper
import json

if __name__ == '__main__':
    # input the url to scrape, https://pocketyoga.com/pose/ is the url for the main page of pocket yoga
    s = Scraper('https://pocketyoga.com/pose/')
    s.full_scrape()
    #writes the file from the scraper object
    with open("yoga_pose_data.json", "w") as outfile:
        json.dump(s.poses, outfile)
