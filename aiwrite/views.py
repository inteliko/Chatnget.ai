from telnetlib import LOGOUT
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.base import ContentFile



from aiwrite.models import Image
import openai, os
from fpdf import FPDF

from io import BytesIO


from dotenv import load_dotenv
load_dotenv()





def home(request):
    return render(request, "aiwrite/index.html")




@csrf_exempt
def registration(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken. Please choose a different username.")
            return redirect('/signin')
        else:
            myuser = User.objects.create_user(username, email, password)
            myuser.save()
            messages.success(request, "Your Account has been successfully created.")
            return redirect('/signin')
    return render(request, "aiwrite/Registration.html")


@csrf_exempt

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            fname = username
            return redirect('subscription')
   
        else:
            messages.error(request, "Wrong Credentials")
            return redirect('Registration')
    return render(request, "aiwrite/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "loggedout succesfully")
    return redirect('home')


def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'aiwrite/dashboard.html', {'username': request.user.username})
    else:
        return redirect('signin')




#open ai chatbot 

api_key = os.getenv("OPENAI_KEY", None)


def chatbot(request):
    chatbot_response = None 
    if api_key is not None and request.method == 'POST':
        openai.api_key = api_key
        user_input = request.POST.get('user_input')
        prompt = user_input

        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt = prompt,
            temperature=0.5,
            max_tokens=150,
            timeout=10
        )

        chatbot_response = response.choices[0].text

        if chatbot_response is not None:
             # Create a new instance of FPDF class
             pdf = FPDF()

             # Add a new page
             pdf.add_page()

             # Set font and font size
             pdf.set_font("Arial", size=12)

             # Write chatbot response to PDF file
             pdf.cell(200, 10, txt=chatbot_response, ln=1)

             # Save PDF file
             pdf.output("chatbot_response.pdf")


    return render(request, 'aiwrite/chatbot.html', {'chatbot_response': chatbot_response})


#AI IMAGE TO TEXT


import os
import requests
from django.core.files.base import ContentFile
from django.shortcuts import render
from .models import Image
import openai

# Set the OpenAI API key
openai.api_key = os.getenv("OPENAI_KEY", None)


def imgtotxt(request):
    obj = None
    if api_key is not None and request.method == 'POST':
        user_input = request.POST.get('user_input')
        response = openai.Image.create(
            prompt=user_input,
            size='256x256' #'512x512'
        )

        img_url = response["data"][0]["url"]
        response = requests.get(img_url)
        img_file = ContentFile(response.content)

        count = Image.objects.count() + 1
        fname = f"image-{count}.jpg"

        obj = Image(phrase=user_input)
        obj.ai_image.save(fname, img_file)
        obj.save()

        print(obj)



    return render(request, 'aiwrite/textimg.html', {"object": obj} )
            
        
  
#donwload AI Image 

from django.http import FileResponse
import os

def download_image(request, image_id):
    image = Image.objects.get(id=image_id)
    path = image.ai_image.path
    file_name = os.path.basename(path)
    response = FileResponse(open(path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    return response

       
#subscription  

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def subscription(request):
    return render(request, 'aiwrite/subscription.html')