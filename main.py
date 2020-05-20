"""Running the Bot"""

from vita_chat_bot import VitaBot
from setup import PROXY, TOKEN

Vitalya = VitaBot(TOKEN, PROXY)
Vitalya.logger.info('Start Bot')
Vitalya.run_bot()

