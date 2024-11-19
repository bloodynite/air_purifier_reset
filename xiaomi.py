import logging
import hashlib
import os
import re
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

# Configuración del logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Estados de la conversación
WAITING_FOR_UUID, WAITING_FOR_BLOCK = range(2)

# Valor por defecto para el bloque 4
DEFAULT_BLOCK_4 = "00 00 4A 44 00 00 41 30 00 20 11 16 00 48 49 34"

# Token del bot desde variable de entorno
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable is not set")

def validate_uuid(uuid_str: str) -> bool:
    """Validate UUID format and characters."""
    uuid_clean = uuid_str.replace(":", "").replace(" ", "")
    if len(uuid_clean) != 14:
        return False
    hex_pattern = re.compile(r'^[0-9a-fA-F]+$')
    return bool(hex_pattern.match(uuid_clean))

def validate_block_4(block_4: str) -> bool:
    """Validate block 4 format and characters."""
    bytes_list = [b for b in block_4.split() if b]
    if len(bytes_list) != 16:
        return False
    hex_pattern = re.compile(r'^[0-9a-fA-F]{2}$')
    return all(hex_pattern.match(byte) for byte in bytes_list)

def process_uuid_to_bytes(uuid_hex: str, block_4_hex: str) -> list:
    """Process UUID and generate NFC commands with input validation."""
    try:
        if not validate_uuid(uuid_hex):
            return ["Error: UUID inválido. Debe ser 7 bytes en formato hexadecimal."]
        
        if not validate_block_4(block_4_hex):
            return ["Error: Bloque 4 inválido. Debe ser 16 bytes en formato hexadecimal separados por espacios."]

        uid_bytes = bytearray.fromhex(uuid_hex.replace(":", "").replace(" ", ""))
        sha1_hash = hashlib.sha1(uid_bytes).hexdigest()
        
        first_byte_decimal = int(sha1_hash[:2], 16)
        indices = [
            first_byte_decimal % 20,
            (first_byte_decimal + 5) % 20,
            (first_byte_decimal + 13) % 20,
            (first_byte_decimal + 17) % 20,
        ]
        
        hash_bytes = [sha1_hash[i:i+2] for i in range(0, len(sha1_hash), 2)]
        extracted_bytes = [hash_bytes[index] for index in indices]
        base_nfc_command = f"1B{''.join(extracted_bytes)},3008"
        
        block_4_bytes = block_4_hex.split()
        commands = [f"A204{''.join(block_4_bytes)}"]
        for block in range(5, 9):
            commands.append(f"A2{block:02X}00000000")
        
        messages = []
        messages.append("📝 *Comandos generados:*")
        messages.append(f"*Comando completo (una línea):*")
        messages.append(f"`{base_nfc_command}," + ",".join(commands) + "`")
        messages.append("*Comandos separados (más fáciles de copiar):*")
        messages.append(f"• Base NFC:")
        messages.append(f"`{base_nfc_command}`")
        for i, command in enumerate(commands, 4):
            messages.append(f"Bloque {i}:")
            messages.append(f"`{base_nfc_command},{command}`")
        
        return messages
    
    except Exception as e:
        logging.error(f"Error processing data: {str(e)}")
        return ["Error interno procesando los datos. Por favor, verifica el formato de entrada."]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Initialize the conversation and request UUID."""
    await update.message.reply_text(
        "¡Hola! Por favor, envíame el UUID en formato hexadecimal.\n"
        "Ejemplo: 04:69:62:e2:58:70:80\n"
        "Debe ser exactamente 7 bytes (14 caracteres hex)."
    )
    logging.info(f"New conversation started with user {update.effective_user.id}")
    return WAITING_FOR_UUID

async def handle_uuid(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle and validate UUID input."""
    uuid = update.message.text.strip()
    
    if not validate_uuid(uuid):
        await update.message.reply_text(
            "UUID inválido. Debe ser 7 bytes en formato hexadecimal.\n"
            "Ejemplo: 04:69:62:e2:58:70:80\n"
            "Por favor, intenta nuevamente."
        )
        return WAITING_FOR_UUID
    
    context.user_data["uuid"] = uuid
    await update.message.reply_text(
        "UUID válido recibido.\n"
        "Ahora envíame el bloque 4 en formato hexadecimal (16 bytes separados por espacios).\n"
        "Ejemplo: 00 00 4A 44 00 00 41 30 00 20 11 16 00 48 49 34\n"
        "O envía 0 para usar el valor por defecto."
    )
    logging.info(f"Valid UUID received from user {update.effective_user.id}: {uuid}")
    return WAITING_FOR_BLOCK

async def handle_block(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle and validate block 4 input."""
    block_4_input = update.message.text.strip()
    
    if not block_4_input or block_4_input == "0":
        block_4_input = DEFAULT_BLOCK_4
    
    uuid = context.user_data.get("uuid")
    if not uuid:
        await update.message.reply_text("Error de sesión. Por favor, inicia nuevamente con /start")
        logging.error(f"Session error for user {update.effective_user.id}: UUID not found in context")
        return ConversationHandler.END
    
    results = process_uuid_to_bytes(uuid, block_4_input)
    for message in results:
        await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
    
    logging.info(f"Commands generated for user {update.effective_user.id}")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel the conversation."""
    await update.message.reply_text(
        "Operación cancelada. Usa /start para comenzar nuevamente."
    )
    logging.info(f"Conversation cancelled by user {update.effective_user.id}")
    return ConversationHandler.END

def main() -> None:
    """Initialize and run the bot."""
    try:
        application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
        
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", start)],
            states={
                WAITING_FOR_UUID: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_uuid)],
                WAITING_FOR_BLOCK: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_block)],
            },
            fallbacks=[CommandHandler("cancel", cancel)],
        )
        
        application.add_handler(conv_handler)
        logging.info("Bot initialized and ready to receive messages")
        application.run_polling()
        
    except Exception as e:
        logging.critical(f"Failed to start bot: {str(e)}")
        raise

if __name__ == "__main__":
    main()
