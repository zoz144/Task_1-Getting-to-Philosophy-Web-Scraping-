from bs4 import BeautifulSoup
import requests 
import time


# A function to check if the link in parentheses
def check_par( paragraph , link_text , index):
    
    link_index = paragraph.index(link_text)
    # Lists of opining and closing bracets index in paragaph " [ " or " ( "
    index_op = [pos for pos, char in enumerate(paragraph) if char == '[']  
    index_cl = [pos for pos, char in enumerate(paragraph) if char == ']']
    index_o = [pos for pos, char in enumerate(paragraph) if char == '(']  
    index_c = [pos for pos, char in enumerate(paragraph) if char == ')'] 
    # If " () " is in paragraph and the link between them return true
    if( ('(' in paragraph) and (index <= len(index_o) -1) ):
        if(link_index > index_o[index] and link_index < index_c[index]): return True
    # If " [] " is in paragraph and the link between them return true   
    if( ('[' in paragraph) and (index <= len(index_o) -1) ):
        if(link_index > index_op[index] and link_index < index_cl[index]): return True
    # If the link text has " [] " rreturn true     
    if( '[' in link_text ): return True
    # Otherwise return false
    return False
    
URL = input("Please Enter the URL of the wikipedia page ? ")
page = requests.get(URL).text

while True:
    # Get the HTML of the page
    soup = BeautifulSoup(page , 'html.parser')
    # Find the class of the main page article
    divv = soup.find("div", {"id": "mw-content-text"})
    div = divv.find("div" , {"class": "mw-parser-output"})
    # Get all direct paragraph children  
    p = div.find_all("p", attrs={'class': None} , recursive=False)
    
    # Find first paragraph which have link that is not in parentheses and get the link
    href = ""
    for i in p:
        if(i.find("a")):
            para = i.getText()
            hrefs = i.find_all('a')
            count = -1
            for j in hrefs: 
                href = j.get('href')
                count += 1
                link = j.text
                check = check_par(para , link , count)
                if(check == False):
                    break
                    
            break
        
    # If there are no links in all paragraphs, then that's a dead-end page    
    if(href == ""):
        print("This page has no link (Dead-End page)")
        break
        
    # Handle the link was to another site ( like wiktionary )      
    if("https" in href):
        print(href)
        page = requests.get(href).text
        time.sleep(0.5)
        continue
    print(href) 
    
    # Stop If the link is Philosophy page. Otherwise, Continue
    if(href != "/wiki/Philosophy"):
        url = "https://en.wikipedia.org" + href
        page = requests.get(url).text
        time.sleep(0.5)
    else:
        print("You have arrived :)")
        break
            
    
    

    
    




            
