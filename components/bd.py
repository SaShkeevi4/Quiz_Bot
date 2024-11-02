import aiosqlite
# Зададим имя базы данных

DB_NAME = 'quiz_bot.db'

async def get_quiz_index(user_id):
     # Подключаемся к базе данных
     async with aiosqlite.connect(DB_NAME) as db:
        # Получаем запись для заданного пользователя
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = (?)', (user_id, )) as cursor:
            # Возвращаем результат
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0

async def update_quiz_index(user_id, index, correct_answer):
    # Создаем соединение с базой данных (если она не существует, она будет создана)
    async with aiosqlite.connect(DB_NAME) as db:
        # Вставляем новую запись или заменяем ее, если с данным user_id уже существует
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index, correct_answer) VALUES (?, ?, ?)', (user_id, index, correct_answer))
        # Сохраняем изменения
        await db.commit()


async def create_table():
    # Создаем соединение с базой данных (если она не существует, она будет создана)
    async with aiosqlite.connect(DB_NAME) as db:
        # Создаем таблицу
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, question_index INTEGER)''')

        # Сохраняем изменения
        await db.commit()

        async with db.execute(f"PRAGMA table_info({'quiz_state'});") as cursor:
            columns = await cursor.fetchall()  # Получаем все результаты

            # Выводим информацию о колонках
            print(f"Колонки в таблице '{'quiz_state'}':")
            for column in columns:
                column_id, column_name, data_type, not_null, default_value, primary_key = column
                print(f"- {column_name} (Тип: {data_type}, NOT NULL: {not_null}, DEFAULT: {default_value}, PRIMARY KEY: {primary_key})")


async def get_quiz_index(user_id):
     # Подключаемся к базе данных
     async with aiosqlite.connect(DB_NAME) as db:
        # Получаем запись для заданного пользователя
        async with db.execute('SELECT question_index, correct_answer FROM quiz_state WHERE user_id = (?)', (user_id, )) as cursor:
            # Возвращаем результат
            results = await cursor.fetchone()
            if results is not None:
                return results[0],results[1]
            else:
                return 0