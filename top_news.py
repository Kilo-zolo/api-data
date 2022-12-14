# Import libs
import requests
import pandas as pd
import time
from itertools import groupby
import APIconfig

# Get API specific details and store them in variables
url = "https://real-time-news-data.p.rapidapi.com/top-headlines"

querys = [{"country": "AU", "lang": "en"}, {"country": "IN", "lang": "en"}, {"country": "US", "lang": "en"}]

head = {
	"X-RapidAPI-Key": APIconfig.api_key,
	"X-RapidAPI-Host": "real-time-news-data.p.rapidapi.com"
}

class news_article:

    # Create API Call function
    def get_news_articles(self, url, head, query):
        
        resp = requests.request("GET", url, headers=head, params=query).json()
        rdata = resp['data']
        
        # Choosing the information we want to keep from the dataset 
        for article in rdata:

            title = article['title']
            published = article['published_datetime_utc']
            sep = "T"
            published_date = str(published).split(sep, 1)[0]
            source = article['source_url']
        
        # Creating a list of the info we choose to keep
        title_lst = []
        pub_lst = []
        src_lst = []
        for i in range(len(rdata)):
            for title in rdata[i]:
                title_lst.append(rdata[i]['title'])
            for published in rdata[i]:
                pub_lst.append(published_date)
            for source in rdata[i]:
                src_lst.append(rdata[i]['source_url'])

        # Zipping the lists together
        rough_data = list(zip(title_lst, pub_lst, src_lst))
        # Removing the consecutive duplicates
        smooth_data = [i[0] for i in groupby(rough_data)]

        self.dataout = smooth_data
        pass

class gen_dframe:

   def smooth_to_dframe(self, dataout):
    dframe = pd.DataFrame(dataout, columns=['Headline', 'Published_on', 'Source'] )
    return dframe

news = news_article()    
generate = gen_dframe()

allData = []

for query in querys:
    news.get_news_articles(url,head,query)
    dframe = generate.smooth_to_dframe(news.dataout)
    allData.append(dframe)

print(allData[2])

    


