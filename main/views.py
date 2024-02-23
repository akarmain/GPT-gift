import datetime
import json

from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.files.storage import FileSystemStorage
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from main.models import *
from .chatGPT import chatGPT
from .forms import RegisterUserForm, LoginUserForm


def get_menu_context():
    return [
        {'url_name': 'index', 'name': 'Главная'},
        {'url_name': 'time', 'name': 'Текущее время'},
        {'url_name': 'user_polls', 'name': 'Мои опросы'},
    ]


def index_page(request: WSGIRequest):
    context = {
        'menu': get_menu_context()
    }
    return render(request, 'pages/index.html', context)


@login_required(login_url="/login")
def time_page(request: WSGIRequest):
    context = {
        'pagename': 'Текущее время',
        'time': datetime.datetime.now().time(),
        'menu': get_menu_context()
    }
    return render(request, 'pages/time.html', context)


def login_page(request: WSGIRequest):
    context = {
        'pagename': 'Текущее время',
        'time': datetime.now().time(),
        'menu': get_menu_context()
    }
    return render(request, 'pages/time.html', context)


@login_required(login_url="/login")
def poll_completion(request: WSGIRequest, poll_slug=0):
    if request.method == "GET":
        context = {
            'poll': Poll.objects.get(slug=poll_slug),
        }

        return render(request, 'pages/poll_completion.html', context)

    elif request.method == "POST":
        print(request.POST)
        poll_text = ""
        for ans in request.POST:
            if ans != "csrfmiddlewaretoken" and ans != "id" and ans != "user_name" and ans != "user_surname":
                if ans[0] == "D":
                    # a = Answer.objects.get(id=int(ans[1:]))
                    # a.title = request.POST[ans]
                    # a.save()
                    poll_text += "Вопрос: " + Answer.objects.get(id=int(ans[1:])).question_relate.title
                    poll_text += "\nОтвет: " + request.POST[ans]
                    poll_text += "\n" * 2
                else:
                    # a = Answer.objects.get(id=int(request.POST[ans]))
                    # a.ans = True
                    # a.save()
                    poll_text += "Вопрос: " + Question.objects.get(id=int(ans)).title
                    poll_text += "\nОтвет: "
                    iter = 0
                    for a in request.POST.getlist(ans, []):
                        iter += 1
                        poll_text += Answer.objects.get(id=int(a)).title
                        if iter < len(request.POST.getlist(ans, [])):
                            poll_text += ", "
                    poll_text += "\n" * 2

        id = int(request.POST["id"])
        poll = Poll.objects.get(id=id)
        poll_results = PollResult.objects.create(poll_relate=poll, name=request.POST["user_name"], \
                                                 surname=request.POST["user_surname"])
        chatGPT_result = chatGPT(poll_text)
        for gift in chatGPT_result:
            print(Gift.objects.get(id=gift))
            poll_results.result.add(Gift.objects.get(id=gift))
        poll_results.save()
        return HttpResponseRedirect(request.path_info)


@login_required(login_url="/login")
def poll_creation(request: WSGIRequest, poll_number=0):
    if request.method == "GET":
        context = {
            'poll': Poll.objects.get(id=poll_number),
        }

        return render(request, 'pages/poll_creation.html', context)
    elif request.method == "POST":
        data = request.POST.get("DATA", None)
        data = json.loads(data)
        print(data)
        id = int(request.POST["id"])
        poll = Poll.objects.get(id=id)
        for q in poll.poll_relate.all():
            q.delete()
        poll_title = request.POST["poll_title"]
        description = request.POST["poll_description"]
        new_questions = data

        for nq in new_questions:
            title = nq["title"]
            if title != "":
                type = nq["type"]
                if type == "Одиночный выбор":
                    type = "singular"
                elif type == "Множественный выбор":
                    type = "plural"
                elif type == "Открытый вопрос":
                    type = "detailed"
                question = Question.objects.create(title=title, type=type, poll_relate=poll)
                for answer in nq["answers"]:
                    answer_object = Answer.objects.create(title=answer, question_relate=question, ans=False)

        poll.title = poll_title
        poll.description = description
        image = request.FILES.getlist('image', '')
        if image != '':
            fss = FileSystemStorage()
            filename = fss.save(image[0].name, image[0])
            url = fss.url(filename)
            poll.image = url

        poll.save()

        return HttpResponseRedirect(request.path_info)


@login_required(login_url="/login/")
def user_polls(request: WSGIRequest):
    context = {
        'all_polls': Poll.objects.filter(user=Profile.objects.get(user=request.user)),
    }
    return render(request, 'pages/user_polls.html', context)


@login_required(login_url="/login")
def poll_results(request: WSGIRequest, poll_number=0):
    poll = Poll.objects.get(id=poll_number)
    poll_results = PollResult.objects.filter(poll_relate=poll)
    has_results = poll_results.exists()
    context = {
        'poll': poll,
        'has_results': has_results,
        'poll_results': poll_results if has_results else None,
    }
    return render(request, 'pages/poll_results.html', context)


@login_required(login_url="/login")
def delete_poll(request: WSGIRequest, poll_number=0):
    poll = Poll.objects.get(id=poll_number)
    poll.delete()
    return redirect('user_polls')


@login_required(login_url="/login")
def new_poll(request: WSGIRequest):
    new_poll = Poll.objects.create(user=Profile.objects.get(user=request.user))
    return redirect('poll_creation', poll_number=new_poll.id)


def all_gifts(request):
    context = {'gifts_by_holiday': Holiday.objects.all()}
    return render(request, 'pages/all_gifts.html', context)


class RegisterUser(CreateView):
    """
    Класс представления для регистрации нового пользователя.
    Позволяет новым пользователям зарегистрироваться в системе.

    :param form_class: Форма для регистрации пользователя.
    :param template_name: Шаблон для отображения страницы регистрации.
    :param success_url: URL для перенаправления после успешной регистрации.

    """
    form_class = RegisterUserForm
    template_name = 'base/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        profile = Profile.objects.create(user=user)
        login(self.request, user)
        return redirect('index')


class LoginUser(LoginView):
    """
    Класс представления для входа пользователя в систему.
    Позволяет пользователям войти в систему, используя свои учетные данные.

    :param form_class: Форма для входа пользователя.
    :param template_name: Шаблон для отображения страницы входа.
    """
    form_class = LoginUserForm
    template_name = 'base/login.html'

    def get_success_url(self):
        return reverse_lazy('index')


def logout_user(request):
    """
    Обработчик запроса для выхода пользователя из системы.
    Позволяет пользователю выйти из системы и перенаправляет его на страницу входа.

    :param request: Объект HttpRequest от Django.
    :return: HttpResponse: Перенаправление на страницу входа.
    """
    logout(request)
    return redirect('index')
