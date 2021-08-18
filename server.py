from flask import *
from flask_cors import CORS
  
app = Flask(__name__) #creating the Flask class object   
CORS(app)

candidatesArray = []
p = open("poll.txt", mode='r', encoding='utf-8')
datas = p.readlines()
p.close()
for data in (datas):
      temp = data.split()
      candidatesArray.append({"name" : temp[0], "votes" : int(temp[1])})
print(candidatesArray)

votersArray = []
v = open("voters.txt", mode='a+', encoding='utf-8')
v.seek(0)
voters = v.readlines()
v.close()
for voter in (voters):
      temp = voter.split()
      votersArray.append(int(temp[0]))
print(votersArray)

@app.route('/') #decorator drfines the   
def home():
    return "This is poll-simulator app server";

@app.route('/add',methods = ['POST'])
def add():
      data = request.get_json()
      if (int(data['pin']) == 214365):
            candidatesArray.append({"name" : data['name'], "votes" : 0})
            f = open("poll.txt", mode='a', encoding='utf-8')
            f.write((data['name']+" 0 \n"))
            f.close()
            return {"Message":"data added.", "status":200}
      return {"Message":"Pin invalid", "status":201}

@app.route('/vote',methods = ['POST'])
def vote():
      resdata = request.get_json()
      print(resdata)
      if (resdata['voterId'] == ''):
            return {"message" : "Please Provide voterID to proceed further.", "response" : 202}

      if (int(resdata['voterId']) > 202012120
          or int(resdata['voterId']) < 202012000):
            return {"message" : "voterID Invalid.", "response" : 202}

      for voter in votersArray:
            if voter == (int(resdata['voterId'])):
                  return {"message" : "This voterID already voted.", "response" : 204}

      if (resdata['selectedCandidate'] == 0):
            return {"message" : "Please select any candidate to vote", "response" : 203}

      votersArray.append(int(resdata['voterId']))
      with open("voters.txt", mode='a+', encoding='utf-8') as v:
            v.write(resdata['voterId'] + " \n")
      for candidate in candidatesArray:
            if(candidate['name'] == resdata['selectedCandidate']):
                  candidate['votes'] = candidate['votes'] + 1;

      with open("poll.txt", mode='w', encoding='utf-8') as p:
            for candidate in (candidatesArray):
                  p.writelines(candidate['name']+" "+str(candidate['votes'])+" \n")
      return {"message" : "Your vote is sucessfully added, Thanks for voting", "response" : 200}

@app.route('/winner',methods = ['GET'])
def winner():
      winner = 0
      setArray  = []
      for candidate in candidatesArray:
            if (candidate['votes'] == winner and winner != 0):
                  return {"message" : "It's Tie", "response" : 201}
            elif(candidate['votes'] > winner):
                  winner = candidate['votes']
                  if len(setArray) > 0:
                        setArray.pop()
                  setArray.append(candidate)
      if(winner == 0):
            return {"message" : "no winner", "response" : 201}
      return jsonify(setArray)

@app.route('/voteSummary',methods = ['GET'])
def voteSummary():  
      return jsonify(candidatesArray)

if __name__ =='__main__':
    app.run(debug = True)