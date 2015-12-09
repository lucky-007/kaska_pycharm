import re

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse

from players.models import Team, Player


def teams_upload(request):
    if request.user.is_anonymous() or not request.user.is_admin:
        return HttpResponseRedirect(reverse('index'))
    f = open('/home/u49036/kaska.me/kaska_pycharm/players/teams.txt', 'r')
    lines = f.readlines()
    f.close()
    lines_cleared = []
    for i in lines:
        s = i.rstrip()
        if s == '':
            continue

        # s = re.sub(u"(\u2018|\u2019)", "'", s)
        # s = re.sub(u"(\u2013|\u2014)", "-", s)
        # s = re.sub(u"(\u2026)", "...", s)
        # s = re.sub("(\xab|\xbb)", '"', s)
        lines_cleared.append(s)

    lines = lines_cleared

    teams = {}
    re_team = re.compile('^team(?P<team>\d{1,2}).(?P<name>.+):$')
    re_intimation = re.compile('^(?P<num>\d).\w*(?P<phrase>.*)$')
    for l in lines:
        q = re_team.match(l)
        if q:
            t = q.group('team')
            teams.update({t: {'team_name': q.group('name')}})
            continue

        q = re_intimation.match(l)
        if q:
            teams[t].update({'intimation'+q.group('num'): q.group('phrase')})

    for t in teams:
        team_obj = Team(**teams[t])
        team_obj.id = int(t)
        team_obj.save()
    return HttpResponse('all right')


def pools_update(request):
    if request.user.is_anonymous() or not request.user.is_admin:
        return HttpResponseRedirect(reverse('index'))
    f = open('/home/u49036/kaska.me/kaska_pycharm/players/pools.txt', 'r')
    lines = f.readlines()
    f.close()
    lines = [i.rstrip() for i in lines]
    while '' in lines:
        lines.remove('')

    pool = {}
    re_pool = re.compile('^(?P<pool>\d+).*:')
    for l in lines:
        q = re_pool.match(l)
        if q:
            p = q.group('pool')
            continue
        if p in pool:
            pool[p].append(l)
        else:
            pool[p] = [l, ]

    for pool_num in pool:
        for pl_full_name in pool[pool_num]:
            sur = pl_full_name.split()[0]
            nam = pl_full_name.split()[1]
            pl_obj = Player.objects.filter(surname__iexact=sur)
            if pl_obj.count() == 0:
                continue
            elif pl_obj.count() != 1:
                pl_obj = pl_obj.filter(name__iexact=nam)
                if pl_obj.count() != 1:
                    continue
            pl_obj = pl_obj[0]
            pl_obj.pool = int(pool_num)
            pl_obj.save()

    return HttpResponse('pools updated')


def teams_flush(request):
    if request.user.is_anonymous() or not request.user.is_admin:
        return HttpResponseRedirect(reverse('index'))
    teams = Team.objects.all()
    for t in teams:
        t.chosen = 8*'0'
        t.save()
    return HttpResponse('teams were flushed')
