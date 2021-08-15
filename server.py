from flask import *
from flask_cors import CORS
  
app = Flask(__name__) #creating the Flask class object   
CORS(app) 

@app.route('/') #decorator drfines the   
def home():
    return "This is poll-simulator app server";

@app.route('/add',methods = ['POST'])
def add():  
    data = request.get_json()
    print(data)
    f = open("poll.txt", mode='a', encoding='utf-8')
    f.write((data['name']+" 0 \n"))
    return {"Message":"data added."}

@app.route('/vote',methods = ['POST'])
def vote():
      resdata = request.get_json()
      print(resdata)

      if (202012120 - int(resdata['voterId']) < 0 or 202012120 - int(resdata['voterId']) > 120):
            print("invalid")
            return {"message" : "voterID Invalid.", "response" : 204}

      v = open("voters.txt", mode='a+', encoding='utf-8')
      v.seek(0)
      voterfile = v.readlines()

      for voters in voterfile:
            if voters == (resdata['voterId'] + " \n"):
                  return {"message" : "This voterID already voted.", "response" : 202}
      # print(voterfile)
      
      v.write(resdata['voterId'] + " \n")
      v.close()

      f = open("poll.txt", mode='r', encoding='utf-8')
      file = f.readlines()
      f.close()

      dataArray = []
      for candidates in file:
            splitData = candidates.split(" ")
            if splitData[0] == resdata['selectedCandidate']:
                  splitData[1] = str(int(splitData[1]) + 1)
            dataArray.append(splitData)
      
      f = f = open("poll.txt", mode='w', encoding='utf-8')
      for data in dataArray:
            f.write((data[0] + " " + data[1] + " \n"))

      return "Welcome %s"

@app.route('/winner',methods = ['GET'])
def winner():  
      f = open("poll.txt", mode='r', encoding='utf-8')
      file = f.readlines()
      f.close()

      dataArray = []
      for candidates in file:
            splitData = candidates.split(" ")
            dataArray.append(splitData)
      
      print(dataArray[0][0])
      
      winner = 0
      setArray  = []
      for data in dataArray:
            if (int(data[1]) > winner):
                  winner = int(data[1])
                  if len(setArray) > 0 :
                        setArray.pop()
                  setArray.append(data)
                  
      return jsonify(setArray)

@app.route('/voteSummary',methods = ['GET'])
def voteSummary():  
      f = open("poll.txt", mode='r', encoding='utf-8')
      datas = f.readlines()
      newArray = []
      for data in (datas):
        temp = data.split()
      #   print(temp)
        newArray.append({"name" : temp[0], "votes" : int(temp[1])})
      print(newArray)
      return jsonify(newArray)

if __name__ =='__main__':
    app.run(debug = True)