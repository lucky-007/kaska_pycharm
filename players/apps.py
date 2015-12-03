import json
import logging

from django.apps import AppConfig
from django.db.models.signals import post_save

logger = logging.getLogger('players_db_entries')


def log_players_change(sender, **kwargs):
    player = kwargs['instance']
    created = kwargs['created']
    raw = kwargs['raw']
    message = '{created:s} {id:d}: {name:s} data={data:s}'

    fields = sorted(sender._meta.get_all_field_names())
    for i in ('logentry', 'user_permissions', 'groups', 'last_login'):
        if i in fields:
            fields.remove(i)

    data = {i: str(getattr(player, i)) for i in fields}
    log_args = {
        'created': 'CREATED' if created else 'MODIFIED',
        'id': player.id,
        'name': player.get_full_name(),
        'data': json.dumps(data),
    }
    if not raw:
        logger.info(message.format(**log_args))


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
