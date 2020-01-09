from django.shortcuts import render
from .models import Question,CustomUser,Event
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, get_object_or_404,render
from .forms import CustomUserCreationForm,ReplyForm,SignUpForm
from django.shortcuts import redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

from django.utils import timezone
import datetime
from django.utils.timezone import utc

#predict profanity
from profanity_check import predict, predict_prob
import re

# for email activation link
# from django.contrib.sites.shortcuts import get_current_site
# from django.utils.encoding import force_bytes
# from django.utils.http import urlsafe_base64_encode
# from django.template.loader import render_to_string
# from .forms import SignUpForm
# from .tokens import account_activation_token
# from django.core.mail import send_mail
# from django.utils.encoding import force_text
# from inquest import settings as sett
# from django.utils.http import urlsafe_base64_decode


#remove digits
def remove(word):
    pattern = '[0-9!@#$%^&*(),.?":{}|<>_=;`~+-]'
    word = [re.sub(pattern, '', word)]
    return word




def question(request):
    event=Event.objects.get(id=1)
    timenow=timezone.now()
    eventtime = event.event_start
    eventend = event.event_end
    if (timenow>eventend):
        message="Thank you all"
        return render('welcome.html',{'message':message})
    else:
        if timenow>eventtime and timenow<eventend:
            if request.user.is_anonymous:
                return redirect('../signup/')
            t=int(request.user.id)
            user=CustomUser.objects.get(id=t)
            if request.method == "POST":
                score=(request.user.score)
                question = get_object_or_404(Question, pk=str((user.score)+1))
                user_answer=request.POST.get('answer')
                flag=0
                ans=str(user_answer)
                ans=ans.lower()
                ans=ans.replace(" ","")
                if(str(ans)==str(question.answer)):
                    user.score+=1
                    timenow=timezone.now()
                    user.last_updated=timenow
                    user.save()
                    user.publish()
                    flag=1
                if flag==0:
                    form=ReplyForm()
                    score=user.score
                    question = get_object_or_404(Question, pk=str((user.score)+1))
                    n=score
                    flash="Try Harder"
                    level=int(user.score)+1
                    return render(request,'question.html',{'question': question,'form':form,'n':n,'flash':flash,'level':level})
                else:
                    form=ReplyForm()
                    score=user.score
                    question = get_object_or_404(Question, pk=str((user.score)+1))
                    n=score
                    flash="Correct Answer"
                    level=int(user.score)+1
                    return render(request,'question.html',{'question': question,'form':form,'n':n,'flash':flash,'level':level})
            else:
                level=int(user.score)+1
                form=ReplyForm()
                score=user.score
                question = get_object_or_404(Question, pk=str((user.score)+1))
                n=score
                return render(request,'question.html',{'question': question,'form':form,'n':n,'level':level})
        else:
            return redirect('home')


def home(request):
    timenow = timezone.now() 
    event=Event.objects.get(id=1)
    eventtime=(event.event_start)
    eventend=(event.event_end)
    timeleft=eventtime-timenow
    timeleft=timeleft.total_seconds()   #  timeleft in seconds
    timeleft=int(timeleft)
    if timenow < eventtime:
        #pass timeleft
        message="welcome"
        timeleft = (eventtime-timenow).total_seconds()
        timeleft =int(timeleft)
        return render(request,'welcome.html',{'message':message,'timeleft':timeleft})
    elif timenow>eventtime and timenow<eventend:
        #game is live
        timeleft = eventend-timenow
        message="game is live"
        return render(request,'welcome.html',{'message':message})
    else:
        message="Thank you"
        return render(request,'welcome.html',{'message':message})


# def test(request):
#     t=int(request.user.id)
#     user=CustomUser.objects.get(id=t)
#     score=user.score
#     return HttpResponse(str(score)+" "+str(CustomUser.objects.filter(score__gt=score).count()))


def leaderboard(request):
    participants = CustomUser.objects.filter().order_by('-score','last_updated')
    return render(request, 'leaderboard.html', {'participants': participants},)

def profile(request):
    return render(request,'profile.html')

def contact(request):
    return render(request,'contact.html')

def logoutred(request):
    return render(request, 'registration/login.html', {},)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            uname = remove(user.username)
            print(uname)
            print(predict(uname))
            if(predict(uname) == 1):
                message="No offensive language in username!!"
                return render(request,'signup.html',{'message':message})
            else:
                if request.user.is_anonymous:
                    user.save()
                    user.is_active = True
                    user.email_confirmed = True
                    user.last_updated = timezone.now()
                    user.save()
                    message="Registered !"
                    return render(request,'registration/login.html',{'message':message})
                else:
                    message="You are logged in already"
                    return render(request,'signup.html',{'message':message})
        else:
            message="Password didnot match"
            return render(request,'signup.html',{'message':message})
    else:
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form,})



def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return redirect('home')
            else:
                return HttpResponse("Your account was inactive. Contact Admin")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            message="Invalid login details given"
            return render(request,'registration/login.html',{'message':message})
    else:
        return render(request,'registration/login.html',{})
