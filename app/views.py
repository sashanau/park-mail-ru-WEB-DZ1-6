import django.db.utils
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.forms import model_to_dict
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.urls import reverse
from django.views.decorators.http import require_POST

from app.models import Question, Answer, Profile, User, Tag, Likes
from django.http import Http404, JsonResponse, HttpResponseRedirect
from app.forms import LoginForm, RegistrationForm, AskForm, AnswerForm


@login_required(login_url='/login/')
def ask(request):
    user = get_user(request)
    form = AskForm()
    if request.method == 'GET':
        form = AskForm()
    elif request.method == 'POST':
        form = AskForm(data=request.POST)
        if form.is_valid():
            user_data = User.objects.get(id=request.user.id) #в форму
            profile = Profile.objects.get(user=user_data)
            ques = Question(title=form.cleaned_data['title'], context=form.cleaned_data['context'],
                            author=profile)
            ques.save()
            tags = form.cleaned_data['tags'].split(",")
            for tag in tags:
                tag = (str(tag)).replace(' ', '')
                new_tag = Tag(name=tag)
                new_tag.save()
                ques.tags.add(new_tag)
                ques.save()
            return redirect(reverse('index'))
    return render(request, "ask.html", {'form': form, 'user': user})


def login(request):
    auth.logout(request)
    form = LoginForm()
    if request.method == 'GET':
        form = LoginForm()
    elif request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(**form.cleaned_data)
            if not user:
                form.add_error(None, "Пользователь askemeNaumenko не найден!")
            else:
                auth.login(request, user)
                return redirect(reverse('index'))
    user_tmp = get_user(request)
    return render(request, "login.html", {'form': form, 'user': user_tmp})


def pagination(request, index, count):
    paginator = Paginator(index, count)
    page = request.GET.get('page')
    content = paginator.get_page(page)
    return content


def index(request):
    user = get_user(request)
    return render(request, "index.html",
                  {'list_index': pagination(request, Question.manager.new_questions(), 3), 'tag': 'New Questions',
                   'sub_tag': 'Hot Questions', 'user': user})


def hot(request):
    user = get_user(request)
    return render(request, "hot.html",
                  {'list_index': pagination(request, Question.manager.hot_questions(), 3), 'tag': 'Hot', 'user': user})


def tag(request, tag_name):
    user = get_user(request)
    if tag_name is None:
        raise Http404()
    return render(request, "hot.html",
                  {'list_index': pagination(request, Question.manager.get_tag(tag_name), 3), 'tag': tag_name,
                   'user': user})


def register(request):
    user = get_user(request)
    form = RegistrationForm()
    if request.method == 'GET':
        form = RegistrationForm()
    elif request.method == 'POST':
        form = RegistrationForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            try:
                user = User.objects.create_user(username=form.cleaned_data['username'],
                                                password=form.cleaned_data['password_repeat'],
                                                email=form.cleaned_data['email'])
            except django.db.utils.IntegrityError:
                form.add_error(None, "The user exists!")
                return render(request, "register.html", {'form': form, 'user': user})
            user.save()
            profile = Profile(user=user, avatar=form.cleaned_data['avatar'])
            profile.save()
            return redirect(reverse('login'))
    return render(request, "register.html", {'form': form, 'user': user})


@login_required(login_url='/login/')
def settings(request):
    user = get_user(request)
    form = RegistrationForm()
    if request.method == 'GET':
        initial_data = model_to_dict(request.user)
        initial_data['avatar'] = request.user.userprofile.avatar
        form = RegistrationForm(initial=initial_data)
    elif request.method == 'POST':
        form = RegistrationForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            user_data = User.objects.get(id=request.user.id)
            user_data.username = form.cleaned_data['username']
            user_data.email = form.cleaned_data['email']
            user_data.set_password(form.cleaned_data['password_repeat'])
            user_data.save()
            data_profile = Profile.objects.get(user=user_data)
            data_profile.avatar = form.cleaned_data['avatar']
            data_profile.save()
            return redirect(reverse('login'))
    return render(request, "settings.html", {'form': form, 'user': user})


@login_required(login_url='/login/')
def question(request, number):
    if number > Question.manager.get_count() or number is None:
        raise Http404()
    question_id = Question.manager.get_questions(number)
    answers_id = Answer.manager.get_answer(question_id)
    if request.method == 'GET':
        form = AnswerForm()
    elif request.method == 'POST':
        user_data = User.objects.get(id=request.user.id)
        profile = Profile.objects.get(user=user_data)
        form = AnswerForm(data=request.POST)
        if form.is_valid():
            question_id.answer = question_id.answer + 1
            question_id.save()
            ans = Answer(context=form.cleaned_data['context'], author=profile, question=question_id)
            ans.save()
    return render(request, "question.html",
                  {'question': question_id, 'list_index': pagination(request, answers_id, 2),
                   'user': get_user(request), 'form': form, 'number': number})


def get_user(request):
    user = None
    try:
        if request.user.is_authenticated:
            user = request.user
    except ValueError:
        pass
    return user


@login_required(login_url='/login/')
@require_POST
def vote(request):
    questions = Question.manager.get_questions(request.POST['id'])
    if check(request, request.POST.get('flag'), questions):
        return JsonResponse({'rating': questions.rating_num})
    return JsonResponse({'rating': questions.rating_num})


@login_required(login_url='/login/')
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/?continue=logout')


def check(request, flag, questions):
    prof = Profile.objects.get(user=request.user) #в форму
    try:
        Likes.objects.get(id_question=questions, id_user=prof)
        return False
    except ObjectDoesNotExist:
        if flag == '1':
            questions.rating_num += 1
            questions.save()
        else:
            if questions.rating_num > 0:
                questions.rating_num -= 1
                questions.save()
        like = Likes(id_question=questions, id_user=prof)
        like.save()
        return True


@login_required(login_url='/login/')
@require_POST
def is_correct(request):
    ans_id = request.POST['id_ans']
    ques_id = request.POST['id_ques']
    answer = Answer.manager.get_answer_for_id(ans_id)
    question_data = Question.manager.get_questions(ques_id)
    if question_data.author.user.id == request.user.id:
        answer.is_correct = not answer.is_correct
        answer.save()
        return JsonResponse({'status': "ok"})
    else:
        return JsonResponse({'status': "fail"})
