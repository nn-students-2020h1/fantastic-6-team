from fantastic_chat_bot import FantasticBot
from setup import PROXY, TOKEN

Vitalya = FantasticBot(TOKEN, PROXY)
Vitalya.logger.info('Start Bot')
Vitalya.run_bot()
