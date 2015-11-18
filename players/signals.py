import logging

from django.apps import AppConfig
from django.db.models.signals import post_save


logger = logging.getLogger('players.db_entries')


def log_players_change(sender, **kwargs):
    player = kwargs['instance']
    created = kwargs['created']
    raw = kwargs['raw']
    logger.info(str(player)+' '+str(created)+' '+str(raw))


class PlayerConfig(AppConfig):
    def ready(self):
        post_save.connect(
            receiver=log_players_change,
            sender=self.get_model('Player'),
            weak=True,
            dispatch_uid='player_db_logging'
        )
