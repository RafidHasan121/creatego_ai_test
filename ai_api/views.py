from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
import re, json
from django.conf import settings
from openai import OpenAI

# assistant_id = asst_KjwmG4O67F2jx0Uxa6sI1ggu

client = OpenAI(api_key=settings.API_KEY)

class assistant(APIView):
    auth_headers = {
            "Content-Type" : "application/json",       
            "Authorization" : "Bearer "+ settings.API_KEY, 
            "OpenAI-Beta": "assistants=v1"
        }
    
    # assistant checker
    # def get(self, request, *args, **kwargs):
    #     url = "https://api.openai.com/v1/assistants/asst_KjwmG4O67F2jx0Uxa6sI1ggu"    
    #     result = requests.get(url, headers=self.auth_headers).json()
    #     return Response(result)
    
    # message checker
    def get(self, request, *args, **kwargs):
        try:
            t_id = str(request.query_params.get('t_id'))
            thread_messages = client.beta.threads.messages.list(t_id)
        except:
            thread_messages = client.beta.threads.messages.list("thread_XBEllU5gl6iNUf7mVDbbnNzF")
        
        # # the actual response
        # # print(thread_messages.data[0].content[0].text.value)
        result = thread_messages.data[0].content[0].text.value
        
        # #check for assistant response
        # for x in thread_messages.data:
        #     flag = False
        #     if x.role == 'assistant':
        #         flag = True
        #         break
        
        # # if no assistant response
        # if not flag:
        #     run = client.beta.threads.runs.create(
        #     thread_id=t_id,
        #     assistant_id="asst_KjwmG4O67F2jx0Uxa6sI1ggu"
        #     )
        # while run.status == "completed":
        #     # result = thread_messages.data[0].content[0].text.value
        #     return Response(result)
            


        # Extract the JSON part using regex
        json_part = re.search(r'```json\n({.*?})\n```', result, re.DOTALL)
        if json_part:
            json_string = json_part.group(1)

            # Replace null values with the string "null"
            json_string = json_string.replace('null', '"null"')

            # Parse JSON string to dictionary
            data = json.loads(json_string)

            # Iterate over keys and set values to null
            for key in data.keys():
                if key not in ['childWidgets', 'isPublic']:
                    data[key] = None

        else:
            return Response(client.beta.threads.messages.list(t_id))
        
        return Response(data)
    
    # def post(self, request, *args, **kwargs):
    #     url = "https://api.openai.com/v1/threads"
    #     _msg = request.data.get("msg")
    #     print(_msg)
    #     msg = [{"role": "user", "content": str(_msg)}]
    #     result = requests.post(url, headers=self.auth_headers, data=msg).json()
    #     print(result)
    #     return Response(result)

    def post(self, request, *args, **kwargs):
        _msg = request.data.get("msg")
        msg = [{"role": "user", "content": _msg}]
        #creating new thread
        thread = client.beta.threads.create(messages=msg)
        #creating run
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id="asst_KjwmG4O67F2jx0Uxa6sI1ggu"
        )
        #getting the thread messages list
        thread_messages = client.beta.threads.messages.list(thread.id)
        return Response(thread_messages)