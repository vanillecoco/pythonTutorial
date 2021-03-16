import csv

def save_to_file(jobs):
  file =open("jobs.csv", mode="w", encoding="utf8") #파일열어 변수에 저장했고
  writer = csv.writer(file) #writer를 만들어줌
  writer.writerow(["title","company","location","link"])
  #리스트로 안넣으면 한글자씩 인식함 
  for job in jobs: #밸류가 필요함
    writer.writerow(list(job.values()))
  return