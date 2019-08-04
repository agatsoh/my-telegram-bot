### Simple Telegram chatbot
This is a simple telegram chatbot using bottle framework and ngrok
You need to have a json file in the root with your telegram bot token
```
{
  "telegram_token" : "your telegram bot token"
}
```
### Raiden Payments Bot
This is a payment bot to showcase raiden micropayments using flask,
raiden api's, telegram api's. You should atleast have one channel open
then you can transfer to your immediate neighbour node or any one of the
interconnected nodes.
Run this to start your raiden bot
```
python raiden_bot.py
```
Just run to start the http, https forwarding service
```
./ngrok http 8080
```
