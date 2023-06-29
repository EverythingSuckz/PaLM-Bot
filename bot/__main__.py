import bot

if __name__ == "__main__":
    import bot.handlers
    bot.executor.start_polling(bot.dp, skip_updates=True)