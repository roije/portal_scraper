# The file the executes
from portal import PortalScraper
from bs4 import BeautifulSoup

portal_scraper = PortalScraper('Jóan Pauli Í Geil', 'http://portal.fo/seinastu+vidmerkingarnar.html')

comment_articles = portal_scraper.get_person_article_links()
portal_scraper.scrape_articles(comment_articles)
'''
with open("test-1.txt", "r", encoding="utf-8") as myfile:
    comments = myfile.read()


comments_soup = BeautifulSoup(comments, 'html.parser')
test = comments_soup.find_all(class_='UFICommentActorName')
for bob in test:
    print("HER ER EIN:\n\t")
    #From here we can extract the name
    commenter_div = bob
    print(commenter_div.text)

    #From here we can traverse to the other stuff
    parent_div = bob.parent

    #From here we can extract the comment
    comment_sibling_div = parent_div.find_next_sibling()

    #The comment
    comment = comment_sibling_div.text

    #Likes div
    likes_div = comment_sibling_div.find_next_sibling()
    #print(likes_div)
'''