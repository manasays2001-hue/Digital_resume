from django.shortcuts import render
from django.core.mail import send_mail
import random


# Create your views here.
def home(request):
     
      return render(request, "index.html")

   

def display(request):
    if request.method == "POST":
        email = request.POST.get('email')   # get email from form

        otp = random.randint(1000, 9999)    # better OTP range

        # store OTP in session
        request.session['generated_otp'] = str(otp)
        request.session['email'] = email
        del request.session['generated_otp']

        # send OTP to email
        send_mail(
            subject="Your OTP Verification Code",
            message=f"Your OTP is: {otp}",
            from_email="your_email@gmail.com",
            recipient_list=[email],
            fail_silently=False
        )

        return render(request, "display.html")

    return render(request, "display.html")
          
def verify_otp(request):
    if request.method == "POST":
        user_otp = request.POST.get('verify_otp')
        generated_otp = request.session.get('generated_otp')

        if user_otp == generated_otp:
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
               from_email="mailtomanasays2001@gmail.com",
               recipient_list=[email],
               fail_silently=True
            )
            send_mail(
               subject="New user enquiry",
               message=f""" 
               Hi  {name} , enquired about {subject} with the message {message} and the email is {email}.""",
               from_email="mailtocontact@gmail.com",
               recipient_list=[email],
               fail_silently=True
            )
            print("mail sent successfully")
      return render(request,"index.html")