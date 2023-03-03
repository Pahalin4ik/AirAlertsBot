import logging
from aiogram.utils import executor
from bot import *
from aletrsparser import *

logging.basicConfig(level=logging.INFO)
app.start()
executor.start_polling(dp, skip_updates=True)
app.stop()
db.close()
