from django.shortcuts import redirect, render
from django.core.mail import send_mail
import random


# Create your views here.
def home(request):
     
      return render(request, "index.html")

   

def display(request):
     if request.method == "POST":
         name=request.POST['name'] 
         email=request.POST['email']
         subject=request.POST['subject']
         message=request.POST['message']
        
         otp = random.randint(1000, 9999)    # better OTP range
         print(str(otp))
         request.session['test'] = otp
         request.session['contact_email'] = email

         if email:
            send_mail(
               subject="Thank you for contacting the page",
               message=f""" 
               Hi  {name} , this is an welcome message from manasa ,we'll get what your looking from me as soon as possible, thank you for contacting us.your OTP is {otp}.""",
               from_email="manasays2001@gmail.com",
               recipient_list=[email],
               fail_silently=True
            )
            send_mail(
               subject="New user enquiry",
               message=f""" 
               Hi  {name} , enquired about {subject} with the message {message} and the email is {email}.""",
               from_email="shreyasms6@gmail.com",
               recipient_list=[email],
               fail_silently=True
            )
            print("mail sent successfully")
            return redirect(request,"verify_otp")
          
def verify_otp(request):
    if request.method == "POST":
        otp = request.POST.get('otp')
        generated_otp = request.session.get('otp')

        if otp == generated_otp:
            return render(request, "index.html", {"success": "OTP Verified"})
        else:
            return render(request, "display.html", {"error": "Invalid OTP"})
     
def contact(request):
    
      if request.method == "POST":
         name=request.POST['name'] 
         email=request.POST['email']
         subject=request.POST['subject']
         message=request.POST['message']

         if email:
            send_mail(
               subject="Thank you for contacting the page",
               message=f""" 
               Hi  {name} , this is an welcome message from manasa ,we'll get what your looking from me as soon as possible, thank you for contacting us.""",
               from_email="manasays2001@gmail.com",
               recipient_list=[email],
               fail_silently=True
            )
            send_mail(
               subject="New user enquiry",
               message=f""" 
               Hi  {name} , enquired about {subject} with the message {message} and the email is {email}.""",
               from_email="shreyasms6@gmail.com",
               recipient_list=[email],
               fail_silently=True
            )
            print("mail sent successfully")
      return render(request,"index.html")