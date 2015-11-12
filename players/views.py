from django.conf import settings
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, resolve_url
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from players.forms import SearchForm, PlayerSelfChangeForm, PlayerCreationForm, AuthenticationForm
from players.models import Player


def roster(request):
    players_list = Player.objects.filter(is_active=True)
    if request.method != 'GET':
        search_form = SearchForm()
        players_list = players_list.order_by('surname')
    else:
        search_form = SearchForm(request.GET.dict())
        if search_form.is_valid():
            s = search_form.cleaned_data['s']
            o = search_form.cleaned_data['o']
            if s:
                players_list = players_list.filter(Q(surname__icontains=s) |
                                                   Q(name__icontains=s) |
                                                   Q(university__icontains=s))

            if o == 'sur':
                players_list = players_list.order_by('surname')
            elif o == 'univer':
                players_list = players_list.order_by('university', 'surname')
            elif o == 'paid':
                players_list = players_list.order_by('-is_paid', 'surname')
            elif o == 'stud':
                players_list = players_list.order_by('-is_student', 'surname')
            elif o == 'play':
                players_list = players_list.filter(is_paid=True, is_student=True)
                players_list = players_list.order_by('surname')
        else:
            search_form = SearchForm()
            players_list = players_list.order_by('surname')

    context = {'players_list': players_list, 'user_id': request.user.id, 'search_form': search_form}
    return render(request, 'players/roster.html', context)


@login_required
def player_info(request, player_id):
    context = {}
    try:
        player = Player.objects.get(pk=player_id)
        if request.user.id == int(player_id):
            context.update({'this_player': True})
    except Player.DoesNotExist:
        return HttpResponseRedirect(reverse('players:roster'))

    context.update({'player': player})
    return render(request, 'players/info.html', context)


@csrf_protect
@login_required
def player_change(request):
    context = {}
    player = request.user
    context.update({'player_photo': player.photo})

    if request.method == 'POST':
        change_form = PlayerSelfChangeForm(instance=player, data=request.POST, files=request.FILES)
        if change_form.is_valid():
            player = change_form.save(commit=False)
            # TODO download link to vk photo
            player.save()
            return HttpResponseRedirect(reverse('players:info', args=[player.id]))
    else:
        change_form = PlayerSelfChangeForm(instance=player)

    context.update({'form': change_form})
    return render(request, 'players/player_change.html', context)


@csrf_protect
@login_required
def password_change(request):
    if request.method == 'POST':
        password_form = PasswordChangeForm(user=request.user, data=request.POST)
        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            return HttpResponseRedirect(reverse('players:info', args=[request.user.id]))
    else:
        password_form = PasswordChangeForm(user=request.user)

    context = {'password_form': password_form}
    return render(request, 'players/change_password.html', context)


@csrf_protect
def player_create(request):
    if not request.user.is_anonymous():
        return HttpResponseRedirect(reverse('players:info', args=[request.user.id]))

    if request.method == 'POST':
        form = PlayerCreationForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            player = form.save(commit=False)
            # TODO download link to vk photo
            player.save()
            return HttpResponseRedirect(reverse('players:roster'))  # maybe to index?
    else:
        form = PlayerCreationForm()
    context = {'form': form}
    return render(request, 'players/player_create.html', context)


@csrf_protect
@never_cache
def login(request, template_name='players/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):
    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, ''))

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            auth_login(request, form.get_user())
            return HttpResponseRedirect(redirect_to)
    else:
        form = authentication_form(request)

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('index'))


def index(request):
    context = {}
    if request.user.is_anonymous():
        if request.method == 'POST':
            auth_form = AuthenticationForm(request, data=request.POST)
            if auth_form.is_valid():
                auth_login(request, auth_form.get_user())
                return HttpResponseRedirect(reverse('index'))
        else:
            auth_form = AuthenticationForm(request)
        context.update({'auth_form': auth_form})
    else:
        context.update({'player': request.user})
    context.update({'current_url': request.path})
    return render(request, 'players/index.html', context)


@csrf_protect
def password_reset(request):
    """
    View for entering email of registered player to change password
    :param request:
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))

    context = {}
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': default_token_generator,
                'from_email': settings.KASKA_EMAIL,
                'email_template_name': 'players/email/email_template.html',
                'subject_template_name': 'players/email/email_subject.txt',
                'request': request,
            }

            try:
                Player.objects.get(email__iexact=form.cleaned_data['email'])
            except Player.DoesNotExist:
                return HttpResponseRedirect(reverse('players:password_reset_no_email'))
            else:
                form.save(**opts)
                return HttpResponseRedirect(reverse('players:password_reset_check_email'))
    else:
        form = PasswordResetForm()

    context.update({'form': form})
    return render(request, 'players/password_reset/password_reset.html', context)


def check_email(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))
    context = {}
    return render(request, 'players/password_reset/check_email.html', context)


def no_email(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))
    context = {}
    return render(request,'players/password_reset/no_email.html', context)


def password_reset_confirm(request, uidb64, token):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))
    return None


def password_reset_complete(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))
    return None
