import os
import random
import asyncio
from collections import OrderedDict

import telepot
from telepot.async.delegate import per_chat_id, create_open


translations = OrderedDict([
    ('English', {'words': ['Yes', 'Yeah', 'Exactly'], 'image': 'https://upload.wikimedia.org/wikipedia/en/thumb/a/a4/Flag_of_the_United_States.svg/500px-Flag_of_the_United_States.svg.png'}),
    ('Russian', {'words': ['Да', 'Правда', 'Точно'], 'image': 'https://upload.wikimedia.org/wikipedia/en/thumb/f/f3/Flag_of_Russia.svg/500px-Flag_of_Russia.svg.png'}),
    ('Italiano', {'words': ['Sì', 'Di sì', 'Certo'], 'image': 'https://upload.wikimedia.org/wikipedia/en/thumb/0/03/Flag_of_Italy.svg/500px-Flag_of_Italy.svg.png'})
])


class YesBot(telepot.async.helper.UserHandler):

    def __init__(self, seed_tuple, timeout):
        super(YesBot, self).__init__(seed_tuple, timeout, flavors=['inline_query', 'chosen_inline_result'])
        self._answerer = telepot.async.helper.Answerer(self.bot)

    def on_inline_query(self, msg):
        def compute_answer():
            query_string = telepot.glance(msg, flavor='inline_query')[2]

            articles = []

            num_random_answer = random.choice(range(3))

            for translation_id, translation in translations.items():
                if query_string:
                    articles.append({
                        'type': 'article',
                        'id': translation_id.lower(),
                        'title': translation_id,
                        'description': '«{0}» - {1}'.format(query_string, translation['words'][num_random_answer]),
                        'message_text': '«{0}» - *{1}*'.format(query_string, translation['words'][num_random_answer]),
                        'parse_mode': 'markdown',
                        'thumb_url': translation['image']
                    })
                else:
                    articles.append({
                        'type': 'article',
                        'id': translation_id.lower(),
                        'title': translation_id,
                        'description': '{0}'.format(translation['words'][num_random_answer]),
                        'message_text': '*{0}*'.format(translation['words'][num_random_answer]),
                        'parse_mode': 'markdown',
                        'thumb_url': translation['image']
                    })

            return articles

        try:
            self._answerer.answer(msg, compute_answer)
        except Exception as e:
            print(msg)
            print(e)
            print(articles)

    # override default on_chosen_inline_result
    def on_chosen_inline_result(self, msg):
        pass

    # override default logger error in on_close, otherwise logs become messy
    def on_close(self, exception):
        pass

    # fix a bug with UserHandler expecting on_chat_message to be implemented
    def on_chat_message(self, msg):
        pass


ACCESS_TOKEN = os.getenv('TELEGRAM_API_KEY')

bot = telepot.async.DelegatorBot(ACCESS_TOKEN, [
    (per_chat_id(), create_open(YesBot, timeout=5*60)),
])
loop = asyncio.get_event_loop()

loop.create_task(bot.message_loop())
print('Started!')

loop.run_forever()
