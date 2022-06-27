# %%
 
import bs4
from numpy import subtract
import requests as rq
import pandas as pd
import json
 
 
BASEURL = 'https://oldschool.runescape.wiki/w/Items'
baseurl = 'https://oldschool.runescape.wiki/'
nextpageurl='https://oldschool.runescape.wiki'

#f = open ("output.csv","w")
#f.write("Released,Members,Quest item,Tradeable,Equipable,Stackable,Options,Destory,Examine,Value,High alch,Low alch,Weight,Price,Buy limit,Daily volume,Combat,Skilling,Food,Untradeable,Quest\n")
#f.close()
 
 
def get_sub_categories(soup): #1 finds sub-categories links
    tag = soup.find(text='Subcategories')
    subcategories_links = list()
    if tag=="Subcategories":
        data = soup.find("div",{'id':"mw-subcategories"})
        data2 = data.find("div",class_="mw-content-ltr")
        data3 = data2.find_all("ul")
        for ul in data3:
            lis = ul.find_all("li")
            for li in lis:
                subcategories_links.append(li.find("a")["href"])
    
 
    return subcategories_links
 
 
def add_subcategories_items(url3,subcategories_links,values): #2 add to values items using the subcategories links
    new_sub_links = []
    for link in subcategories_links[:1]:
        res = rq.get(url3+link)
        soup = bs4(res.content,"html.parser")
        tags=soup.find(text='Subcategories')
        data = soup.find("div",class_= "mw-content-ltr")
        data2 = data.find_all("ul")
        if(tags=="Subcategories"):
            new_sub_links = get_sub_categories(soup,new_sub_links)
            #print(new_sub_links)
            values = add_subcategories_items(url3,new_sub_links,values)
            
        for ul in data2:
            lis = ul.find_all("li")
            for li in lis:
                values.append(li.find("a")['href'])
   
    
    return values
 
def whichCategory(item_data,category):
    if(category=="/w/Category:Armour" or category=="/w/Category:Runes" or category=="/w/Category:Weapons"):
        with open('output.csv','a') as f: 
            f.write(f'{item_data["Released"]},{item_data["Members"]},{item_data["Quest item"]},{item_data["Tradeable"]},{item_data["Equipable"]},{item_data["Stackable"]},{item_data["Options"]},{item_data["Destroy"]},{item_data["Examine"]},{item_data["Value"]},{item_data["High alch"]},{item_data["Low alch"]},{item_data["Weight"]},{item_data["Exchange"]},{item_data["Buy limit"]},{item_data["Daily volume"]},{1},{None},{None},{None},{None}\n')

    if(category=="/w/Category:Construction" or category=="/w/Category:Crafting_items" or category=="/w/Category:Farming" or category=="/w/Category:Firemaking" or category=="/w/Category:Fishing" or category=="/w/Category:Fletching" or category=="/w/Category:Hunter" 
        or category=="/w/Category:Mining" or category=="/w/Category:Prayer items" or category=="/w/Category:Runecraft" or category=="/w/Category:Smithing" or category=="/w/Category:Woodcutting"):
            with open('output.csv','a') as f: 
                f.write(f'{item_data["Released"]},{item_data["Members"]},{item_data["Quest item"]},{item_data["Tradeable"]},{item_data["Equipable"]},{item_data["Stackable"]},{item_data["Options"]},{item_data["Destroy"]},{item_data["Examine"]},{item_data["Value"]},{item_data["High alch"]},{item_data["Low alch"]},{item_data["Weight"]},{item_data["Exchange"]},{item_data["Buy limit"]},{item_data["Daily volume"]},{None},{1},{None},{None},{None}\n')
    
    if(category=="/w/Category:Food"):
        with open('output.csv','a') as f: 
            f.write(f'{item_data["Released"]},{item_data["Members"]},{item_data["Quest item"]},{item_data["Tradeable"]},{item_data["Equipable"]},{item_data["Stackable"]},{item_data["Options"]},{item_data["Destroy"]},{item_data["Examine"]},{item_data["Value"]},{item_data["High alch"]},{item_data["Low alch"]},{item_data["Weight"]},{item_data["Exchange"]},{item_data["Buy limit"]},{item_data["Daily volume"]},{None},{None},{1},{None},{None}\n')
    
    if(category=="/w/Category:Quest items"):
        with open('output.csv','a') as f: 
            f.write(f'{item_data["Released"]},{item_data["Members"]},{item_data["Quest item"]},{item_data["Tradeable"]},{item_data["Equipable"]},{item_data["Stackable"]},{item_data["Options"]},{item_data["Destroy"]},{item_data["Examine"]},{item_data["Value"]},{item_data["High alch"]},{item_data["Low alch"]},{item_data["Weight"]},{item_data["Exchange"]},{item_data["Buy limit"]},{item_data["Daily volume"]},{None},{None},{None},{None},{1}\n')
        


def getCategories(BASEURL,df):
 
    base_page = rq.get(BASEURL).content
 
    soup = bs4.BeautifulSoup(base_page,'html.parser')
    div = soup.find(id="mw-content-text")
    div = div.find_all('ul')[-3]
 
    lis = [s.find('a')['href'] for s in div.find_all('li')]
   
    categories  = [s for s in lis]
    #/w/Category:Armour
    #/w/Category:Runecraft
    #/w/Category:Etc..
    for cat in categories[1:]:
        if cat=='/w/Category:Grand_Exchange_items' or cat=="/w/Category:Equipable_items":
            continue 
        content = rq.get(baseurl + cat).content
        soup = bs4.BeautifulSoup(content,'html.parser')
        tag=soup.find(text='Subcategories')
        print('now searching: ',baseurl + cat)
        try:
            dfs_search_itemCategory(bs4.BeautifulSoup(content,'html.parser'),df,category=cat)
            dfs_search_items(bs4.BeautifulSoup(content,'html.parser'),category=cat)
        except Exception as e:
            print('no items here')


def dfs_search_itemCategory(url,df,category=None):
    cat=category
    new_sub_links = []
    subCatItems = get_sub_categories(url)
    if len(subCatItems)!=0:
        for sub in subCatItems:
            content = rq.get(baseurl + sub).content
            soup = bs4.BeautifulSoup(content,'html.parser')
            tag=soup.find(text='Subcategories')
            try:
                if tag == "Subcategories":
                    new_sub_links = get_sub_categories(soup)
                    dfs_search_itemCategory(soup,new_sub_links,category)    
            ###print('item page:',baseurl+sub)
            #dfs_search_itemCategory(url,category=category)
                dfs_search_items(bs4.BeautifulSoup(content,'html.parser'),df,category=cat)
            # insert into df here

            except Exception as e:
                print('no valid items here baby',e)
                pass
    else: 
        dfs_search_items(url,df,category)
 
def dfs_search_items(url,df,category=None):
    items = list()
    div  = url.find('div',{'class':'mw-category'})
    divPage = url.find('div',id ="mw-pages")
    nextPage = divPage.find("a")["href"]
    isLastPage = divPage.find_all(("a"))
    #print(isLastPage)
    #print("tag is ",tag)
    for s in div.find_all('a'):
        try:
            items.append(s['href'])
            #print(s['href'])
                    
        except Exception as e:
            #print('error',e)
            pass 

    for page in isLastPage:
        if page.text.strip()=="next page":
            res=rq.get(nextpageurl+page["href"]).content
            dfs_search_items(bs4.BeautifulSoup(res,'html.parser'),df,category)
        elif page.text.strip()=='previous page':
            pass
        exit

    for item in items:
        # print('now crawling item:',baseurl + item,'of category: ',category[category.find(':')+1:])
        content = rq.get(baseurl + item).content
        #print("sent",baseurl+item)
        crawl(bs4.BeautifulSoup(content,'html.parser'),df,category)
        #print('item',item)
    

def crawl(soup,df,category):
    counter=1
    keys=[]
    values=[]
    item_data = {}
    table = soup.find('table',{'class':'infobox-item'})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    dict_items = dict()


    for row in rows:
        children = row.findChildren(recursive=False)
        if len(children) == 2:
            keys = [x.getText() for x in row.find_all('th')]
            values = [x.getText() for x in row.find_all('td')]

            for key,value in zip(keys,values):
                dict_items[key] = value
    #print(dict_items) 

    with open('keys.json','r') as w:
        item_data = json.load(w)

    for i,key in enumerate(dict_items):
        item_data[key] = dict_items[key].replace(',','')       

    #whichCategory(item_data,category)
    # with open('output.csv','a') as f: 
    #     f.write(f'{item_data["Released"]},{item_data["Members"]},{item_data["Quest item"]},{item_data["Tradeable"]},{item_data["Equipable"]},{item_data["Stackable"]},{item_data["Options"]},{item_data["Destroy"]},{item_data["Examine"]},{item_data["Value"]},{item_data["High alch"]},{item_data["Low alch"]},{item_data["Weight"]},{item_data["Exchange"]},{item_data["Buy limit"]},{item_data["Daily volume"]},{None},{None},{None},{None},{None}\n')
    if(category=="/w/Category:Armour" or category=="/w/Category:Runes" or category=="/w/Category:Weapons"):
        with open('output.csv','a') as f: 
            f.write(f'{item_data["Released"]},{item_data["Members"]},{item_data["Quest item"]},{item_data["Tradeable"]},{item_data["Equipable"]},{item_data["Stackable"]},{item_data["Options"]},{item_data["Destroy"]},{item_data["Examine"]},{item_data["Value"]},{item_data["High alch"]},{item_data["Low alch"]},{item_data["Weight"]},{item_data["Exchange"]},{item_data["Buy limit"]},{item_data["Daily volume"]},{1},{0},{0},{0},{0}\n')

    elif(category=="/w/Category:Construction" or category=="/w/Category:Crafting_items" or category=="/w/Category:Farming" or category=="/w/Category:Firemaking" or category=="/w/Category:Fishing" or category=="/w/Category:Fletching" or category=="/w/Category:Hunter" or category=="/w/Category:Mining" or category=="/w/Category:Prayer items" or category=="/w/Category:Runecraft" or category=="/w/Category:Smithing" or category=="/w/Category:Woodcutting"):
        with open('output.csv','a') as f: 
            f.write(f'{item_data["Released"]},{item_data["Members"]},{item_data["Quest item"]},{item_data["Tradeable"]},{item_data["Equipable"]},{item_data["Stackable"]},{item_data["Options"]},{item_data["Destroy"]},{item_data["Examine"]},{item_data["Value"]},{item_data["High alch"]},{item_data["Low alch"]},{item_data["Weight"]},{item_data["Exchange"]},{item_data["Buy limit"]},{item_data["Daily volume"]},{0},{1},{0},{0},{0}\n')
    
    elif(category=="/w/Category:Food"):
        with open('output.csv','a') as f: 
            f.write(f'{item_data["Released"]},{item_data["Members"]},{item_data["Quest item"]},{item_data["Tradeable"]},{item_data["Equipable"]},{item_data["Stackable"]},{item_data["Options"]},{item_data["Destroy"]},{item_data["Examine"]},{item_data["Value"]},{item_data["High alch"]},{item_data["Low alch"]},{item_data["Weight"]},{item_data["Exchange"]},{item_data["Buy limit"]},{item_data["Daily volume"]},{0},{0},{1},{0},{0}\n')
    
    elif(category=="/w/Category:Quest items"):
        with open('output.csv','a') as f: 
            f.write(f'{item_data["Released"]},{item_data["Members"]},{item_data["Quest item"]},{item_data["Tradeable"]},{item_data["Equipable"]},{item_data["Stackable"]},{item_data["Options"]},{item_data["Destroy"]},{item_data["Examine"]},{item_data["Value"]},{item_data["High alch"]},{item_data["Low alch"]},{item_data["Weight"]},{item_data["Exchange"]},{item_data["Buy limit"]},{item_data["Daily volume"]},{0},{0},{0},{0},{1}\n')
    else:
        with open('output.csv','a') as f: 
            f.write(f'{item_data["Released"]},{item_data["Members"]},{item_data["Quest item"]},{item_data["Tradeable"]},{item_data["Equipable"]},{item_data["Stackable"]},{item_data["Options"]},{item_data["Destroy"]},{item_data["Examine"]},{item_data["Value"]},{item_data["High alch"]},{item_data["Low alch"]},{item_data["Weight"]},{item_data["Exchange"]},{item_data["Buy limit"]},{item_data["Daily volume"]},{0},{0},{0},{0},{0}\n')


 
 
 
df = pd.DataFrame()
# getCategories(BASEURL,df)
df = pd.read_csv('output.csv')
#df.head(50)

df
 
 
 
    
# %%