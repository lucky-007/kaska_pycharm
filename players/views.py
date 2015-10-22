from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django import forms
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from players.models import Player, CHOICES_POSITION, CHOICES_STYLE

CHOICES_FILTER = (
    ('sur', 'Surname'),
    ('univer', 'University'),
    ('paid', 'Who paid'),
    ('stud', 'Have stud photos'),
    ('play', 'Already players')
)


class SearchForm(forms.Form):
    s = forms.CharField(label='', max_length=50, required=False)
    o = forms.ChoiceField(label='Sorted by:', choices=CHOICES_FILTER, initial='sur')


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


def admin(request):
    return HttpResponseRedirect('/admin')


@login_required
def player_info(request, player_id):
    context = {}
    try:
        player = Player.objects.get(pk=player_id)
        if request.user.id == int(player_id):
            context.update({'this_player': True})
    except Player.DoesNotExist:
        return HttpResponseRedirect(reverse('players:roster'))

    context.update({'player': player, 'choices_pos': CHOICES_POSITION, 'choices_style': CHOICES_STYLE})
    return render(request, 'players/info.html', context)


class PlayerSelfCreateForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Player
        fields = ('email', 'password1', 'password2', 'surname', 'name', 'university', 'experience', 'vk_link',
                  'position', 'fav_throw', 'style', 'size')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2


class PlayerSelfChangeForm(PlayerSelfCreateForm):
    class Meta:
        exclude = ('password1', 'password2')


@csrf_protect
@login_required
def player_change(request):
    # TODO make sure to have opportunity to upload photo
    context = {}
    player = request.user
    context.update({'player_photo': player.photo})

    if request.method == 'POST':
        change_form = PlayerSelfChangeForm(instance=player, data=request.POST)
        if change_form.is_valid():
            change_form.save(commit=False)
            # TODO download link to vk photo
            change_form.save()
            return HttpResponseRedirect(reverse('players:info', args=[player.id]))
    else:
        change_form = PlayerSelfChangeForm(instance=player)

    context.update({'form': change_form})
    return render(request, 'players/player_change.html', context)
