import json

from django.conf import settings
from django.contrib.auth.decorators import login_required  #
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import *
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


# Create your views here.
def home(request):
    # to check if the user has signed in or not

    if request.user.is_authenticated:
        df = DanceForms.objects.all()

        # this will allow the user to access the course only if the payment is done
        # check if there is any payment done by the user, if so it will show purchased or not the buy button
        try:
            pd = PaymentDetails.objects.get(user=request.user)
            # fetch the courses that the user has subscribed

            courses = list(
                # since this is a many-to-many field we use course.all(), we are converting it as list
                pd.course.all().values_list('id', flat=True))  # flattening the dimension since we got a tuple

            print(courses)  # debugging

        except:
            courses = ''

    else:
        df = DanceForms.objects.all()
        courses = ''

    return render(request, 'home.html', {'d': df, 'sc': courses})


def register_fn(request):
    if request.method == 'POST':
        fn = request.POST['fn']
        ln = request.POST['ln']
        em = request.POST['em']
        mb = request.POST['mb']
        gn = request.POST['gn']
        pw1 = request.POST['pw']
        pw2 = request.POST['cp']

        if User.objects.filter(username=em).exists():  # if user exists the condition will be true
            print("Email already taken")
        else:
            if pw1 == pw2:
                u = User.objects.create_user(username=em, first_name=fn, last_name=ln, password=pw1, email=em)
                u.save()
                r = Register(user=u, phone=mb, gender=gn)
                r.save()
                return redirect('/')
            else:
                print("Password not matching")
    return render(request, 'register.html')


# logged in user
def dynamic_user(a):
    #
    if PaymentDetails.objects.filter(user=a).exists():
        pd = PaymentDetails.objects.filter(user=a)
        return pd
    else:
        return None


# Login Function
def login_function(request):
    if request.method == 'POST':
        un = request.POST['em']
        pw = request.POST['pw']
        user = authenticate(username=un, password=pw)
        if user is not None:
            login(request, user)
            print("Logged in successfully..!!")

            du = dynamic_user(user)
            if du is not None:
                return redirect('ld')
            else:
                return redirect('/')
        else:
            print("Invalid Credentials")

    return render(request, 'login.html')


# Logout Function
def Logout_function(request):
    logout(request)
    return redirect('/')


def forgot_password(request):
    if request.method == "POST":
        em = request.POST['un']
        if User.objects.filter(username=em).exists():
            return redirect('cp', p=em)
        else:
            print("Invalid Username")
    return render(request, 'forgot.html')


def change_password(request, p):
    a = User.objects.get(username=p)
    print(a)
    if request.method == "POST":
        pw = request.POST["pw1"]

        a.set_password(pw)
        a.save()
        print(pw)
        print("Password changed!")
        return redirect("/")
    return render(request, 'change_pw.html')


@login_required(login_url='login')
def tutorial_fn(request, i):
    tut = Tutorials.objects.filter(dance_forms=i)
    df = DanceForms.objects.get(id=i)
    total_videos = len(tut)
    print(total_videos)
    try:
        progress = 100 / total_videos
        tv = TutorialProgress.objects.filter(user=request.user, course=df)
        total_watched_videos = len(tv)
        total_progress = total_watched_videos * progress
        print(total_progress)
    except:
        total_progress = 0
    print(df.name)
    return render(request, 'tutorial.html', {"ts": tut, "df": df, 'tp': total_progress})


@login_required(login_url='login')
def watch_fn(request, vdo):
    df = Tutorials.objects.get(id=vdo)
    return render(request, 'watch_tutorial.html', {'k': df})


@login_required(login_url='login')
def buy_course(request, d):
    cs = DanceForms.objects.get(id=d)
    return render(request, 'buy_course.html', {'b': cs})


@login_required(login_url='login')
def subscription(request):
    try:

        pd = PaymentDetails.objects.get(user=request.user)
        courses = list(pd.course.all().values_list('id', flat=True))  # to get the id of the danceforms
        print(courses)
    except:
        courses = ''
    subscribe = DanceForms.objects.exclude(
        id__in=courses)  # to exclude the already purchased course from the subscription page

    return render(request, 'subscription.html', {'s': subscribe})


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from .models import DanceForms  # Replace with your actual model
import json

amt = 0
course_keys = ''


@csrf_exempt
def calculate_total(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            primary_keys = data.get("primary_keys", [])

            # Convert primary keys to integers
            global course_keys
            primary_keys = list(map(int, primary_keys))
            course_keys = primary_keys

            print("Received primary keys:", primary_keys)  # Debugging line

            total_amount = DanceForms.objects.filter(id__in=primary_keys).aggregate(total=Sum('fees'))['total'] or 0
            global amt
            amt = total_amount
            print("Calculated total amount:", total_amount)  # Debugging line

            return JsonResponse({"total_amount": total_amount})
        except Exception as e:
            print("Error in calculate_total view:", str(e))  # Debugging line
            return JsonResponse({"error": str(e)}, status=400)


@login_required(login_url='login')
def final_amount(request):
    global amt, course_keys
    if request.method == 'POST':
        amoun = request.POST["hn"]
        print(amoun)
        print(course_keys)
        # to check if there is any object in the name of user - store in pc flag will be false.
        # if we create object the flag will be true
        # id__in - to pass a list

        pc, flag = PaymentDetails.objects.get_or_create(user=request.user)
        print(pc, flag)

        #
        df = DanceForms.objects.filter(id__in=course_keys)
        payment_amt = PaymentAmount(user=request.user, amount=amoun)
        payment_amt.save()
        pc.amount.add(payment_amt)
        pc.course.add(*df)  # arbitrary argument
        pc.save()

        # for showing the list of courses in email

        list1 = [i for i in DanceForms.objects.filter(id__in=course_keys).values_list('name', flat=True)]
        s = ' , '.join(list1)

        #################################### Emails ####################################################

        subject = 'Order Confirmation'

        message = render_to_string('emailtemp.html',
                                   {'name': request.user.first_name,
                                    'sd': payment_amt.start_date, 'amt': payment_amt.amount, 'cr': s,
                                    })
        email = EmailMessage(
            subject, message, to=[request.user.email]
        )
        email.content_subtype = 'html'
        email.send()
        #################################### end ####################################################
        amt = 0
        course_keys = ''

        # for i in course_keys:
        #     df = DanceForms.objects.get(id=i)
        #     pd.course.add(df)
        #     pd.save()

        return redirect("/")

    return render(request, 'final_payment.html', {'at': amt})


def card_select(request):
    m = request.GET.get('card')
    print(m)
    saved_card = Card_Details.objects.get(id=m)
    return render(request, 'card_dynamic.html', {'card': saved_card})


@login_required(login_url='login')
def payment_pg(request):
    card = Card_Details.objects.filter(user=request.user)
    if request.method == "POST":
        a = request.user
        print(a)
        user = User.objects.get(username=a)
        print(user)

        number = request.POST['cn']
        print(number)
        month = request.POST['em']
        print(month)
        year = request.POST['ey']
        print(year)
        if Card_Details.objects.filter(card_no=number, user=user).exists():
            print("Card exists")
            return redirect('fp')
        else:

            c = Card_Details(user=user, card_no=number, Exp_month=month, Exp_year=year)
            c.save()
            print("Card saved successfully")
            return redirect('fp')
    else:
        print(" not working")

    return render(request, 'payment.html', {'c': card})


def login_dynamic(request):
    pd = PaymentDetails.objects.get(user=request.user)
    courses = pd.course.all()
    print("Chooses courses === ", courses)

    return render(request, 'login_dynamic.html', {'cr': courses})


from django.http import JsonResponse

import logging

logger = logging.getLogger(__name__)


@csrf_exempt
def video_completed(request):
    if request.method == 'POST':
        try:

            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            print(body_unicode)
            print(body)
            # get by name

            video_id = body.get('video_id')
            print("helooooo", video_id)
            t = Tutorials.objects.get(id=video_id)
            print("Tutorial = ", t)

            d = t.dance_forms
            print("dance form = ", d)
            if TutorialProgress.objects.filter(user=request.user, course=d, tutorial=t).exists():
                pass
                return redirect('tt', i=d.id)
            else:
                prog = TutorialProgress(user=request.user, course=d, tutorial=t)
                prog.save()
                return redirect('tt', i=d.id)

            # Example processing logic (uncomment as needed)
            # t = Tutorials.objects.get(id=video_id)
            # d = t.dance_forms.id
            # print(d)
            # Redirect to the 'tt' view with parameter i=

        except Exception as e:
            logger.error(f'Error processing video completion: {e}')
            return JsonResponse({'error': 'Internal server error'}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)


from django.template.loader import render_to_string

from django.http import HttpResponse

from dateutil.relativedelta import relativedelta
from fpdf import FPDF

from datetime import datetime

# Get current date and time
current_datetime = datetime.now()

# Format the date and time as a string (optional)
current_datetime_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

print("Current date and time:", current_datetime_str)


def generate_certificate(request, id):
    start_date = PaymentAmount.objects.filter(user=request.user).first().start_date
    print(start_date)
    end_date = TutorialProgress.objects.filter(user=request.user, course__id=id).first().end_date
    delta = relativedelta(end_date, start_date)
    days = (end_date - start_date).days
    months = delta.months + (delta.years * 12)
    # Example data (replace with your actual data)
    recipient_name = f"{request.user.first_name} {request.user.last_name}"
    course_name = f"{DanceForms.objects.get(id=id).name}"
    course_duration = months
    place = 'Kochi, India'

    # Initialize PDF object
    pdf = FPDF()
    pdf.add_page()

    # Set font for header
    pdf.set_font("Times", size=16)

    # Add background image (assuming it covers the whole page)
    pdf.image(r'C:\Users\kuttu\e_learning_folder\e_learning_project\static\images\back.png', x=0, y=0, w=210,
              h=297)  # Adjust dimensions as needed

    pdf.set_xy(0, 50)
    pdf.multi_cell(210, 20, "Nritta Dance Academy", 0, 'C')
    # Add logo image at the top center
    pdf.image(r'C:\Users\kuttu\e_learning_folder\e_learning_project\static\images\mynewlogo.png', x=70, y=20, w=70)

    # Add heading "Course Certificate"
    pdf.set_xy(0, 80)  # Adjust position for the heading
    pdf.set_font("Arial", size=20)
    pdf.multi_cell(210, 20, "Course Certificate", 0, 'C')

    # Set font for content
    pdf.set_font("Times", "I", size=12)

    # Add recipient details with left and right margins
    pdf.ln(15)  # Move down before adding recipient details
    recipient_details = (
        f"We are proud to announce that Mr./Ms. {recipient_name} has successfully completed the "
        f"{course_name} at Nritta Dance Academy. This intensive course, spanning {course_duration} months, "
        f"has showcased your dedication, skill, and passion for dance. We commend your outstanding "
        f"efforts and achievements throughout the program. We wish you all the best for your future "
        f"endeavors and are confident that you will continue to shine in your dance journey."
    )
    margin_left = 20
    margin_right = 20
    page_width = 210
    pdf.set_x(margin_left)
    pdf.multi_cell(page_width - margin_left - margin_right, 10, recipient_details, 0, 'J')  # Justify the text
    pdf.ln(10)

    # Add company seal at bottom left (adjusted position)
    pdf.image(r'C:\Users\kuttu\e_learning_folder\e_learning_project\static\images\nritta_badge.jpg', x=20, y=190, w=50)

    # Add place and date at bottom right (adjusted position)
    pdf.set_xy(150, 200)  # Adjust position for place and date
    pdf.multi_cell(0, 10, f"Place: {place}", 0, 'R')
    pdf.set_xy(110, 210)
    pdf.multi_cell(0, 10, f"Issue Date: {current_datetime_str}", 0, 'R')

    # Output PDF as bytes
    pdf_bytes = pdf.output(dest='S').encode('latin1')

    # Create HTTP response with PDF as attachment for download
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'

    return response
