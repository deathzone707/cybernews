#!/usr/bin/env python3

import google.generativeai as genai
from os import environ
from urllib.request import urlopen
from bs4 import BeautifulSoup
from cybernews import CyberNews
from datetime import datetime
from multiprocessing import Pool

"""
To function properly a Google Gemini API key must be saved to your local environment variables.
export GEMINI_API_KEY='<your API key>'
"""

class AICyberNewsSummary:
  gemini_api_key = environ["GEMINI_API_KEY"]
  genai.configure(api_key = gemini_api_key)
  def __init__(self, newsType) -> None:
    self._newsType = newsType
    self._prompt = "You are an expert content summarizer. You take content in and output a summary using the format below. Combine all of your understanding of the content into a single, 20-word sentence in a section called ONE SENTENCE SUMMARY:. Output the 10 most important points of the content as a list with no more than 15 words per point into a section called MAIN POINTS:. Output a list of the 5 best takeaways from the content in a section called TAKEAWAYS:. Create the output using the formatting above. You only output human readable Markdown. Output numbered lists, not bullets. Do not output warnings or notes, just the requested sections. Do not repeat items in the output sections. Do not start items with the same opening words. INPUT FOR SUMMARIZATION: "
    self._model = genai.GenerativeModel('gemini-pro')
  def get_article(self, newsType) -> list:
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
  
  def ai_summary(self, newsArticle):
    output ="-"*50+"\n"
    output += "!!!"+self._newsType.upper() + " ARTICLE!!!"+"\n"
    output += "-"*50+"\n"
    if ".com" in newsArticle:
      output += "*="*30+"\n"
      output += "News Article: "+newsArticle+"\n"
      output += "-"*50+"\n"
      page = urlopen(newsArticle).read()
      soup = BeautifulSoup(page, 'html.parser')
      if 'https://thehackernews.com' in newsArticle:
        title = soup.find("h1")
        body = soup.find("div", class_="articlebody")
      elif 'economictimes.indiatimes.com' in newsArticle:
        title = soup.find("h1")
        body = soup.find("div", class_="article-section__body__news")
      else:
        output += "Unsupported News Article: "+newsArticle+"\n"
        output += "*="*30+"\n"
        pass
      response = self._model.generate_content(self._prompt+str(body))
      output += title.get_text()+"\n"
      output += response.text+"\n"
      output += "*="*30+"\n"
    else:
      output += "Unsupported News Article: "+newsArticle+"\n"
      output += "*="*30+"\n"
    return output

  def summary(self):
    pool = Pool(8)
    newsArticles = self.get_article(self._newsType)
    result = pool.map(self.ai_summary, newsArticles)
    return ''.join(result)