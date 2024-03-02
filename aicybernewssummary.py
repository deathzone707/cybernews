#!/usr/bin/env python3

import google.generativeai as genai
from os import environ
from urllib.request import urlopen
from bs4 import BeautifulSoup
from cybernews.cybernews import CyberNews
from datetime import datetime

"""
To function properly a Google Gemini API key must be saved to your local environment variables.
export GEMINI_API_KEY='<your API key>'
"""

model = genai.GenerativeModel('gemini-pro')
gemini_api_key = environ["GEMINI_API_KEY"]
genai.configure(api_key = gemini_api_key)
prompt = "You are an expert content summarizer. You take content in and output a summary using the format below. Combine all of your understanding of the content into a single, 20-word sentence in a section called ONE SENTENCE SUMMARY:. Output the 10 most important points of the content as a list with no more than 15 words per point into a section called MAIN POINTS:. Output a list of the 5 best takeaways from the content in a section called TAKEAWAYS:. Create the output using the formatting above. You only output human readable Markdown. Output numbered lists, not bullets. Do not output warnings or notes, just the requested sections. Do not repeat items in the output sections. Do not start items with the same opening words. INPUT FOR SUMMARIZATION: "
newsTypes = ["general", "dataBreach", "cyberAttack", "vulnerability", "malware", "security", "cloud", "tech", "iot", "bigData", "business", "mobility", "research", "socialMedia", "corporate"]
filename = "/CyberSecurityArticleSummaries.txt"
path = environ["HOME"]
file = path+filename
f = open(file, 'a')

def get_article(newsType):
  news = CyberNews()
  stories = news.get_news(newsType)
  urlLst = []
  for story in stories:
     if str('fullURL') in story:
       if str('https://thehackernews.com') in story.get('fullURL'):
        newsURL2 = story.get('newsURL')
        urlLst.append(newsURL2)
       else:
         newsURL2 = story.get('fullURL')+story.get('newsURL')
         urlLst.append(newsURL2)
  return urlLst

if __name__ == "__main__":
    f.write(datetime.today().strftime('%Y-%m-%d %H:%M:%S')+"\n")
    for newsType in newsTypes:
      f.write("-"*50+"\n")
      f.write(newsType.upper() + " ARTICLES!"+"\n")
      f.write("-"*50+"\n")
      newsArticles = get_article(newsType)
      try:
        for newsArticle in newsArticles:
          if ".com" in newsArticle:
            f.write("*="*30+"\n")
            f.write("News Article: "+newsArticle+"\n")
            f.write("-"*50+"\n")
            page = urlopen(newsArticle).read()
            soup = BeautifulSoup(page, 'html.parser')
            if 'https://thehackernews.com' in newsArticle:
              body = soup.find("div", class_="articlebody")
            elif 'economictimes.indiatimes.com' in newsArticle:
              body = soup.find("div", class_="article-section__body__news")
            else:
              f.write("Unsupported News Article: "+newsArticle+"\n")
              f.write("*="*30+"\n")
              pass
            response = model.generate_content(prompt+str(body))
            f.writelines(response.text+"\n")
            f.write("*="*30+"\n")
          else:
            f.write("Unsupported News Article: "+newsArticle+"\n")
            f.write("*="*30+"\n")
      except:
        pass
    f.close()