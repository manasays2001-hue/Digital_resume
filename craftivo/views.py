from django.shortcuts import render

# Create your views here.
def home(request):
     
      return render(request, "index.html")

   

def display(request):
  
    if request.method == "POST":
        print("you have submitted the form")
    
    import random
    otp=random.randrange(1234,2345)

    print(otp)
    return render(request,"display.html",{'generated_otp':otp})
          
def verify_otp(request):
    if request.method == "POST":
     verify_OTP=request.POST['verify_otp']
     generated_otp=request.POST['otp']
     if generated_otp == verify_OTP:
      print('OTP is valid')
      return render(request,"index.html")
     else :
       print("not a valid input")
       return render(request,"display.html")