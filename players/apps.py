import json
import logging

from django.apps import AppConfig
from django.db.models.signals import post_save

logger = logging.getLogger('players_db_entries')


def log_players_change(sender, **kwargs):
    player = kwargs['instance']
    created = kwargs['created']
    raw = kwargs['raw']

    if not raw:
        # message = '{created:s} {id:d}: {name:s} data={data:s}'

        fields = sorted(sender._meta.get_all_field_names())
        for i in ('logentry', 'user_permissions', 'groups', 'last_login'):
            if i in fields:
                fields.remove(i)
        data = {unicode(i): unicode(getattr(player, i)) for i in fields}

        log_args = {
            'created': u'CREATED' if created else u'MODIFIED',
            'id': data[u'id'],
            'name': player.get_full_name(),
            'data': json.dumps(data, ensure_ascii=False),
        }

        log_string = u''
        for i in ['created', 'id', 'name', 'data']:
            if i == 'data':
                log_string += log_args[i]
                continue
            log_string += log_args[i] + u' '
        logger.info(log_string)


class PlayerConfig(AppConfig):
    name = 'players'
    verbose_name = 'Players'

    def ready(self):
        post_save.connect(
            receiver=log_players_change,
            sender=self.get_model('Player'),
            weak=True,
            dispatch_uid='player_db_logging'
        )
