import logging
import mimetypes
import os
import posixpath
import random
import stat

import datetime
from django.core.exceptions import PermissionDenied
from django.utils.six.moves.urllib.parse import unquote

import requests
import json

from django.conf import settings
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
    get_user_model, authenticate)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden, Http404, HttpResponseNotModified, \
    FileResponse
from django.shortcuts import render, resolve_url
from django.template.response import TemplateResponse
from django.utils.encoding import force_text
from django.utils.http import is_safe_url, urlsafe_base64_decode, http_date
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.utils.translation import ugettext_lazy as _, ugettext
from django.views.static import was_modified_since

from players.forms import SearchForm, PlayerSelfChangeForm, PlayerCreationForm, AuthenticationForm
from players.models import Player, Team


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

    context = {'players_list': players_list, 'user_id': request.user.id, 'search_form': search_form, 'request': request}
    return render(request, 'players/roster.html', context)


@login_required
def player_info(request, player_id):
    context = {'request': request}
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
    context = {'request': request}
    player = request.user
    context.update({'player_photo': player.photo})

    if request.method == 'POST':
        change_form = PlayerSelfChangeForm(instance=player, data=request.POST, files=request.FILES)
        if change_form.is_valid():
            player = change_form.save(commit=False)
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

    context = {'password_form': password_form, 'request': request}
    return render(request, 'players/change_password.html', context)


@csrf_protect
def player_create(request):
    if not request.user.is_anonymous():
        return HttpResponseRedirect(reverse('players:info', args=[request.user.id]))
    error = None
    disp_errors = {}

    if request.method == 'GET' and 'vk' not in request.session:
        redirect_uri = request.build_absolute_uri(resolve_url('players:create'))
        if not request.GET.dict():
            vk_opts_user = {
                'client_id': settings.VK_CLIENT_ID,
                'display': 'popup',
                'redirect_uri': redirect_uri,
                'scope': ','.join(settings.VK_SCOPES),
                'response_type': 'code',
                'v': '5.40',
            }
            return HttpResponseRedirect(requests.get('https://oauth.vk.com/authorize', params=vk_opts_user).url)
        else:
            if 'error' in request.GET.keys():
                return HttpResponseRedirect(reverse('index'))

            vk_opts_server = {
                'client_id': settings.VK_CLIENT_ID,
                'client_secret': settings.VK_CLIENT_SECRET,
                'redirect_uri': redirect_uri,
                'code': request.GET['code'],
            }
            r = requests.get('https://oauth.vk.com/access_token', params=vk_opts_server)
            vk_resp = r.json()

            if 'error' in vk_resp.keys():
                error = 'bad_oauth'
                return render(request, 'players/player_create.html', {'error': error})

            vk_data = {i: vk_resp[i] for i in vk_resp if i in ['access_token', 'email', 'user_id']}
            vk_data['vk_id'] = str(vk_data.pop('user_id'))

            if Player.objects.filter(vk_id=vk_data['vk_id']):
                error = 'registered'
                return render(request, 'players/player_create.html', {'error': error})

            vk_opts_server = {
                'user_id': vk_data['vk_id'],
                'access_token': vk_data['access_token'],
                'v': '5.40',
                'fields': 'photo_400_orig,sex,photo_max',
                'name_case': 'nom',
            }
            r = requests.get('https://api.vk.com/method/users.get', params=vk_opts_server)
            vk_data.update(r.json()['response'][0])
            vk_data.pop('id')
            vk_data['name'] = vk_data.pop('first_name')
            vk_data['surname'] = vk_data.pop('last_name')
            if vk_data['sex'] == 1:
                vk_data['sex'] = 'f'
            else:
                vk_data['sex'] = 'm'
            request.session['vk'] = vk_data

    if request.method == 'POST':
        form = PlayerCreationForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            vk_data = request.session['vk']
            request.session.flush()
            player = form.save(commit=False)
            player.vk_id = vk_data['vk_id']
            player.access_token = vk_data['access_token']
            if 'photo_400_orig' in vk_data:
                player.photo = vk_data['photo_400_orig']
            else:
                player.photo = vk_data['photo_max']
            player.save()
            player = authenticate(email=player.email, password=form.cleaned_data['password2'])
            auth_login(request, player)
            return HttpResponseRedirect(reverse('info'))
        else:
            form_errors = json.loads(form.errors.as_json())
            for field in form_errors:
                if form_errors[field][0]['code'] != 'required':
                    disp_errors.update({
                        form.fields[field].widget.attrs['placeholder']: form_errors[field][0]['message']
                    })
    else:
        form = PlayerCreationForm(initial=request.session['vk'])

    context = {'form': form, 'error': error, 'request': request, 'form_errors': disp_errors}
    return render(request, 'players/player_create.html', context)


@csrf_protect
@never_cache
def login(request, template_name='players/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):

    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))

    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, resolve_url('index')))

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
        'request': request,
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
    pl_registered = Player.objects.filter(is_paid=True, is_active=True, is_student=True).count()
    now = datetime.datetime.now()
    end = datetime.datetime(2015, 12, 20, 0, 0)
    til_end = end - now
    til_end = til_end.days
    context = {'request': request, 'registered_players': pl_registered,
               'til_end': til_end}
    return render(request, 'players/index.html', context)


@csrf_protect
def password_reset(request):
    """
    View for entering email of registered player to change password
    :param request:
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))

    context = {'request': request}
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': default_token_generator,
                'from_email': settings.DEFAULT_FROM_EMAIL,
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
    context = {'request': request}
    return render(request, 'players/password_reset/check_email.html', context)


def no_email(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))
    context = {'request': request}
    return render(request, 'players/password_reset/no_email.html', context)


@never_cache
def password_reset_confirm(request, uidb64=None, token=None):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))

    context = {'request': request}
    UserModel = get_user_model()
    assert uidb64 is not None and token is not None

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        valid_link = True
        title = _('Enter new password')
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('players:password_reset_complete'))
        else:
            form = SetPasswordForm(user)
    else:
        valid_link = False
        title = _('Password reset failed')
        form = None

    context.update({
        'form': form,
        'title': title,
        'valid_link': valid_link,
    })
    return render(request, 'players/password_reset/confirm.html', context)


def password_reset_complete(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))
    context = {'request': request}
    return render(request, 'players/password_reset/complete.html', context)


def logo(request):
    return render(request, 'logo.html', {})


def media(request, path, document_root=None):
    if request.user.is_anonymous() or not request.user.is_admin:
        raise PermissionDenied

    path = posixpath.normpath(unquote(path))
    path = path.lstrip('/')
    newpath = ''
    for part in path.split('/'):
        if not part:
            # Strip empty path components.
            continue
        drive, part = os.path.splitdrive(part)
        head, part = os.path.split(part)
        if part in (os.curdir, os.pardir):
            # Strip '.' and '..' in path.
            continue
        newpath = os.path.join(newpath, part).replace('\\', '/')
    if newpath and path != newpath:
        return HttpResponseRedirect(newpath)
    fullpath = os.path.join(document_root, newpath)
    if os.path.isdir(fullpath):
        raise Http404(_("Directory indexes are not allowed here."))
    if not os.path.exists(fullpath):
        raise Http404(_('"%(path)s" does not exist') % {'path': fullpath})
    # Respect the If-Modified-Since header.
    statobj = os.stat(fullpath)
    if not was_modified_since(request.META.get('HTTP_IF_MODIFIED_SINCE'),
                              statobj.st_mtime, statobj.st_size):
        return HttpResponseNotModified()
    content_type, encoding = mimetypes.guess_type(fullpath)
    content_type = content_type or 'application/octet-stream'
    response = FileResponse(open(fullpath, 'rb'), content_type=content_type)
    response["Last-Modified"] = http_date(statobj.st_mtime)
    if stat.S_ISREG(statobj.st_mode):
        response["Content-Length"] = statobj.st_size
    if encoding:
        response["Content-Encoding"] = encoding
    return response


def gallery(request):
    return render(request, 'gallery.html', {'request': request})


def tournament(request):
    return render(request, 'tournament.html', {'request': request})


logger = logging.getLogger('teams_selection')

@csrf_protect
@login_required
def teams(request):
    context = {'request': request}

    error_msg = {
        'bad_req': ugettext('Bad team selected'),
        'already_selected': ugettext('This team was already selected'),
    }

    no_choice_msg = {
        'have_selected': ugettext('You have already selected your team'),
        'no_player': ugettext('You are not registered as player'),
    }

    if not settings.TEAM_SELECTION_STARTED and not request.user.is_admin:
        return render(request, 'teams/teams_soon.html', context)

    if not (request.user.is_paid and request.user.is_student and request.user.is_active):
        context.update({'cant_choose': no_choice_msg['no_player']})
    elif request.user.team is not None:
        context.update({'cant_choose': no_choice_msg['have_selected']})
    else:
        if request.method == 'POST':
            if 'selected' in request.POST:
                try:
                    team = Team.objects.get(pk=request.POST['selected'])
                except Team.DoesNotExist:
                    return HttpResponse(json.dumps({'error': error_msg['bad_req']}), content_type='application/json')
                chosen = team.chosen
                pos = request.user.pool - 1
                if chosen[pos] == '1':
                    return HttpResponse(json.dumps({'error': error_msg['already_selected']}),
                                        content_type='application/json')
                chosen = chosen[:pos]+'1'+chosen[pos+1:]
                team.chosen = chosen
                team.save()

                player = Player.objects.get(pk=request.user.id)
                player.team = team
                player.save()
                logger.info('p=%d t=%d' % (player.id, team.id))
                return HttpResponse(json.dumps({'done': True}), content_type='application/json')

    intimations = [(t.id, t.get_intimation(request.user.pool)) for t in Team.objects.all()]
    random.shuffle(intimations)
    context.update({'teams': intimations})
    return render(request, 'teams/teams.html', context)


def info(request):
    return render(request, 'info.html', {'request': request})


def teams_available(request):
    pool = int(request.GET['pool'])
    available = {t.id: t.is_available(pool) for t in Team.objects.all()}
    available = json.dumps(available)
    return HttpResponse(available, content_type='application/json')


def teams_success(request):
    return render(request, 'teams/teams_success.html', {})
