from tkinter import *
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def crawlers():
    foundLinks = set()
    url = ent1.get()
    print(url)
    
    def request(url): 
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
            soup = BeautifulSoup(response.text, "html.parser")
            return soup
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def craw(url):
        to_crawl = [url]
        
        while to_crawl:
            current_url = to_crawl.pop()
            if current_url not in foundLinks:
                foundLinks.add(current_url)
                print(current_url)
                links = request(current_url)
                if links:
                    for link in links.find_all("a"):
                        found_link = link.get("href")
                        if found_link:
                            found_link = urljoin(current_url, found_link)
                            if urlparse(found_link).scheme in ["http", "https"]:
                                to_crawl.append(found_link)
    
    craw(url)
    
    # Save the collected links to a file
    with open("crawled_links.txt", "w") as file:
        for link in foundLinks:
            file.write(link + "\n")
    
    # Show a messagebox indicating that the file has been saved
    messagebox.showinfo("Bilgi", "Dosyanız kaydedilmiştir.")

pencere1 = Tk()
pencere1.geometry("500x500")
pencere1.title("Website Crawler")

label1 = Label(pencere1, text="Lütfen websitesi adresini giriniz")
label1.pack()
ent1 = Entry(pencere1)
ent1.pack()
buton1 = Button(pencere1, text="Aramak için tıklayın", command=crawlers)
buton1.pack()

pencere1.mainloop()
