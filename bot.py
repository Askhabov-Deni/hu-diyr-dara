# bot.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    ConversationHandler
)
from config import TELEGRAM_BOT_TOKEN
from recommendation_engine import recommend_activities
import logging

# Настройка логгирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Состояния диалога
CITY, BUDGET, MOOD, FREE_TIME, SUGGESTING = range(5)

# Глобальные переменные для хранения данных
user_data = {}
suggestions = {}


async def start(update: Update, context) -> int:
    await update.message.reply_text(
        "Привет! Я помогу тебе выбрать активность на сегодня.\n"
        "Для начала, в каком городе ты находишься?"
    )
    return CITY


async def city(update: Update, context) -> int:
    user_data['city'] = update.message.text
    await update.message.reply_text(
        "Отлично! Сколько рублей ты готов потратить на активность?"
    )
    return BUDGET


async def budget(update: Update, context) -> int:
    try:
        budget = float(update.message.text)
        if budget < 0:
            await update.message.reply_text("Бюджет не может быть отрицательным. Введите положительное число.")
            return BUDGET
        user_data['budget'] = budget
    except ValueError:
        await update.message.reply_text("Пожалуйста, введите число.")
        return BUDGET

    mood_keyboard = [
        [InlineKeyboardButton("Энергичный", callback_data='энергичный')],
        [InlineKeyboardButton("Веселый", callback_data='веселый')],
        [InlineKeyboardButton("Спокойный", callback_data='спокойный')],
        [InlineKeyboardButton("Грустный", callback_data='грустный')],
        [InlineKeyboardButton("Нейтральный", callback_data='нейтральный')],
        [InlineKeyboardButton("Романтичный", callback_data='романтичный')],
    ]
    reply_markup = InlineKeyboardMarkup(mood_keyboard)
    await update.message.reply_text(
        "Какое у тебя сегодня настроение?",
        reply_markup=reply_markup
    )
    return MOOD


async def mood(update: Update, context) -> int:
    query = update.callback_query
    await query.answer()
    user_data['mood'] = query.data
    await query.edit_message_text(text=f"Настроение: {query.data}")
    await query.message.reply_text("Сколько минут у тебя есть для активности?")
    return FREE_TIME


async def free_time(update: Update, context) -> int:
    try:
        free_time = int(update.message.text)
        if free_time <= 0:
            await update.message.reply_text("Время должно быть положительным числом.")
            return FREE_TIME
        user_data['free_time'] = free_time
    except ValueError:
        await update.message.reply_text("Пожалуйста, введите целое число (минуты).")
        return FREE_TIME

    # Получаем рекомендации
    user_id = update.message.from_user.id
    activities = recommend_activities(
        user_data['budget'],
        user_data['mood'],
        user_data['free_time'],
        user_data['city']
    )

    if not activities:
        await update.message.reply_text("К сожалению, по вашим параметрам активностей не найдено.")
        return ConversationHandler.END

    # Сохраняем рекомендации
    suggestions[user_id] = activities
    context.user_data['current_index'] = 0
    context.user_data['selected'] = []

    return await suggest_activity(update, context)


async def suggest_activity(update: Update, context):
    user_id = update.message.from_user.id if update.message else update.callback_query.from_user.id
    index = context.user_data['current_index']
    activities = suggestions[user_id]

    if index >= len(activities):
        # Показать все активности
        return await show_all_activities(update, context)

    activity = activities[index]
    message = (
        f"Активность {index + 1}/{len(activities)}:\n"
        f"🏷 {activity[1]}\n"
        f"📝 {activity[2]}\n"
        f"💰 Бюджет: {activity[3]}-{activity[4]} руб\n"
        f"⏱ Время: {activity[10]}-{activity[11]} мин"
    )

    keyboard = [
        [InlineKeyboardButton("✅ Выбрать", callback_data=f'select_{index}')],
        [InlineKeyboardButton("➡ Следующая", callback_data='next')],
        [InlineKeyboardButton("📋 Показать все", callback_data='all')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        await update.callback_query.edit_message_text(text=message, reply_markup=reply_markup)
    else:
        await update.message.reply_text(text=message, reply_markup=reply_markup)

    return SUGGESTING


async def handle_suggestion(update: Update, context):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == 'next':
        context.user_data['current_index'] += 1
        return await suggest_activity(update, context)

    elif data.startswith('select_'):
        index = int(data.split('_')[1])
        activity = suggestions[query.from_user.id][index]
        context.user_data['selected'].append(activity)
        context.user_data['current_index'] += 1

        if context.user_data['current_index'] >= len(suggestions[query.from_user.id]):
            return await show_selected(update, context)
        else:
            await query.edit_message_text(text=f"✅ Вы выбрали: {activity[1]}")
            return await suggest_activity(update, context)

    elif data == 'all':
        return await show_all_activities(update, context)


async def show_selected(update: Update, context):
    query = update.callback_query
    selected = context.user_data['selected']

    if not selected:
        await query.edit_message_text("Вы не выбрали ни одной активности.")
        return ConversationHandler.END

    message = "🎉 Вы выбрали:\n\n" + "\n".join(
        f"• {activity[1]}" for activity in selected
    )
    await query.edit_message_text(text=message)
    return ConversationHandler.END


async def show_all_activities(update: Update, context):
    if update.callback_query:
        query = update.callback_query
        user_id = query.from_user.id
    else:
        user_id = update.message.from_user.id

    activities = suggestions[user_id]
    message = "Все подходящие активности:\n\n"
    for i, activity in enumerate(activities):
        message += (
            f"{i + 1}. {activity[1]}\n"
            f"   - {activity[2]}\n"
            f"   - Бюджет: {activity[3]}-{activity[4]} руб\n"
            f"   - Время: {activity[9]}-{activity[10]} мин\n\n"
        )

    if update.callback_query:
        await query.edit_message_text(text=message)
    else:
        await update.message.reply_text(text=message)

    return ConversationHandler.END


async def cancel(update: Update, context) -> int:
    await update.message.reply_text('Диалог прерван.')
    return ConversationHandler.END


def main() -> None:
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, city)],
            BUDGET: [MessageHandler(filters.TEXT & ~filters.COMMAND, budget)],
            MOOD: [CallbackQueryHandler(mood)],
            FREE_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, free_time)],
            SUGGESTING: [CallbackQueryHandler(handle_suggestion)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == '__main__':
    main()