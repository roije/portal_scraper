import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

class PortalScraper():

    def __init__(self, person, init_page):
        self.person = person
        self.init_soup = self.request_init_page(init_page)

    def request_init_page(self, init_page):
         # request portal.fo 
        res = requests.get(init_page)
        #read text and using bs4 html parser
        soup = BeautifulSoup(res.text, 'html.parser')
        return soup

    def get_person_article_links(self):
        """ 
            Reads through the init page (http://portal.fo/seinastu+vidmerkingarnar.html)
            And gets every comment of search person and stores the link to article in which 
            the comment was given in a Set.
            Returns: Set
        """
        comment_items = self.init_soup.find_all("div", class_="comment_item")
        search_person_article_links = set()

        for comment in comment_items:
            commenter_name = comment.find(class_="comment_profilename").text
            if(commenter_name == self.person):
                search_person_article_links.add(comment.parent.get('href'))
        
        return search_person_article_links
    
    def scrape_articles(self, articles):
        test = 0
        for article in articles:
            test_file = "test-" + str(test) + ".txt"
            comment_section_soup = self.get_comment_section(article)
            with open(test_file, "w", encoding="utf-8") as fo:
                fo.write(str(comment_section_soup.prettify()))
            test = test + 1
    
    def get_comment_section(self, article):
        """
            -- This method is only meant to be used in this file --
            The Facebook Comments Plugin is loaded with Javascript, so we can't use the
            request module to read the articles, because it only gets static server HTML.
            This method uses Selenium, so we can wait for the plugin to have been loaded
            Returns: Soup for each article comment section (BeautifulSoup object)
        """
        driver = webdriver.Chrome()
        driver.get(article)
        timeout = 10
        try:
            # First we have to wait until the page is fully loaded. Using selenium and WebDriverWait to do that
            # Facebook Comments plugin is loaded via Javascript, so we cant use the request module to simply read the page
            element_present = EC.presence_of_element_located((By.CLASS_NAME, 'fb_iframe_widget'))
            WebDriverWait(driver, timeout).until(element_present)

            # Now the Facebook plugin has been loaded
            # First get innerHTML of the page and use BeautifulSoup HTML parser so that we can work with it
            innerHTML = driver.execute_script("return document.body.innerHTML") #returns the inner HTML as a string
            soup_comments = BeautifulSoup(innerHTML, 'html.parser')
            
            # This is the Facebook comments plugin which is an iframe
            facebook_plugin_iframe = soup_comments.find('iframe', class_="fb_ltr")
            frame_id = facebook_plugin_iframe.get('id')

            # Because we need to work with another iframe, we need to change the frame
            # First set the current frame of the driver to the default
            # Then switch to iframe with the id we got from the Facebook comments plugin (line 29)
            # Then get innerHTML of the iframe and use BeautifulSoup so that we can work with it
            driver.switch_to_default_content()
            driver.switch_to.frame(frame_id)
            self.press_open_replies_if_present(driver)
            iframe_innerhtml = driver.execute_script("return document.body.innerHTML") #returns the inner HTML as a string
            iframe_soup = BeautifulSoup(iframe_innerhtml, 'html.parser')
            return iframe_soup

        except TimeoutException:
            print("Timed out waiting for page to load")

    def press_open_replies_if_present(self, driver):
        """
            -- This method is only meant to be used in this file --
        """
        span_show_more_replies = driver.find_elements_by_xpath("//*[contains(text(), 'more replies in this thread') or contains(text(), 'more reply in this thread')]")
        for span_tag in span_show_more_replies:
            # Navigate one level up to the anchor tag
            anchor_clickable = span_tag.find_element_by_xpath('..')
            driver.execute_script("arguments[0].scrollIntoView();", anchor_clickable)
            anchor_clickable.click()
        
        # Wait until all loading spans are gone.
        # The presence of them means that the plugin is loading the comments
        timeout = 10
        try:
            element = WebDriverWait(driver, timeout).until(EC.invisibility_of_element_located((By.XPATH, "//span[@aria-valuetext='Loading...']")))    
        except TimeoutException:
            print("Timed out waiting for element to disappear") 


    def __repr__(self):
        return "Search person: %s" % (self.init_soup)