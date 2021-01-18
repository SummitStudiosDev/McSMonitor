from flask import Flask
from flask import render_template
#from flask import redirect, url_for
import datetime
import json
from mcstatus import MinecraftServer
from flask_apscheduler import APScheduler


 
app = Flask(__name__,static_folder='static')

def write_json(data, filename='count.json'): 
    with open(filename,'w') as f: 
        json.dump(data, f, indent=4) 
      
 
def log():
  with open('serverip.json') as json_file: 
      data = json.load(json_file) 
      data = data['server'] 
      ip = (data[0]['ip'])
      port = int(data[0]['port'])

  server = MinecraftServer(ip,port)
  status = server.status()
  playercount = status.players.online
  print("The server has {0} players and replied in {1} ms".format(status.players.online, status.latency))

  #now = datetime.datetime.now()
  #print(now.strftime('%H:%M:%S on %A, %B the %dth, %Y')) this is in gmt
  #hms = now.strftime('%H:%M:%S')
  hms = datetime.datetime.now().isoformat()
  print(hms+" : "+str(playercount))


  with open('count.json') as json_file: 
      data = json.load(json_file) 
        
      temp = data['playercount'] 
    
      y = {"time": hms, 
          "players": str(playercount)
          } 
    
    
      temp.append(y) 
        
  write_json(data)  



@app.route("/")
def chart():
  '''
    f = open('count.json') 
    data = json.load(f) 
    f.close()
    labels = []
    values = []

    for i in data['playercount']: 
      #print(i) 
      labels.append(i["time"])
      values.append(i["players"])
      

    #print(labels)
    #print(values)

    legend = "Player Count"
    #maxp = 100000000



    return render_template('chart.html', values=values, labels=labels, legend=legend ) '''
  f = open('count.json') 
  data = json.load(f) 
  f.close()
  labels = []
  values = []

  for i in data['playercount']: 
      #print(i) 
    labels.append(i["time"])
    values.append(i["players"])

  z = list(zip(labels,values))

  return render_template('chart2.html', cdata = z)
 
 
 
@app.route("/log")
def manual_log():
  log()


  #return redirect(url_for('chart'))
  return render_template('h.html')


'''
@app.route("/clear")
def clear():
  data = {
	"playercount":[
	]
  }
  with open("count.json",'w') as f: 
      json.dump(data, f, indent=4) 

  return render_template('h.html')
'''


def minute_log(text):
    print(text, str(datetime.datetime.now()))
    log()
    
def weekly_clear(text):
    print(text, str(datetime.datetime.now()))

    day = datetime.datetime.today().strftime('%A')
    print("today:",day)
    with open ("day.txt", "r") as myfile:
      lchecked=myfile.read()
    print("last checked:",lchecked)
    if(day=="Monday"):
      if(day != lchecked):
        print("clear!")
        data = {
            "playercount":[
          ]
        }
        with open("count.json",'w') as f: 
            json.dump(data, f, indent=4) 

    with open("day.txt", "w") as myfile:
      print("Writing last checked to file")
      myfile.write(day)
    print()

if __name__ == "__main__":
    scheduler = APScheduler()
    scheduler.add_job(func=minute_log, args=['job run minute log '], trigger='interval', id='minutelog', minutes=1)
    scheduler.add_job(func=weekly_clear, args=['job run hour check '], trigger='interval', id='weeklyclear', hours=1)
    #24 (hours) * 7 (days per week) = 168 (one week)

    scheduler.start()

    print("Server Start at",str(datetime.datetime.now()))
    app.run(host='0.0.0.0', port=8080)
    print("Server Start Log")
    log()