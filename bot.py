from telegram import Update, LabeledPrice, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, PreCheckoutQueryHandler

TOKEN = '7593052075:AAGz7CEyC_wPcI8yUYv_1CEEqC3SibDbFO0'
PROVIDER_TOKEN = 'TEST-b26531a8-7cb9-42d0-ab4c-e0e17d802a12'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('¡Hola! Soy tu bot de ventas. Envía /comprar para ver nuestras fotos y videos.')

def comprar(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Selecciona una opción para comprar:')
    update.message.reply_text('/foto1 - Foto 1\n/video1 - Video 1\n/foto_mujeres - Foto Mujeres')

def foto1(update: Update, context: CallbackContext) -> None:
    prices = [LabeledPrice('Foto 1', 500)]
    context.bot.send_invoice(update.effective_chat.id, title='Foto 1', description='Compra de Foto 1',
                             payload='foto1', provider_token=PROVIDER_TOKEN, start_parameter='test',
                             currency='USD', prices=prices)

def video1(update: Update, context: CallbackContext) -> None:
    prices = [LabeledPrice('Video 1', 1000)]
    context.bot.send_invoice(update.effective_chat.id, title='Video 1', description='Compra de Video 1',
                             payload='video1', provider_token=PROVIDER_TOKEN, start_parameter='test',
                             currency='USD', prices=prices)

def foto_mujeres(update: Update, context: CallbackContext) -> None:
    prices = [LabeledPrice('Foto Mujeres', 800)]
    context.bot.send_invoice(update.effective_chat.id, title='Foto Mujeres', description='Compra de Foto Mujeres',
                             payload='foto_mujeres', provider_token=PROVIDER_TOKEN, start_parameter='test',
                             currency='USD', prices=prices)

def precheckout_callback(update: Update, context: CallbackContext) -> None:
    query = update.pre_checkout_query
    if query.invoice_payload not in ['foto1', 'video1', 'foto_mujeres']:
        query.answer(ok=False, error_message="Algo salió mal...")
    else:
        query.answer(ok=True)

def successful_payment_callback(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Pago recibido, gracias. Aquí tienes tu archivo:')
    if update.message.successful_payment.invoice_payload == 'foto1':
        context.bot.send_document(chat_id=update.effective_chat.id, document=InputFile('path/to/your/photo1.jpg'))
    elif update.message.successful_payment.invoice_payload == 'video1':
        context.bot.send_document(chat_id=update.effective_chat.id, document=InputFile('path/to/your/video1.mp4'))
    elif update.message.successful_payment.invoice_payload == 'foto_mujeres':
        context.bot.send_document(chat_id=update.effective_chat.id, document=InputFile('path/to/your/photo_mujeres.jpg'))

def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("comprar", comprar))
    dispatcher.add_handler(CommandHandler("foto1", foto1))
    dispatcher.add_handler(CommandHandler("video1", video1))
    dispatcher.add_handler(CommandHandler("foto_mujeres", foto_mujeres))
    dispatcher.add_handler(PreCheckoutQueryHandler(precheckout_callback))
    dispatcher.add_handler(MessageHandler(Filters.successful_payment, successful_payment_callback))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
