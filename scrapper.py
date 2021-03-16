import requests
from bs4 import BeautifulSoup

def get_last_page(url):
  result = requests.get(url)  

  soup = BeautifulSoup(result.text, 'html.parser')
  pagination = soup.find("div",{"class":"s-pagination"})
  #print(pagination)
  pages = pagination.find_all('a') #모든링크를 찾음

  max_page = pages[-2].get_text(strip=True)
  #print(max_page)
  return int(max_page)

def extract_job(html):
  title = html.find("h2",{"class":"mb4"}).find("a")["title"]

  company, location =html.find("h3").find_all("span", recursive=False)
  company = company.get_text(strip=True)
  location = location.get_text(strip=True).strip('-').strip(" \r").strip("\n")
  
  link = html["data-jobid"]
  #print(link)
  return {
    "title":title,
    "company":company,
    "location":location,
    "link": f"https://stackoverflow.com/jobs/{link}"
    }

def extract_jobs(last_page,url):
  jobs = []
  for page in range(last_page):
    #print(f"Scrapping SO: PAGE: {page}")
    #print(page+1) #1부터 끝까지 출력
    result = requests.get(f"{url}&pg={page+1}")
    #print(result.status_code)
    soup = BeautifulSoup(result.text, 'html.parser') #copy soup
    results = soup.find_all("div",{"class":"-job"})
   # print(results) 리스트
  
  for result in results:
    job = extract_job(result)
    jobs.append(job)
  return jobs

def get_jobs(word):
  url=f"https://stackoverflow.com/jobs?q={word}&sort=i"
  last_page = int(get_last_page(url))
  jobs = extract_jobs(last_page, url)
  
  return jobs 




