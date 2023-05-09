# Author Justin Lewman
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from utils import timer
# import json
# from urllib.request import urlopen
import requests # request img from web
import shutil # save img locally
import os.path


class Scraper:
    def __init__(self, url):
        self.base_url = url
        self.to_scrape = []
        self.poses = {}

    def test(self):
        """
        just test code, no real reason to rrun or remove it
        :return:
        """
        url = self.base_url
        print(url)
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        # Now we use the driver to render the JavaScript webpage.
        driver.get(url)
        while driver.page_source.split("title>")[1] == "Yoga Poses Dictionary | Pocket Yoga</":
            time.sleep(0.01)
        # page_source stores the HTML markup of the webpage, not the JavaScript code.
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, features='lxml')
        images = soup.find_all('img')
        for image in images:
            self.save_image(image["src"])
        print(images)

        driver.quit()

    @timer
    def full_scrape(self, base_url=None, crawl=True):
        """
        Runs a full scrape on the inputted url including getting images and all information about each pose
        :param base_url: New url to start at; will use scraper's base url if left empty
        :param crawl: boolean indicating whether to follow all unvisited pose links or not
        :return:
        """
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        if not base_url:
            base_url = self.base_url
        self.get_links(self.base_url, driver)
        for url in self.to_scrape:
            self.scrape_with_links(base_url+url, driver, crawl=crawl)
        driver.quit()
        print("Number of poses:", len(self.poses))

    def scrape(self, url):
        """
        Scrapes a url and prints results, this is mainly for testing
        :param url: url to scrape (pose urls only)
        :return:
        """
        print(url)
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        # Now we use the driver to render the JavaScript webpage.
        driver.get(url)
        time.sleep(1)
        # page_source stores the HTML markup of the webpage, not the JavaScript code.
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, features='lxml')
        title = soup.find("section", class_="poseHeading").find("h3").get_text()
        descriptions = [i.get_text() for i in soup.findAll("p", class_="text")]
        while len(descriptions) < 2:
            descriptions.append("")
        lines = soup.find("section", class_="poseDescription").find_all("h5")
        difficulty = ""
        for line in lines:
            if "Difficulty:" in line.text:
                difficulty = line.find_next("span").text
        print("Pose Title:", title)
        print("Difficulty:", difficulty)
        print("Pose Description:", descriptions[0])
        print("Pose Benefits:", descriptions[1])
        driver.quit()

    def get_links(self, url, driver):
        """
        Gets all the pose links on the webpage, used for crawling
        :param url: url to find all links on
        :param driver: a created webdriver to load the javascript of the page
        :return:
        """
        # Now we use the driver to render the JavaScript webpage.
        # We use the same driver as opening a closing a new one takes 1-10 seconds
        driver.get(url)
        time.sleep(1)
        # page_source stores the HTML markup of the webpage, not the JavaScript code.
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, features='lxml')
        urls = set()
        for link in soup.find_all('a'):
            l = link.get('href')
            if l.startswith("/pose/") and l not in self.to_scrape:
                urls.add(l.replace("/pose/", ""))
        self.to_scrape.extend(urls)

    def scrape_with_links(self, url, driver, crawl=True):
        """
        Fully scrapes a url including saving the central image to the images and storing all necessary data in self.poses
        :param url: The url to scrape
        :param driver: a created webdriver to load the javascript of the page
        :param crawl: boolean representing whether or not to crawl to all linked unvisted pose pages
        :return:
        """
        #print(url)
        # Now we use the driver to render the JavaScript webpage.
        driver.get(url)
        # Check if the javascript has been sucessfully loaded, if not, wait (DOES NOT WORK ON NON POSE PAGES!)
        while driver.page_source.split("title>")[1] == "Yoga Poses Dictionary | Pocket Yoga</":
            time.sleep(0.01)
        # page_source stores the HTML markup of the webpage, not the JavaScript code.
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, features='lxml')
        url_extension = url.split("/pose/")[1]
        title_container = soup.find("section", class_="poseHeading")
        # ignore empty pages
        if not title_container:
            return
        # finds and adds description and benefits to self.poses, "" if empty
        title = title_container.find("h3").get_text()
        descriptions = [i.get_text() for i in soup.findAll("p", class_="text")]
        while len(descriptions) < 2:
            descriptions.append("")
        self.poses[url_extension] = {"Pose Name": title, "Pose Description": descriptions[0], "Pose Benefits": descriptions[1]}
        # finds and adds pose variations to self.poses
        related_urls = set()
        section = soup.find("section", class_="poseVariations")
        if section:
            for link in section.find_all('a'):
                l = link.get('href').replace("/pose/", "")
                related_urls.add(l)
            related_urls.discard("#")
        self.poses[url_extension]["Variations"] = list(related_urls)
        # finds and adds transitions into poses to self.poses
        into_urls = set()
        section = soup.find("div", class_="related-poses next-poses")
        if section:
            for link in section.find_all('a'):
                l = link.get('href').replace("/pose/", "")
                into_urls.add(l)
        self.poses[url_extension]["Transitions Into"] = list(into_urls)
        # finds and adds transitions from poses to self.poses
        from_urls = set()
        section = soup.find("div", class_="related-poses previous-poses")
        if section:
            for link in section.find_all('a'):
                l = link.get('href').replace("/pose/", "")
                from_urls.add(l)
        self.poses[url_extension]["Transitions From"] = list(from_urls)
        # finds subheaders and adds to self.poses (difficulty and category)
        lines = soup.find("section", class_="poseDescription").find_all("h5")
        difficulty = ""
        for line in lines:
            if "Difficulty:" in line.text:
                difficulty = line.find_next("span").text
        self.poses[url_extension]["Difficulty"] = difficulty
        category = ""
        for line in lines:
            if "Category" in line.text:
                category = line.find_next("span").text.split()
        self.poses[url_extension]["Category"] = " ".join(category)
        images = soup.find_all('img')
        # save all images if they don't already exist in the image folder
        for image in images:
            self.save_image(image["src"])
        if crawl:
            related_urls.update(into_urls)
            related_urls.update(from_urls)
            urls = [url for url in related_urls if url not in self.to_scrape]
            self.to_scrape.extend(urls)

    def save_image(self, img_url):
        """
        Save an image to the image folder
        :param img_url: url  of the image to save
        :return:
        """
        if len(img_url.split("full/")) <= 1:
            return
        url_name = img_url.split("full/")[1].replace("_R", "").replace("_L", "")
        path = "./images/"+url_name
        # ignore non-pose images
        if os.path.isfile(path):
            # print(img_url + " already exists")
            return
        res = requests.get(img_url, stream=True)
        if res.status_code == 200:
            with open(path, 'wb') as f:
                shutil.copyfileobj(res.raw, f)
            print('Image sucessfully Downloaded: ', url_name)
        else:
            print('Image Couldn\'t be retrieved')



if __name__ == '__main__':
    s = Scraper('https://pocketyoga.com/pose/chair')
    s.test()
    # s.full_scrape(base_url='https://pocketyoga.com/pose/', crawl=False)
    # print(s.to_scrape)
    # json_object = json.dumps(s.poses, indent=4)
    # print(json_object)
    # # s.scrape("https://pocketyoga.com/pose/crow_side_preparation")
    # # s.get_links('https://pocketyoga.com/pose/')

