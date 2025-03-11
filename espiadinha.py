import nest_asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import asyncio
from telegram.error import TimedOut, Forbidden

# Permite reutilizar o loop de eventos
nest_asyncio.apply()

# ID do canal VIP
CHANNEL_ID = -1002212704190

# Função para gerar o link de convite para o canal VIP com tentativas
async def generate_invite_link(context: CallbackContext, retries=3):
    for attempt in range(retries):
        try:
            invite_link = await context.bot.create_chat_invite_link(chat_id=CHANNEL_ID, member_limit=1)
            return invite_link.invite_link
        except TimedOut as e:
            print(f"Tentativa {attempt + 1} falhou: {e}")
            await asyncio.sleep(2 ** attempt)
        except Exception as e:
            print(f"Erro inesperado na tentativa {attempt + 1}: {e}")
            await asyncio.sleep(2 ** attempt)
    raise Exception("Falha ao gerar link de convite após múltiplas tentativas")

# Função para o comando /start
async def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    first_name = user.first_name if user.first_name else "usuário"
    user_id = user.id

    try:
        invite_link = await generate_invite_link(context)
        await update.message.reply_text(f"Olá {first_name}😍\nMe chamo Alice, sou suporte da Hotflix Brasil e vou te auxiliar a partir daqui")
        await asyncio.sleep(2)  # Adiciona o delay de 2 segundos
        await update.message.reply_text("Você foi presenteado com um teste grátis do nosso canal VIP com 3 minutos de acesso para desfrutar de tudo🔥🔥\nAproveite!!!")
        await asyncio.sleep(2)  # Adiciona o delay de 2 segundos
        await update.message.reply_text(f"Entre aqui: {invite_link}")
        await asyncio.sleep(2)  # Adiciona o delay de 2 segundos
        asyncio.create_task(handle_user_access(update, context, user_id))
    except Exception as e:
        await update.message.reply_text(f"Erro ao gerar link de convite: {e}")

# Função para gerenciar o tempo de acesso de cada usuário
async def handle_user_access(update: Update, context: CallbackContext, user_id):
    await asyncio.sleep(10)  # 3 minutos
    await remove_user_from_channel(update, context, user_id)

    try:
        await update.message.reply_text("Seu período de teste acabou 💔")
        await asyncio.sleep(2)  # Adiciona o delay de 2 segundos
        await update.message.reply_text("Para continuar acessando assine o canal VIP 🌟")
        await asyncio.sleep(2)  # Adiciona o delay de 2 segundos
        await update.message.reply_text("Clique no botão abaixo e continue com a nossa experiência gostosa 👇")
        await asyncio.sleep(2)  # Adiciona o delay de 2 segundos
        await update.message.reply_text("https://t.me/bot")

        # Após 15 minutos
        await asyncio.sleep(900)
        await update.message.reply_text("Oi amor, conseguiu se inscrever? 🫣")
        await asyncio.sleep(2)  # Adiciona o delay de 2 segundos
        await update.message.reply_text("Não perca mais tempo, clica no botão abaixo e finalize a assinatura 👇")
        await asyncio.sleep(2)  # Adiciona o delay de 2 segundos
        await update.message.reply_text("https://t.me/bot")
        await asyncio.sleep(2)  # Adiciona o delay de 2 segundos
        await update.message.reply_text("tô te esperando no VIP 💕")
        await update.message.reply_text("Se você já assinou, desconsidere essa mensagem 🤭")

        # Após mais 15 minutos (30 minutos no total)
        await asyncio.sleep(900)
        await update.message.reply_text("Parece que você ainda não entrou no VIP ☹️")
        await asyncio.sleep(2)  # Adiciona o delay de 2 segundos
        await update.message.reply_text("Tudo bem, não guardo ressentimento, continue se divertindo no Grupo Grátis 💕")
        await asyncio.sleep(2)  # Adiciona o delay de 2 segundos
        await update.message.reply_text("https://t.me/previas")
        await asyncio.sleep(2)  # Adiciona o delay de 2 segundos
        await update.message.reply_text("Clica aqui e seja feliz 👆")
    except Forbidden:
        print(f"Bot foi bloqueado pelo usuário {user_id}")
    except Exception as e:
        print(f"Erro ao enviar mensagens de acompanhamento: {e}")

# Função para remover o usuário do canal
async def remove_user_from_channel(update: Update, context: CallbackContext, user_id):
    try:
        print(f"Tentando remover o usuário {user_id} do canal...")
        await context.bot.ban_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
    except Exception as e:
        print(f"Erro ao remover o usuário {user_id}: {e}")

# Função principal para rodar o bot
async def main():
    token = '8068745600:AAGoX4QS36XHK-V7PiF6pX3idkj5pWDN1NQ'  # Substitua pelo seu token de bot
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    print("Bot está rodando...")
    await application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except (KeyboardInterrupt, SystemExit):
        pass
