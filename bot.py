import localize
from aiogram import types
from config import db, MapUrl
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from dispacher import dp
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext


class StartStates(StatesGroup):
    SelectLang = State()
    SelectTag = State()


@dp.message_handler(commands=['help', 'h'], state=None)
async def help(msg: types.Message):
    lang = db.get_user_lang(msg.chat.id)
    await msg.answer(localize.helpText[lang])
    await msg.delete()


@dp.message_handler(commands=['lang', 'l'], state=None)
async def lang(msg: types.message):
    lang = db.get_user_lang(msg.chat.id)
    lang_keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton("EN", callback_data="EN"),
        InlineKeyboardButton("UA", callback_data="UA")
    )
    await msg.answer(localize.selectLang[lang], reply_markup=lang_keyboard)
    await msg.delete()


@dp.message_handler(commands=['region', 'r'], state=None)
async def reg(msg: types.Message):
    lang = db.get_user_lang(msg.chat.id)
    keyboard = InlineKeyboardMarkup().add(
        *(InlineKeyboardButton(localize.regions[i][lang], callback_data=i) for i in localize.regions.keys()))
    await msg.answer(localize.selectRegion[lang], reply_markup=keyboard)
    await msg.delete()


@dp.message_handler(commands=['start'], state=None)
async def start(msg: types.Message):
    if db.user_exists(msg.chat.id):
        return
    lang_keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton("EN", callback_data="EN"),
        InlineKeyboardButton("UA", callback_data="UA")
    )
    await msg.answer(localize.helpText["EN"])
    await msg.answer(localize.selectLang["EN"],
                     reply_markup=lang_keyboard)
    await StartStates.SelectLang.set()
    await msg.delete()


@dp.callback_query_handler(state=None)
async def command(query: types.CallbackQuery):
    await query.message.delete()
    await query.answer(query.data)
    if query.data.startswith("#"):
        db.upd_region(query.message.chat.id, query.data)
    else:
        db.upd_lang(query.message.chat.id, query.data)


@dp.callback_query_handler(state=StartStates.SelectLang)
async def setLang(query: types.CallbackQuery, state: FSMContext):
    await query.answer(query.data)
    async with state.proxy() as data:
        data['lang'] = query.data
    keyboard = InlineKeyboardMarkup().add(
        *(InlineKeyboardButton(localize.regions[i][query.data], callback_data=i) for i in localize.regions.keys()))
    await query.message.answer(localize.selectRegion[query.data], reply_markup=keyboard)
    await query.message.delete()
    await StartStates.next()


@dp.callback_query_handler(state=StartStates.SelectTag)
async def setRegion(query: types.CallbackQuery, state: FSMContext):
    await query.message.delete()
    async with state.proxy() as data:
        db.add_user(query.message.chat.id, data['lang'], query.data)
    await query.answer(query.data)
    await state.finish()


@dp.message_handler(commands=['m', 'menu'])
async def menu(msg: types.Message):
    await msg.answer()


@dp.message_handler(commands=['map'])
async def get_map(msg: types.Message):
    await msg.delete()
    lang = db.get_user_lang(msg.chat.id)
    pref = "" if lang == "UA" else "en"
    url = MapUrl + pref
    map_keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton(localize.here[lang], web_app=WebAppInfo(url=url))
    )
    await msg.answer(localize.map_placed[lang], reply_markup=map_keyboard)
