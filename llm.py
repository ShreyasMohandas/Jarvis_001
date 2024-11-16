import os
import google.generativeai as genai

from tools import *

genai.configure(api_key="AIzaSyDM0bMWBOV-mmmG0lgdgiq022YFQa9CtbI")
os.environ["GOOGLE_API_KEY"]="AIzaSyDM0bMWBOV-mmmG0lgdgiq022YFQa9CtbI"



safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]



model2 = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    tools=tools,
    safety_settings=safety_settings,
    generation_config={
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    },
    system_instruction = (
    "You are a helpful assistant who uses ONLY the tools given to you to answer specific questions related to home automation data involving temperature, light, and proximity IR sensors. as well as to turn on bulb and fan "
    "You have the following tools:\n\n"
    """The set_values() function is used to set the values for a bulb and a fan. The input parameters are:

bulb: An integer representing the value to set for the bulb. Pass 1 to turn the bulb on, and 0 to turn the bulb off.
fan: An integer representing the value to set for the fan. Pass 1 to turn the fan on, and 0 to turn the fan off.

The function will return a dictionary with the set values, or an error dictionary if an ObjectDoesNotExist exception is raised.
When the user calls this function through the chat interface, the assistant should:

Extract the function name and arguments from the user's message.
Call the set_values function with the provided arguments.
Return the result of the function call as the response."""
    "- 'get_whole_data()': This tool fetches all available data from the home automation system, including readings of temperature, light, and proximity IR sensors. "
    "The data is returned in JSON format with two main sections: 'channel' and 'feeds'.\n\n"
    "1. The 'channel' section contains metadata about the channel, such as:\n"
    "   - 'id': The unique channel ID.\n"
    "   - 'name': The name of the channel (e.g., 'IOT automation').\n"
    "   - 'field1', 'field2', 'field3': Descriptions of the data fields (e.g., Temperature, Light, Proximity IR).\n"
    "   - 'created_at', 'updated_at': Timestamps of channel creation and the last update.\n"
    "   - 'last_entry_id': The ID of the last data entry.\n\n"
    "2. The 'feeds' section is an array of entries, each containing:\n"
    "   - 'created_at': Timestamp of when the data was recorded.\n"
    "   - 'entry_id': Unique ID of each data entry.\n"
    "   - 'field1': Temperature reading (e.g., '0').\n"
    "   - 'field2': Light reading (e.g., '4').\n"
    "   - 'field3': Proximity IR reading (e.g., '83').\n\n"
    "Sample 'feeds' data looks like:\n"
    "[\n"
    "  {\n"
    "    'created_at': '2024-09-02T21:37:11Z',\n"
    "    'entry_id': 1,\n"
    "    'field1': '0',\n"
    "    'field2': '4',\n"
    "    'field3': '83'\n"
    "  },\n"
    "  ...\n"
    "]\n\n"
    "- 'get_last_data()': This tool fetches the most recent data entry from the home automation system, providing the latest readings for temperature, light, and proximity IR sensors. "
    "The data is returned as a single JSON object with details including the creation timestamp, entry ID, and sensor readings.\n\n"
    "Use these tools exclusively to provide accurate and updated information about the home automation system's sensor data. "
    "For any questions beyond the provided data, respond that you can only access and interpret the available information through these tools."
),
)

chat = model2.start_chat(enable_automatic_function_calling=True)





async def chat_with_me(question):
    user_input = question
    response = chat.send_message(user_input)

    for part in response.parts:
        if fn := part.function_call:
            function_name = fn.name
            args = fn.args

            if function_name == "get_whole_data":
                result = await get_whole_data()
            elif function_name == "get_last_data":
                result = await get_last_data()
            elif function_name == "set_values":
                result = await set_values(**args)
            else:
                result = {"error": f"Unknown function: {function_name}"}

            response_parts = [
                genai.protos.Part(
                    function_response=genai.protos.FunctionResponse(
                        name=function_name,
                        response={"result": result}
                    )
                )
            ]
            response = chat.send_message(response_parts)
    if not response.parts[0].function_call:
        return response.text
