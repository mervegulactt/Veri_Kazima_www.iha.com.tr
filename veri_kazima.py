import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from IPython.display import clear_output

#Kategoriler
sections = ["http://www.iha.com.tr/gundem/",
            "http://www.iha.com.tr/ekonomi/",
            "http://www.iha.com.tr/dunya/"]

urls = []
# Öncelikle bir Kategori seçiyoruz.
for section in sections:
    # Kategorinin içerisinde kaç sayfa dolaşılacağı belirlenir.
    for i in range(1, 2):
        try:
            # Öncelikle URL'imizi oluşturuyoruz. Örneğin;
            # http://www.iha.com.tr/gundem/1
            newurl = section + str(i)
            print(newurl)

            # Url'nin içerisindeki bütün html dosyasını indiriyoruz.
            html = requests.get(newurl).text
            soup = bs(html, "lxml")

            #makaleleri tags adında bir değişkene topluyoruz.
            tags = soup.findAll("div", class_="row newslist")[0]

            # Sırayla bütün makalelere girip, href'in içerisindeki linki urls adlı listemize append ediyoruz.
            for a in tags.find_all('a', href=True):
                urls.append((section.split("/")[4], a['href']))
        except IndexError:
            break

urldata = pd.DataFrame(urls)
urldata.columns = ["Kategori","Link"]
urldata.head()
#Bazı linkler çoklamışlar, onlardan kurtulmak için drop_duplicates() #Fonksiyonunu kullanıyoruz.
urldata = urldata.drop_duplicates()
urldata.to_csv('urldata.csv')

def GetData(url):
    try:
        # Url içerisindeki html'i indiriyoruz.
        html = requests.get(url).text
        soup = bs(html, "lxml")

        # Belirlediğimiz element'in altındaki bütün p'leri seçiyoruz.
        body_text = soup.findAll("div", class_="content")[0].findAll('p')

        # Body_text adındaki metni tek bir string üzerinde topluyoruz.
        body_text_big = ""
        for i in body_text:
            body_text_big = body_text_big + i.text


        return ((url, body_text_big))

    # Link boş ise verilen hata üzerine Boş Data mesajını dönüyor.
    except IndexError:
        return ("Boş Data")


#Veri kazıma, Url datasındaki linkleri tek tek fonksiyon ile çalıştırıp, sonuçları bigdata listesine kaydediyor.
bigdata = []
k = 0
for i in urldata.Link:
    clear_output(wait=True)
    print(k)
    print(i)
    bigdata.append(GetData(i))
    k = k + 1

#Verileri DataFrame olarak kaydetme
bigdatax = pd.DataFrame(bigdata)
bigdatax.columns = ["Link","Body_text"]
bigdatax = bigdatax.loc[bigdatax.Link.drop_duplicates().index]
bigdatax.index = range(0,len(bigdatax))
bigdatax.head()
bigdatax.to_csv("bigdata.csv")
