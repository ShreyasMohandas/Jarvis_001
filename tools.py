from asgiref.sync import sync_to_async
from google.generativeai.protos import FunctionDeclaration, Schema, Type
import urllib.request
import json

READ_API_KEY='0LKFNGXE07FKRQTX'
CHANNEL_ID=2643942


@sync_to_async
def get_whole_data():
    try:
        url = "http://api.thingspeak.com/channels/{}/feeds.json?api_key={}&last_entry_id=0".format(CHANNEL_ID, READ_API_KEY)
        with urllib.request.urlopen(url) as conn:
            response = conn.read()
            data = json.loads(response)
        return data
    except:
        return {"error": "internal error"}

@sync_to_async
def get_last_data():
    try:
        url = f"http://api.thingspeak.com/channels/{CHANNEL_ID}/feeds/last.json?api_key={READ_API_KEY}"
        with urllib.request.urlopen(url) as conn:
            response = conn.read()
            data = json.loads(response)
        return data
    except:
        return {"error": "internal error"}

@sync_to_async
def set_values(bulb:int,fan:int):
    try:
        print({"bulb":bulb,"fan":fan})
        return {"bulb":bulb,"fan":fan}
    except:
        return {"error": "internal error"}
    


tools = [
    FunctionDeclaration(
        name="get_whole_data",
        description="Fetch the whole information about home automation data: temperature, humidity and PIR sensor",
        parameters=Schema(
            type=Type.OBJECT,
            properties={
                "dummy": Schema(type=Type.STRING, description="This parameter is not used but required for the OBJECT type")
            },
            required=[]
        )
    ),
    FunctionDeclaration(
        name="get_last_data",
        description="Fetch the recent updated home automation data: temperature, humidity and PIR sensor",
        parameters=Schema(
            type=Type.OBJECT,
            properties={
                "dummy": Schema(type=Type.STRING, description="This parameter is not used but required for the OBJECT type")
            },
            required=[]
        )
    ),
    FunctionDeclaration(
       name="set_values",
       description="Set the values for a bulb and fan, if the user said to turn 'on' bulb or fan - their respective arguments passed should be 1 , if mentioned to turn 'off' bulb or fan - then pass function argument as 0 for that device",
       parameters=Schema(
           type=Type.OBJECT,
           properties={
               "bulb": Schema(type=Type.INTEGER, description="The value to set for the bulb"),
               "fan": Schema(type=Type.INTEGER, description="The value to set for the fan")
           },
           required=["bulb", "fan"]
       )
   )
]