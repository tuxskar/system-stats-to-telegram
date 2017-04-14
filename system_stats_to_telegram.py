import logging

import attr
import click
from psutil import virtual_memory, swap_memory
from telegram.ext import Updater, CommandHandler

from utils import extract_comma_sep, convert_size

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


@click.command()
@click.argument('token')
@click.option('--user_ids', default='', help='Authorized comma separated users ids to send information to')
@click.option('--usernames', default='', help='Authorized comma separated usernames to send information to')
def stats_notifier(token, user_ids, usernames):
    updater = Updater(token)
    stats_handler = StatsHandler(user_ids, usernames)
    updater.dispatcher.add_handler(CommandHandler('stats', stats_handler.stats))
    updater.start_polling()
    updater.idle()


@attr.s
class StatsHandler:
    user_ids = attr.ib(convert=extract_comma_sep)
    usernames = attr.ib(convert=extract_comma_sep)

    def __attrs_post_init__(self):
        if not self.user_ids and not self.usernames:
            logger.warning('No user restrictions have been set, ANYONE using telegram can run commands, please check '
                           'README file to fix.')

    def stats(self, bot, update):
        def format_memory_stats():
            mem = virtual_memory()
            metrics = ['-- Ram']
            for attribute in ('used', 'available', 'free', 'total', 'available'):
                metrics.append('{}: {}'.format(attribute.title(), convert_size(getattr(mem, attribute))))
            metrics.append('Percent: {}%'.format(mem.percent))
            metrics.append('-- Swap')
            mem = swap_memory()
            for attribute in ('used', 'total', 'free'):
                metrics.append('{}: {}'.format(attribute.title(), convert_size(getattr(mem, attribute))))
            metrics.append('Percent: {}%'.format(mem.percent))
            return '\n'.join(metrics)

        # TODO: get ip
        # TODO: get cpu avg load
        # TODO: get temperature
        # TODO: uptime
        # TODO: top process running
        # TODO: check sending a parameter like raspi or pc to only answer the bot that pass the filter

        allowed_user = self.allowed_user(update)
        if allowed_user:
            msg = format_memory_stats()
        else:
            msg = 'Sorry, you are not authorized to get information.'
        update.message.reply_text(msg)

    def allowed_user(self, update):
        if not self.user_ids and not self.usernames:
            return True
        user_info = update.to_dict().get('message').get('from')
        user_id = user_info.get('id')
        username = user_info.get('username')
        return str(user_id) in self.user_ids or username in self.usernames


if __name__ == '__main__':
    stats_notifier()
