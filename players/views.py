from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django import forms
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from players.models import Player


FILTER_CHOICES = (
    ('sur', 'Surname'),
    ('univer', 'University'),
    ('paid', 'Who paid'),
    ('stud', 'Have stud photos'),
    ('play', 'Already players')
)


class SearchForm(forms.Form):
    s = forms.CharField(label='', max_length=50, required=False)
    o = forms.ChoiceField(label='Sorted by:', choices=FILTER_CHOICES, initial='sur')


def roster(request):
    players_list = Player.objects.filter(is_active=True)#.filter(is_admin=False)
    # TODO Find filter() parameters (OR)
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
                players_list = players_list.order_by('is_paid', 'surname')
            elif o == 'stud':
                players_list = players_list.order_by('is_student', 'surname')
            elif o == 'play':
                players_list = players_list.filter(is_paid=True, is_student=True)
                players_list = players_list.order_by('surname')
        else:
            search_form = SearchForm()
            players_list = players_list.order_by('surname')

    context = {'players_list': players_list, 'user_id': request.user.id, 'search_form': search_form}
    return render(request, 'players/roster.html', context)


def admin(request):
    return HttpResponseRedirect('/admin')


@login_required()
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


@login_required()
def player_change(request, player_id):
    context = {}
    if request.user.id != int(player_id):
        return HttpResponseRedirect(reverse('players:info', args=[player_id]))
    try:
        player = Player.objects.get(pk=player_id)
        context.update({'player_photo': player.photo})
    #     here would be form
    except Player.DoesNotExist:
        return HttpResponseRedirect(reverse('players:roster'))
    # TODO Create a form for change players
    return HttpResponse('Right user')
