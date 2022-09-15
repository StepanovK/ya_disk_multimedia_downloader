# Скрипт для автоскачивания фото и видео с яндекс диска

# Настройка

Для использования требуется:

1. Получить токен, перейдя и авторизовавшись по
   ссылке: https://oauth.yandex.ru/authorize?response_type=token&client_id=bb153a621888486bbd37256bbe8a1430

2. Создать виртуальное окружение
   ```
   Python -m venv venv
   venv/Scripts/activate
   ```

3. Установить необходимые пакеты
   ```
   pyp install -r requirements.txt
   ```

4. Создать в каталоге со скриптом файл `.env`, скопировав и переименовав файл `.envEXAMPLE`

## Переменные `.env` файла:

- `TOKEN_YD` - ваш токен
- `PATH_YD` - путь к папке на компьютере, куда будут сохраняться файлы
- `DAYS_BEFORE_CLEANING` - количество дней до очистки
