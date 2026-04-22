from django.shortcuts import redirect, render
from django.core.mail import send_mail
import random


def home(request):
    return render(request, "index.html")


def display(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        otp = random.randint(1000, 9999)
        print("Generated OTP:", otp)
        request.session['otp'] = otp
        request.session['contact_email'] = email

        if email:
            send_mail(
                subject="Your OTP - Thank you for contacting us",
                message=f"Hi {name}, thank you for reaching out. Your OTP is {otp}. Please use it to verify your submission.",
                from_email="manasa.srikath.mails@gmail.com",
                recipient_list=[email],  
                fail_silently=False,     
            )
            # Notify admin separately
            send_mail(
                subject="New user enquiry",
                message=f"Hi, {name} enquired about {subject} with the message: {message}. Email: {email}.",
                from_email="manasa.srikath.mails@gmail.com",
                recipient_list=["manasa.srikath.mails@gmail.com"],
                fail_silently=True,
            )
            print("Mail sent successfully to:", email)
            return redirect("verify_otp")


def verify_otp(request):
    email = request.session.get('contact_email', '')
    show_regen = request.GET.get('regen') == '1'
    edit_email = request.GET.get('edit') == '1'

    if request.method == "POST":
        entered_otp = request.POST.get('verify_otp', '').strip()
        generated_otp = request.session.get('otp')

        if str(entered_otp) == str(generated_otp):
            request.session.flush()
            return redirect('home')
        else:
            return render(request, "display.html", {
                "email": email,
                "error": "Invalid OTP. Please try again.",
                "show_regen": show_regen,
                "edit_email": edit_email,
            })

    return render(request, "display.html", {
        "email": email,
        "show_regen": show_regen,
        "edit_email": edit_email,
    })


def regenerate_otp(request):
    if request.method == "POST":
        email = request.POST.get('email', '').strip() or request.session.get('contact_email', '')

        if not email:
            return redirect('verify_otp')

        # Generate new OTP
        otp = random.randint(1000, 9999)
        print("Regenerated OTP:", otp)

        request.session['otp'] = otp
        request.session['contact_email'] = email
        request.session.modified = True  

        # Send new OTP to the (possibly updated) email
        try:
            send_mail(
                subject="Your New OTP",
                message=f"Hi, your new OTP is {otp}. Please use it to verify your submission.",
                from_email="manasa.srikath.mails@gmail.com",
                recipient_list=[email],
                fail_silently=False,  
            )
            print("Regenerated OTP sent successfully to:", email)
        except Exception as e:
            print("Error sending regenerated OTP:", e)

        return redirect('verify_otp')

    return redirect('verify_otp')


def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        if email:
            send_mail(
                subject="Thank you for contacting the page",
                message=f"Hi {name}, thank you for contacting us. We'll get back to you soon.",
                from_email="manasa.srikath.mails@gmail.com",
                recipient_list=[email],
                fail_silently=True,
            )
            print("mail sent successfully")
    return render(request, "index.html")