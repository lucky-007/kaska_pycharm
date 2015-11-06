from django.core.urlresolvers import reverse
from django.test import TestCase
from players.models import Player


def create_player(email, vk_link, surname='aaa', name='bbb', university='BMSTU'):
    return Player.objects.create(
        email=email,
        surname=surname,
        name=name,
        university=university,
        experience=5,
        vk_link=vk_link,
        position='han',
        fav_throw='scoober',
        style='slow',
        size='m',
    )


def create_players_db(amount=3):
    for i in range(amount):
        create_player(
            email='gogo%s@foo.com' % i,
            vk_link='vk.com/%s' % i,
            surname='Surname%s' % i,
            name='Name%s' % i,
            university='Uni%s' % i
        )


class PlayersViewTest(TestCase):
    def test_post_method(self):
        response = self.client.post(reverse('players:roster'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['players_list'], [])

    def test_get_method_without_parameters_no_players(self):
        response = self.client.get(reverse('players:roster'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['players_list'], [])

    def test_get_method_without_parameters_with_players(self):
        create_player('go@gogo.com', 'vk.com/eee', '123', '456')
        create_player('og@ogog.com', 'vk.com/123')
        response = self.client.get(reverse('players:roster'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['players_list'],
            ['<Player: 123 456>', '<Player: aaa bbb>']
        )

    def test_get_method_with_parameters(self):
        data = {'z': 2}
        response = self.client.get(reverse('players:roster'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'None')


class PlayerViewInfoAndChangeTest(TestCase):
    def test_info_non_logged_in(self):
        player = create_player('go@gogo.com', 'vk.com/eee', '123', '456')
        response = self.client.get(reverse('players:info', args=[player.id]))
        self.assertEqual(response.status_code, 302)

    def test_change_non_logged_in(self):
        player = create_player('go@gogo.com', 'vk.com/eee', '123', '456')
        response = self.client.get(reverse('players:change', args=[player.id]))
        self.assertEqual(response.status_code, 302)

    def test_info_non_existence_player(self):
        response = self.client.get(reverse('players:info', args=[1]))
        self.assertEqual(response.status_code, 302)

    def test_change_non_existence_player(self):
        response = self.client.get(reverse('players:change', args=[1]))
        self.assertEqual(response.status_code, 302)

    def test_info_logged_in_player_self(self):
        pass

    def test_info_logged_in_player_other(self):
        pass

    def test_change_logged_in_player_self(self):
        pass

    def test_change_logged_in_player_other(self):
        pass

    def test_info_logged_in_non_existence_player(self):
        pass

    def test_change_logged_in_non_existence_player(self):
        pass


class PlayerSortingAndFiltering(TestCase):
    pass
