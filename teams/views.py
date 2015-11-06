from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext

from teams.models import Team


# Create your views here.


# Функция для получения контекста из тех команд, которые доступны игроку
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
    return context

# Функция для обработки выбора команды

@login_required
def select(request):
    if request.user.team != None:
        # TODO выдать красивую ошибку, что ты уже выбрал
        return HttpResponseRedirect(reverse('players:roster', args=()))

    context = team_selection(request)
    if request.method == 'POST':
        try:
            selected_team = Team.objects.get(pk=request.POST['team'])
        except (KeyError, Team.DoesNotExist):
            context.update({'error_message': "You didn't select a team."})
            return render(request, 'teams/select_team.html', context)

        else:
            #Проверка на то, не выбрали ли уже команду эту, пока ты сам выбирал!
            #TODO check this!

            flag = False
            for player in selected_team.player_set.all():
                if player.pool == request.user.pool :
                  flag = True
            if flag:
                context.update({'error_message': "Team is already selected."})
                return render(request, 'teams/select_team.html', context)

            else:
                request.user.team = selected_team
                request.user.save()
                return HttpResponseRedirect(reverse('players:roster', args=()))
    else:
        return render(request, 'teams/select_team.html',context)

