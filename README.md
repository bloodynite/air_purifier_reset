Aquí tienes un ejemplo de `README.md` para tu programa:

```markdown
# Telegram NFC Command Generator Bot

Este es un bot de Telegram que genera comandos NFC basados en un UUID y un bloque de datos en formato hexadecimal proporcionados por el usuario.

## Características

- Valida y procesa un UUID de 7 bytes en formato hexadecimal.
- Valida y procesa un bloque de datos hexadecimal de 16 bytes.
- Genera comandos NFC a partir de las entradas del usuario.
- Devuelve los comandos generados en mensajes separados, con títulos y contenido bien formateados.

## Requisitos

- Python 3.8 o superior.
- Librerías necesarias: `python-telegram-bot`.
- Un token de bot de Telegram configurado como variable de entorno `TELEGRAM_BOT_TOKEN`.

## Instalación

1. Clona este repositorio:

   ```bash
   git clone https://github.com/tu_usuario/telegram-nfc-bot.git
   cd telegram-nfc-bot
   ```

2. Instala las dependencias:

   ```bash
   pip install python-telegram-bot==20.3
   ```

3. Configura la variable de entorno `TELEGRAM_BOT_TOKEN` con el token de tu bot de Telegram.

   ```bash
   export TELEGRAM_BOT_TOKEN="tu-token-aquí"
   ```

4. Ejecuta el programa:

   ```bash
   python bot.py
   ```

## Uso

1. Inicia el bot en Telegram con el comando `/start`.
2. Envía un UUID en formato hexadecimal. Ejemplo:
   ```
   04:69:62:e2:58:70:80
   ```
3. Envía un bloque de datos en formato hexadecimal (16 bytes separados por espacios). Ejemplo:
   ```
   00 00 4A 44 00 00 41 30 00 20 11 16 00 48 49 34
   ```
   - Si deseas usar el valor por defecto, simplemente envía `0`.

4. El bot generará y enviará los comandos NFC en mensajes separados.

## Mensajes del bot

- **UUID inválido**: Si el UUID proporcionado no es válido, el bot pedirá que se reenvíe en el formato correcto.
- **Bloque inválido**: Si el bloque de datos no es válido, el bot pedirá que se reenvíe en el formato correcto.
- **Comandos generados**: Los comandos NFC generados serán enviados con títulos y contenido separados para facilitar su lectura.

## Ejemplo de salida

1. Mensaje de inicio:
   ```
   📝 *Comandos generados:*
   ```

2. Comando completo:
   ```
   *Comando completo (una línea):*
   `1B...,...`
   ```

3. Comandos separados:
   ```
   *Comandos separados (más fáciles de copiar):*
   • Base NFC:
   `1B...`
   
   Bloque 4:
   `1B...,A204...`
   ```

## Cancelación

Puedes cancelar la operación en cualquier momento enviando el comando `/cancel`.

## Desarrollo y contribución

Si deseas contribuir a este proyecto:

1. Crea un fork de este repositorio.
2. Haz tus cambios en una rama nueva.
3. Envía un pull request con una descripción detallada de tus cambios.

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.

## Contacto

Para dudas o soporte, puedes contactarme en [tu_email@dominio.com](mailto:tu_email@dominio.com).
``` 

Este `README.md` proporciona una descripción clara del programa, cómo usarlo, y los pasos necesarios para configurarlo y ejecutarlo. Si necesitas incluir más detalles específicos, avísame y lo actualizo.
