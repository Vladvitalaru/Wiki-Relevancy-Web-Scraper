#Vlad Vitalaru

import requests
from bs4 import BeautifulSoup
import re
from collections import deque
#importing modules needed for webscraping

'''The purpose of this program is to find how many link jumps it would take to get from
    the first wiki page to the second

Program uses Breadth First Search up to maxDepth jumps before it stops searching
'''


'''This function cleans and returns the proper links that start with wikki'''
def internal_not_special(href):
    if href:
        if re.compile('^/wiki/').search(href):  #return link if starts with wikki
            if not re.compile('/\w+:').search(href):
                if not re.compile('#').search(href):
                    return True
    return False




''' Main function loop '''
def main():

    maxDepth = 7 #variable that simply holds total amount of jumps it will attempt

    print("\n  -- Wiki Relevancy script -- \n")
    print(" Enter the title names of two wiki pages!")
    print(" Some titles are \33[93mCase Sensitive!\33[0m capitalize proper nouns: \33[93mStar Wars\33[0m \n\n")
    firstSite = input(" Enter first wiki page title: ").strip().replace(" ","_").capitalize()
    secondSite = input(" Enter Second wiki page title: ").strip().replace(" ","_").capitalize()
    print("\n")

    #RandomPage = get_random_page_url() #Start program off by calling function that provides a random url from wiki


    visitedSites = set([]) #set used to check if sites have already been visited

    #deque that holds all information needed for each page: wiki, path, depth parent
    deck = deque([['https://en.wikipedia.org', "/wiki/" + firstSite, 0, ""]])


    allSites = deque([['https://en.wikipedia.org/wiki/' + firstSite, ""]]) #deque that holds all sites and their parent link
    output = deque() #special deque used for holding specific output url


    while deck:

        wiki, path, depth, parent = deck.popleft() #This is where we pop the next link node

        print(" Searching through page-", path[6:])

        if depth < maxDepth: #depth cannot go over

            req = requests.get("https://en.wikipedia.org" + path)
            page = BeautifulSoup(req.text, 'html.parser')
            mainBody = page.find(id="bodyContent")


            for link in mainBody.find_all('a', href=internal_not_special): #gets all links in mainbody
                href = (link.get('href'))


                if href not in visitedSites:
                    visitedSites.add(href)
                    deck.append([wiki + href, href, depth + 1, path])
                    allSites.append([href, req.url[24:]])


                if href == "/wiki/" + secondSite:
                    holder = "/wiki/" + secondSite #holder variable used to hold the parent url
                    output.append(["/wiki/" + secondSite])

                    while True:

                        for i in allSites:

                            if i[0] == holder:
                               output.append([i[1]])
                               holder=i[1] #updating holder value

                            if holder == "/wiki/" + firstSite:
                                print("\n")
                                print('\33[92m' ,firstSite.replace("_"," "), "took", depth+1, "jump(s) to find", secondSite.replace("_"," ") + "!\33[0m\n")
                                print(" \33[93mPath:\33[0m")
                                for i in reversed(output):
                                    req = requests.get("https://en.wikipedia.org" + i[0])
                                    page = BeautifulSoup(req.text, 'html.parser')
                                    pageTitle = page.find('h1', id="firstHeading").string #obtaining title from wikipage
                                    print(" " + pageTitle, end="") #printing title page with no new line character
                                    print(' (https://en.wikipedia.org' + i[0] + ")") #formats and prints entire url code

                                print("\n")
                                exit()
        else: #if link could not be found in maxDepth hops, print the wiki link, with an error message
            print("\n")
            print("\nNo Path under 6 jumps Found between", firstSite, "and", secondSite + "!\n")
            #print('https://en.wikipedia.org' + allSites[-1][0])
            print('\n')
            exit()

if __name__ == "__main__":
    main()
