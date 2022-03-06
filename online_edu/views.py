from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render
from django.urls import reverse
import markdown2
from django import forms
from .models import User, Notes, Category, Course, Profile, Comment 
import datetime
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.paginator import Paginator
import time

notes_category=(
    ('Computer Science','Computer Science'),
    ('Social Science','Social Science'),
    ('History','History'),
    ('Economics','Economics'),
    ('Business Studies','Business Studies'),
    ('Law','Law'),
    ('Biology','Biology'),
    ('Chemistry','Chemistry'),
    ('Physics','Physics'),
    ('Engineering','Engineering'),
    ('Fashion Designing','Fashion Designing')


)

class UploadNotes(forms.ModelForm):
    class Meta:
        model=Notes
        fields=['title','course','category','additional_category','description','thumbnail','video_iframe','markdown_notes_content']

class CreateCourse(forms.ModelForm):
    class Meta:
        model=Course
        fields=['course_name','course_category','course_description','course_thumbnail']

def index(request):
    all_courses=Course.objects.all()[::-1]
    len_a_c=len(all_courses)
    paginator=Paginator(all_courses,9)
    page_number=request.GET.get('page')
    all_courses=paginator.get_page(page_number)
    return render(request,"online_edu/index.html",{
        "all_courses":all_courses,
        "len_a_c":len_a_c
    })

def create_course(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    if request.user.lecturer==False:
        return HttpResponseRedirect(reverse('index'))
    form0=CreateCourse()
    form0.fields['course_category'].queryset=Category.objects.all().order_by('category_name')
    if request.method=="POST":
        form=CreateCourse(request.POST)
        if form.is_valid():
            course_name=form.cleaned_data['course_name']
            course_description=form.cleaned_data['course_description']
            course_category=form.cleaned_data['course_category']
            course_thumbnail=form.cleaned_data['course_thumbnail']
            creator=request.user
            course_date=datetime.datetime.now()
            print(Course.objects.filter(creator=request.user))
            for course in Course.objects.filter(creator=request.user):
                if course_name==course.course_name:
                    return render(request,"online_edu/create_course.html",{
                        "form":form,
                        "message":"You already have a course with the same name!"
                    })
                    break
            course=Course(course_category=course_category,course_date=course_date,course_description=course_description,course_name=course_name,course_thumbnail=course_thumbnail,creator=creator)
            course.save()
            return HttpResponseRedirect(reverse('course_view',args=[course.creator.username,course.course_name]))

        else:
            return render(request,"online_edu/create_course.html",{
                "form":form
            })
    return render(request,"online_edu/create_course.html",{
        "form":form0
    })

def upload_notes(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    if request.user.lecturer==False:
        return HttpResponseRedirect(reverse('index'))
    form0=UploadNotes()
    form0.fields['course'].queryset=Course.objects.filter(creator=request.user).order_by('-course_date')
    form0.fields['category'].queryset=Category.objects.all().order_by('category_name')
    if request.method=="POST":
        form=UploadNotes(request.POST)
        if form.is_valid():
            title=form.cleaned_data['title']
            course=form.cleaned_data['course']
            thumbnail=form.cleaned_data['thumbnail']
            category=form.cleaned_data['category']
            additional_category=form.cleaned_data['additional_category']
            description=form.cleaned_data['description']
            markdown_notes_content=form.cleaned_data['markdown_notes_content']
            html_notes_content=markdown2.markdown(form.cleaned_data['markdown_notes_content'])
            video_iframe=form.cleaned_data['video_iframe'] 
            date=datetime.datetime.now()
            creator=request.user
            notes=Notes(title=title,course=course,markdown_notes_content=markdown_notes_content,date=date, creator=creator, html_notes_content=html_notes_content,video_iframe=video_iframe,thumbnail=thumbnail,category=category,additional_category=additional_category,description=description)
            notes.save()
            return HttpResponseRedirect(reverse('note_view',args=[notes.id]))
        else:
            return render(request,"online_edu/upload_notes.html",{
                "form":form
            }) 
    return render(request,"online_edu/upload_notes.html",{
        "form":form0,
    })


def search(request):
    search_entry=request.GET.get('q','')
    all_courses=Course.objects.all()
    all_notes=Notes.objects.all()
    all_lecturers=User.objects.filter(lecturer=True)
    related_courses=[]
    all_categories=Category.objects.all()
    for category in all_categories:
        if search_entry.lower() in category.category_name.lower():
            for course in Course.objects.filter(course_category=category):
                related_courses.append(course)
            for note in Notes.objects.filter(category=category):
                related_courses.append(note.course)

    for course in all_courses:
        if search_entry.lower() in course.course_name.lower():
            related_courses.append(course)
    for note in all_notes:
        if search_entry.lower() in note.additional_category.lower() or search_entry.lower() in note.title.lower():
            related_courses.append(note.course)

    for lecturer in all_lecturers:
        if search_entry.lower() in lecturer.username.lower():
            for course in Course.objects.filter(creator=lecturer):
                related_courses.append(course)

    return render(request,"online_edu/search.html",{
        "related_courses":set(related_courses),
        "search_entry":search_entry
    })


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "online_edu/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "online_edu/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "online_edu/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            profile=Profile(person=user)
            profile.save()
        except IntegrityError:
            return render(request, "online_edu/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "online_edu/register.html")

def note_view(request,id):
    note=Notes.objects.get(pk=id)
    has_liked=False
    if request.user in note.like.all():
        has_liked=True
    categories=Category.objects.all().order_by('category_name')
    courses_by_this_user=Course.objects.filter(creator=note.creator).order_by('-course_date')
    return render(request,"online_edu/note_view.html",{
        "note":note,
        "categories":categories,
        "courses_by_this_user":courses_by_this_user,
        "has_liked":has_liked,
        "comments":Comment.objects.filter(note_commented=note)[::-1],
    })


@csrf_exempt
def edit_note(request,id):
    note=Notes.objects.get(pk=id)
    user=User.objects.get(username=request.user)
    if request.method=="POST":
        data = json.loads(request.body)
        if data['title'].strip()=="":
            title=note.title
        else:
            title=data['title']
        if data['desc'].strip()=="":
            description=note.description
        else:
            description=data['desc']
        thumbnail=data['t_url']
        additional_category=data['a_category']
        if data['content'].strip()=="":
            markdown_notes_content=note.markdown_notes_content
        else:
            markdown_notes_content=data['content']
        html_notes_content=markdown2.markdown(markdown_notes_content)
        video_iframe=data['v_iframe']
        category=Category.objects.get(category_name=data['category'])
        courses_by_creator=Course.objects.filter(creator=note.creator)
        course=courses_by_creator.get(course_name=data['course'])
        note.title=title
        note.markdown_notes_content=markdown_notes_content
        note.html_notes_content=html_notes_content
        note.video_iframe=video_iframe
        note.thumbnail=thumbnail
        note.category=category
        note.additional_category=additional_category
        note.description=description
        note.course=course
        note.save()
        return JsonResponse({'status':200})

@csrf_exempt
def delete_note(request,id):
    note=Notes.objects.get(pk=id)
    if request.method=="POST":
        data = json.loads(request.body)
        if data['to_delete']=="yes":
            note.delete()
            return JsonResponse({'status':200})
@csrf_exempt
def delete_course(request,lecturer,course):
    lecturer=User.objects.get(username=lecturer)
    course_filter=Course.objects.filter(creator=lecturer)
    course=course_filter.get(course_name=course)
    if request.method=="POST":
        data = json.loads(request.body)
        if data['to_delete']=="yes":
            course.delete()
            return JsonResponse({'status':200})

def course_view(request,lecturer,course):
    lecturer=User.objects.get(username=lecturer)
    course_filter=Course.objects.filter(creator=lecturer)
    course=course_filter.get(course_name=course)
    print(course)
    categories=Category.objects.all().order_by('category_name')
    has_subscribed=False
    if request.user in course.subscribed_users.all():
        has_subscribed=True
    return render(request,"online_edu/course_view.html",{
        "course":course,
        "categories":categories,
        "has_subscribed":has_subscribed
    })

@csrf_exempt
def edit_course(request,lecturer,course):
    lecturer=User.objects.get(username=lecturer)
    course_filter=Course.objects.filter(creator=lecturer)
    course=course_filter.get(course_name=course)
    course_titles=[]
    for course_title in course_filter:
        if course_title!=course:
            course_titles.append(course_title.course_name)
    if request.method=="POST":
        data = json.loads(request.body)
        if data['cc'].strip()=="":
            course_category=None
        else:
            course_category=Category.objects.get(category_name=data['cc'])
        if data['cn'].strip()=="":
            course_name=course.course_name
        else:
            course_name=data['cn']
        if data['cd'].strip()=="":
            course_description=course.course_description
        else: 
            course_description=data['cd']
        if data['ct'].strip()=="":
            course_thumbnail=course.course_thumbnail
        else: 
            course_thumbnail=data['ct']

        course.course_category=course_category
        course.course_description=course_description
        course.course_thumbnail=course_thumbnail
        course.save()
        if course_name in course_titles:
            return JsonResponse({'status':300})

        elif course_name==course.course_name:
            return JsonResponse({'status':150})

        else:
            course.course_name=course_name
            course.save()
            return JsonResponse({'status':200})

@csrf_exempt
def post_comment(request,id):
    note=Notes.objects.get(pk=id)
    user=User.objects.get(username=request.user)
    if request.method=="POST":
        data = json.loads(request.body)

        if data['com_con'].strip()!="":
            comment=Comment(time_of_comment=datetime.datetime.now(),comment=data['com_con'],commenter=request.user,note_commented=note)
            comment.save()
            print(datetime.datetime.now())
            return JsonResponse({'status':200})
        else:
            return JsonResponse({'status':300})

def comments(request,id):
    start = int(request.GET.get("start") or 0)
    end = int(request.GET.get("end") or (start + 9))
    note=Notes.objects.get(pk=id)
    print(note.title)
    comments_deets = []
    comments=[]
    comments_filter=Comment.objects.filter(note_commented=note).values()[::-1]
    for comment in comments_filter:
        comments_deets.append(dict(id=comment["id"],time_of_comment=comment["time_of_comment"].strftime("%b %d, %Y, %I:%M%p"),comment=comment["comment"],commenter=User.objects.get(pk=comment["commenter_id"]).username,note_commented=note.title))
    print(comments_deets)
    if end>len(comments_deets):
        end=len(comments_deets)-1
    print(end)
    for i in range(start, end + 1):
        comments.append(comments_deets[i])
    time.sleep(1)

    return JsonResponse({
        "comments": list(comments)
    })


def profile_view(request,username):
    profile=User.objects.get(username=username)
    courses_by_this_user=Course.objects.filter(creator=profile)[::-1]
    notes_by_this_user=Notes.objects.filter(creator=profile)
    follower_following=Profile.objects.get(person=profile)
    total_subscribers=[]
    total_likes=[]
    for course in courses_by_this_user:
        total_subscribers.append(course.subscribed_users.all().count())

    for note in notes_by_this_user:
        total_likes.append(note.like.all().count())

    is_follow=False
    if request.user in follower_following.follower.all():
        is_follow=True
    return render(request,"online_edu/profile_view.html", {
        "profile":profile,
        "profile_stats":follower_following,
        "is_follow":is_follow,
        "courses_by_this_user":courses_by_this_user,
        "total_subscribers":sum(total_subscribers),
        "total_likes":sum(total_likes)
    })


def category_list(request):
    return render(request,"online_edu/categories.html",{
        "categories":Category.objects.all().order_by('category_name')
    })

def category_view(request,category_name):
    try: 
        category=Category.objects.get(category_name=category_name)
        courses_in_this_category=Course.objects.filter(course_category=category)
        notes_in_this_category=Notes.objects.filter(category=category)
        courses_related_to_category=[]
        for note in notes_in_this_category:
            courses_related_to_category.append(note.course)
        for course in courses_in_this_category:
            courses_related_to_category.append(course)
        len_c=len(set(courses_related_to_category))
    except Category.DoesNotExist:
        raise Http404(f"'{category_name}' category does not exist!")
    courses_related_to_category=list(set(courses_related_to_category))[::-1]
    paginator = Paginator(courses_related_to_category, 9)
    page_number = request.GET.get('page')
    courses_related_to_category= paginator.get_page(page_number)
    return render(request,"online_edu/category.html",{
        "courses":courses_related_to_category,
        "category":category_name,
        "len_c":len_c
    })

def subscribed_courses(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    subscribed_courses=Course.objects.filter(subscribed_users=request.user)[::-1]
    s_c_c=len(subscribed_courses)
    paginator = Paginator(subscribed_courses, 9)
    page_number = request.GET.get('page')
    subscribed_courses = paginator.get_page(page_number)
    return render(request,"online_edu/subscribed_courses.html",{
        "subscribed_courses":subscribed_courses, 
        "s_c_c":s_c_c
    })

def following_lecturer_courses(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    user=User.objects.get(username=request.user)
    person=Profile.objects.get(person=user)
    lecturers_following=person.following.all()
    all_courses=Course.objects.all()
    f_l_c=[]
    for course in all_courses:
        for lecturer in lecturers_following:
            if lecturer==course.creator:
                f_l_c.append(course)
    print(f_l_c)
    len_f_l_c=len(f_l_c)
    paginator = Paginator(f_l_c[::-1], 9)
    page_number = request.GET.get('page')
    f_l_c = paginator.get_page(page_number)
    return render(request,"online_edu/following_lecturer_courses.html",{
        "f_l_c":f_l_c,
        "len_f_l_c":len_f_l_c
    })


@csrf_exempt
def follow_unfollow(request,username):
    profile=User.objects.get(username=username)
    user=User.objects.get(username=request.user)
    user_id=user.id
    if request.method=="POST":
        data = json.loads(request.body) 
        if data["to_follow"]==True:
            person=Profile.objects.get(person=profile)
            person.follower.add(user)
            person.save()
            user=Profile.objects.get(person=user_id)
            person=User.objects.get(username=profile)
            user.following.add(person)
            user.save()
            return HttpResponse(status=200)
        else:
            person=Profile.objects.get(person=profile)
            person.follower.remove(user)
            person.save()
            user=Profile.objects.get(person=user_id)
            person=User.objects.get(username=profile)
            user.following.remove(person)
            user.save()
            return HttpResponse(status=200)
    elif request.method=="GET":
        return HttpResponse(status=200)

@csrf_exempt
def subscribe_unsubscribe(request,id):
    user=User.objects.get(username=request.user)
    course=Course.objects.get(pk=id)
    if request.method=="POST":
        data = json.loads(request.body) 
        if data["to_subscribe"]==True:
            course.subscribed_users.add(user)
            course.save()
            return HttpResponse(status=200)
        else:
            course.subscribed_users.remove(user)
            course.save()
            return HttpResponse(status=200)
    elif request.method=="GET":
        return HttpResponse(status=200)


@csrf_exempt
def like_unlike(request,id):
    user=User.objects.get(username=request.user)
    note=Notes.objects.get(pk=id)
    if request.method=="POST":
        data = json.loads(request.body) 
        if data["to_like"]==True:
            note.like.add(user)
            note.save()
            return HttpResponse(status=200)
        else:
            note.like.remove(user)
            note.save()
            return HttpResponse(status=200)
    elif request.method=="GET":
        return HttpResponse(status=200)
