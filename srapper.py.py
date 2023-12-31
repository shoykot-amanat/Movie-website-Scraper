from bs4 import BeautifulSoup
import requests


def pagination(page_start, page_finish):
    """This function will collect the links of the pages in a list according to user input."""
    root_url = "http://subslikescript.com/movies_letter-A?" # root url of the site we are going to scrape.
    page_link_list = []
    for i in range(page_start, page_finish + 1): # iterating through a range of user input to generate the complete links and save them in a list.
        page_link = f"{root_url}page={i}"
        page_link_list.append(page_link)
    return page_link_list


def get_movie_link(url_list):
    """This function will return a dictionary. which contains the page urls as key and list of movie links of each
    page as value."""
    movie_link_dict = {}
    for url in url_list: # iterating through the url list generated by the function pagination and collecting the movie links of each page and storing them in a dictionary.
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'lxml')
            box = soup.find('article', class_='main-article')
            links = [link['href'] for link in box.find_all('a', href=True)]
            movie_link_dict[url] = links
        except:
            pass
    return movie_link_dict


def movie_file(movie_link_dict):
    """This function will scrape the transcript of every movie and create a file named after movie title"""
    base_url = "https://subslikescript.com"
    for url, links in movie_link_dict.items(): # iterating through the dictionary generated by the function get movie link
        for link in links:
            try:
                response = requests.get(f"{base_url}/{link}") # placing a HTTP request
                soup = BeautifulSoup(response.text, 'lxml') # parsing the htlm document
                block = soup.find('article', class_='main-article') # parsing the block which contains our content
                title = block.find('h1').get_text() # extracting movie title.
                transcript = block.find('div', class_='full-script').get_text(strip=True, separator=' ') #extracting movie transcript
                with open(f'{title}.txt', 'w', encoding='utf-8') as file: # creating txt file named after the title which contains transcript as it's content.
                    file.write(transcript)
            except:
                pass


movie_file(get_movie_link(pagination(1, 3)))
