from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
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
        thread_messages = client.beta.threads.messages.list("thread_MjhfZLxDS7rOlLzX3s2Cb2Xm")
        # the actual response
        # print(thread_messages.data[0].content[0].text.value)
        result = thread_messages.data[0].content[0].text.value
        return Response(result)
    
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