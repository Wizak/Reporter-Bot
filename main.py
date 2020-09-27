import config
import logging
import datetime

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)

buttons = [
    KeyboardButton('Subscribe'),
    KeyboardButton('Unsubscribe'),
    KeyboardButton('Report')
]

report_status = None


@dp.message_handler(commands=['start'])
async def start_dialog(message: types.Message):

    global report_status

    report_status = False
    board = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
    ).add(buttons[0])

    await bot.send_message(
        message.from_user.id,
        '@'+message.from_user.username+' connect.',
        reply_markup=board
    )


@dp.message_handler()
async def action_on_button(message: types.Message):

    global report_status

    if message.text == 'Subscribe':
        # add to db
        board = ReplyKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True
        ).add(*buttons[1:])

        await bot.send_message(
            message.from_user.id,
            '@'+message.from_user.username+' has subscribed!',
            reply_markup=board
        )

    elif message.text == 'Unsubscribe':
        # delete from db
        board = ReplyKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True
        ).add(buttons[0])

        await bot.send_message(
            message.from_user.id,
            '@'+message.from_user.username+' has unsubscribed!',
            reply_markup=board
        )

    elif message.text == 'Report':
        # create report
        report_status = True
        board = ReplyKeyboardRemove(True)
        await bot.send_message(
            message.from_user.id,
            'Wait for reporting...',
            reply_markup=board
        )

    else:
        if report_status:
            # save report
            date = datetime.datetime.now().strftime('%c')
            with open('Reports.docx', 'a') as f:
                content = '@' + message.from_user.username + \
                    '\t' + date + '\n\n' + message.text + '\n'*5
                f.write(content)

            report_status = False
            board = ReplyKeyboardMarkup(
                resize_keyboard=True,
                one_time_keyboard=True
            ).add(*buttons[1:])

            await bot.send_message(
                message.from_user.id,
                '@'+message.from_user.username+' has reported!',
                reply_markup=board
            )


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
