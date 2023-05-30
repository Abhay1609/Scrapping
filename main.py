import requests
from bs4 import BeautifulSoup
import pandas as pd
url=input("Enter url:")
depth=int(input("Enter Depth:"))
r=requests.get(url)
print(r.status_code)
soup=BeautifulSoup(r.text, "html.parser")
np=soup.find_all("a")
Valid=[]
Invalid=[]
Invalid_page=[]
New_valid=[]
Done=set()
for i in np:
    link=i.get("href")
    try:
        req = requests.get(link)
        status=req.status_code
    except:
        if link != None:
            link=url+link
            req=requests.get(link)
            status=req.status_code
        status=400
    if status == 404:
        if link not in Invalid:
            Invalid.append(link)
            Invalid_page.append(url)
    else:
        if link not in Valid:
            Valid.append(link)
Done.add(url)

for dep in range(0,depth):

    for new_url in Valid:

        if (new_url not in Done) and (new_url!= None):
            r = requests.get(new_url)
            soup = BeautifulSoup(r.text, "html.parser")
            np = soup.find_all("a")

            for i in np:
                link = i.get("href")

                try:
                    req = requests.get(link)
                    status = req.status_code
                except:

                    link = new_url + link
                    req = requests.get(link)
                    status = req.status_code

                if status == 404:
                    if link not in Invalid:
                        Invalid.append(link)
                        Invalid_page.append(new_url)



                else:
                    if (link not in Valid) and (link not in New_valid):
                        New_valid.append(link)

            Done.add(new_url)
    Valid=New_valid





Invalid=list(Invalid)
print("All link is ",len(Done)+len(Invalid)+len(Valid))
print("Invalid link is",len(Invalid))
df = pd.DataFrame({"Invalid":Invalid,"Invalid_page":Invalid_page})
print(df)
df.to_csv("broken_link.csv")

