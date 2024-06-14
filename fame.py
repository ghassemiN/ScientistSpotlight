from openai import OpenAI
from pathlib import Path
import os ,json
from credentials import OPENAI_API_KEY


# Get the OpenAI key from the environment variables

openai_key = OPENAI_API_KEY

client = OpenAI(api_key=openai_key)


with open('fame_persons.txt', 'r') as file:
    listed_famous = [line.rstrip('\n') for line in file.readlines()]

get_full_name = [{
    "name": "get_full_name",
    "description": "Get person name and gender",
    "parameters": {
        "type": "object",
        "properties": {
            "full-name": {
                "type": "string",
                "description": "only one person full name"
            },
            "gender": {
                "type": "string",
                "description": "Person gender e.g. He or She"
            }
        },
        "required": [ "full-name", "gender" ]
    }
}]

get_person_full_info = [{
    'name': 'get_person_full_info',
    "type": "function",
    "description": "Get details about input person",
    "function": {
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The full Name and nickname/alias"
                },
                "fields": {
                    "type": "string",
                    "description": "What field/fields they were fameous"
                },
                "life": {
                    "type": "string",
                    "description": "Details about their personal and professional life"
                },
                "famous-for": {
                    "type": "string",
                    "description": "Why are they famous? Describe it in a simple words until a child can understand it."
                },
                "prizes": {
                    "type": "string",
                    "description": "What prizes? when?"
                }
            },
            "required": [ "name", "fields", "life", "famous-for", "prizes" ]
        }
    }
}]

get_person_personal = [{
    'name': 'get_person_personal',
    "type": "function",
    "description": "Get details about personal life of input person",
    "function": {
        "parameters": {
            "type": "object",
            "properties": {
                "life": {
                    "type": "string",
                    "description": "Details about their personal and professional life"
                }
            }
        }
    }
}]

message_content = "Give me a only one name of famous person in science. IMPORTANT NOTE : Not from this list:  "+str(listed_famous)
print(message_content+"\n")
try:
    response = client.chat.completions.create(
        model="gpt-4-0613",
        messages=[{"role": "user", "content": message_content }],
        functions = get_full_name,
        function_call = 'auto'
    )
except Exception as e:
    print("Error!")

print(response.choices[0])
print("\n")
person = ""

if response.choices[0].finish_reason == "function_call" and response.choices[0].message.function_call.arguments != None:
    person = json.loads(response.choices[0].message.function_call.arguments)["full-name"]
    gender = json.loads(response.choices[0].message.function_call.arguments)["gender"]

if response.choices[0].finish_reason == "stop" and response.choices[0].message.content != None:
    person = json.loads(response.choices[0].message.content)["full-name"]
    gender = json.loads(response.choices[0].message.content)["gender"]

if person == "":
    print("No person found!")
    exit()

###############################################
# Get the person info 
###############################################
message_content = "Give me a full information about "+person+", including field of study, prizes "+gender+" have won, and details about life"
print(message_content+"\n")


response.choices[0].finish_reason = "function_call"
while response.choices[0].finish_reason == "function_call":
    try:
        response = client.chat.completions.create(
            model="gpt-4-0613",
            messages=[{"role": "user", "content": message_content }],
            functions = get_person_personal,
            function_call = 'auto'
        )
    except Exception as e:
        print("Error!")

print(response.choices[0])

###############################################
# Write the person name in the file 
###############################################
def write_to_file(person):
    with open('fame_persons.txt', 'r+') as f:
        fame_persons = f.read().splitlines()
        if person not in fame_persons:
            f.write(f"{person}\n")

write_to_file(person)

###############################################
# text to speech 
###############################################
#Comming soon, I don't know when, soon as soon as the sloth reaches the other end of the forest. Now you have to find which sloth in which forest, where in that forest... so simple and quick.