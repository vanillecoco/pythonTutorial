from flask import Flask, render_template, request, redirect, send_file
from scrapper import get_jobs
from export import save_to_file

app = Flask("SuperScrapper")

db ={} #라우터 바깥에 있어야함 db에 값이 들어있으면 다시 안불러도됨

#웹사이트에 띄우고 싶은 문구 not found가 아닌
@app.route("/")
def home():
  return render_template("potato.html")

@app.route("/report") #폼 액션에 넣은 report
def report():
  # print(request.args.get('gogo'))
  #print(request.args)
  word = request.args.get('gogo')
  if word: #if word exists
    word = word.lower()
    #데이터 베이스 안에 내용이 있는지 체크
    existingJobs = db.get(word)
    if existingJobs:
      jobs = existingJobs #다시 만들지 않고 사용
    else:
      jobs = get_jobs(word)
      db[word] = jobs
  else:
    #리다이렉트
    return redirect("/")
  #return f"You are looking for a job in {word}"
  return render_template(
    "report.html",
     searchingBy=word, 
     potato="sexy",
     resultsNumber=len(jobs),
     jobs =jobs) #이부분에 담긴 값을 html에서 for문으로 불러옴

# @app.route("/<username>")
# def potato(username):
#   return f"Hello {username} how are you doing"  


@app.route("/export")
def export():
  try:
    word =request.args.get('gogo')
    if not word:
      raise Exception()
    word = word.lower()
    jobs = db.get(word)
    if not jobs:
      raise Exception()
    #return f"Generate CSV for {word}"  
    save_to_file(jobs)
    return send_file("jobs.csv")
  except:
    return redirect("/") #에러나면 첫페이지로 보내
 
    
app.run(host="0.0.0.0") #리플 안에 있으니 호스트설정이렇게


