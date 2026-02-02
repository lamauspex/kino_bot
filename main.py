""" Файл запуска """

if __name__ == "__main__":
    from bot.app import create_app

    # Создаем приложение и запускаем его корректно
    app = create_app()
    app.run_polling()
