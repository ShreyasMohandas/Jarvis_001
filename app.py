from flask import Flask,jsonify,request
from llm import *
app=Flask(__name__)

@app.route('/home',methods=['POST'])
async def home():
    data= request.get_json()
    response= await chat_with_me(data['user'])
    print(response)
    return jsonify({"response": response})


if __name__=='__main__':
    app.run(debug=True)

