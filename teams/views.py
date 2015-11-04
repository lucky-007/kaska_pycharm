from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.utils import timezone
from django.views import generic
from teams.models import Team


# Create your views here.

# Функция для обработки реквеста для teams/select
@login_required
def team_selection(request):
    #if not request.user.is_authenticated():
        #return redirect()
        #pass
    #else:


    # КОСТЫЛЬ! НАДО УБРАТЬ!

    available_teams = []

    for team in Team.objects.all():
        flag = True
        for player in team.player_set.all():
            if player.pool == request.user.pool :
                flag = False
        if flag:
            available_teams.append(team)


    context = RequestContext(request, {
        'user' : request.user,
        'user_pool' : request.user.pool,
        'teams_list': available_teams
    })
    return render(request, 'teams/select_team.html', context)

# Функция для обработки выбора команды

@login_required
def select(request):
    try:
        selected_choice = Team.objects.get(pk=request.POST['team'])
    except (KeyError, Team.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'teams/select_team.html', {
            'error_message': "You didn't select a team.",
        })

    else:
        if request.user.pool in selected_choice.pool:
            return render(request, 'teams/select_team.html', {
                'error_message': "Вдруг два человека обратятся к одной команде сразу - это так раз тот случай, и ты проебался((( прости. "
            })
        else:
            request.user.team = selected_choice
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            return HttpResponseRedirect(reverse('teams:detail', args=()))

