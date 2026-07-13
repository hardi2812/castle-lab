import os
import psycopg2

# Твоя строка подключения к Supabase (без квадратных скобок вокруг пароля!)
DATABASE_URL = os.environ.get(
    'DATABASE_URL', 
    'postgresql://postgres:Egorb20095658@db.dfersqopzrbqzivclgae.supabase.co:5432/postgres'
)

def init_db():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    # 1. Таблица базовых страниц
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pages (
            id SERIAL PRIMARY KEY,
            url_path TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            meta_description TEXT,
            h1 TEXT NOT NULL,
            subtitle TEXT,
            content TEXT,
            contact_url TEXT,
            avatar_img TEXT
        )
    ''')

    # 2. Таблица услуг
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS services (
            id SERIAL PRIMARY KEY,
            slug TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            short_description TEXT NOT NULL,
            full_description TEXT,
            icon_svg TEXT,
            meta_title TEXT,
            meta_description TEXT
        )
    ''')

    # 3. Таблица портфолио
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS portfolio (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            stack TEXT NOT NULL,
            image_url TEXT,
            project_url TEXT
        )
    ''')

    # 4. Таблица преимуществ
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS service_benefits (
            id SERIAL PRIMARY KEY,
            badge TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL
        )
    ''')

    # 5. Таблица шагов работы
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS steps (
            id SERIAL PRIMARY KEY,
            step_num TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL
        )
    ''')

    # 6. Таблица категорий технологического стека
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tech_categories (
            id SERIAL PRIMARY KEY,
            icon TEXT NOT NULL,
            title TEXT NOT NULL,
            tags TEXT NOT NULL
        )
    ''')

    # Заполняем данные главной страницы (ON CONFLICT обновляет данные, если запись '/' уже есть)
    main_page_data = (
        '/',
        'CASTLE LAB | Розробка Telegram ботів та Web App',
        'Професійна розробка Telegram ботів на Python. Автоматизація бізнесу, Web App рішення, інтеграція платежів та крипти.',
        'Розробка Telegram ботів та Web App рішень для бізнесу',
        'Python • Telegram Bots • Web Apps',
        'Створюю швидкі, стабільні та автономні рішення на Python. Автоматизація рутину, інтеграція платежів, крипти та створення повноцінних інтерфейсів прямо всередині Telegram.',
        'https://t.me/tgbotegor',
        'avatar.jpg'
    )
    cursor.execute('''
        INSERT INTO pages (url_path, title, meta_description, h1, subtitle, content, contact_url, avatar_img)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (url_path) DO UPDATE SET
            title = EXCLUDED.title,
            meta_description = EXCLUDED.meta_description,
            h1 = EXCLUDED.h1,
            subtitle = EXCLUDED.subtitle,
            content = EXCLUDED.content,
            contact_url = EXCLUDED.contact_url,
            avatar_img = EXCLUDED.avatar_img
    ''', main_page_data)

    # Услуги
    services_data = [
        (
            'sales-bot',
            'Магазини & Web Apps',
            'Повноцінні інтернет-магазини прямо всередині Telegram. Сучасні Web App інтерфейси, кошик, вибір товарів та повна імітація сайту.',
            'Створюю сучасні Web App інтерфейси для Telegram, які повністю замінюють звичайні сайти. Користувачі купують товари, оформлюють підписки та проводять оплати в один клік, не виходячи з месенджера. Бекенд будується на FastAPI або Flask з надійною базою даних.',
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>',
            'Розробка Telegram Магазинів та Web Apps | Castle Lab',
            'Замовити розробку Telegram Web App магазину під ключ на Python. Зручний каталог, кошик та оплата в один клік.'
        ),
        (
            'admin-bot',
            'Автоматизація & CRM',
            'Автоматизація рутинних процесів вашого бізнесу. Розумні боти для модерації чатів, автопостингу, збору заявок та інтеграції з будь-якими CRM.',
            'Автоматизую рутину будь-якої складності. Створюю ботів для управління бізнес-процесами: автоматичний прийом заявок, підключення до CRM (Bitrix24, AmoCRM), автоматична модерація чатів і каналів, парсинг даних та автопостинг контенту за розкладом.',
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>',
            'Автоматизація Бізнесу та CRM Боти в Telegram | Castle Lab',
            'Професійна розробка Telegram ботів для автоматизації процесів, інтеграції з CRM системами та збору заявок.'
        ),
        (
            'crypto-bot',
            'Крипто-інтеграції & Оплати',
            'Автоматичний прийом платежів у фіаті та криптовалюті (USDT, USDC, TON). Безпечні автовиплати через API, реферальні системи та фінансовий облік.',
            'Розробляю надійні платіжні рішення. Інтегрую прийом фіатних карток, а також крипто-платежів через офіційні API (Crypto Pay, Mono, WayForPay). Бот вміє самостійно перевіряти транзакції, нараховувати баланси та робити автоматичні виплати.',
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>',
            'Прийом Оплат та Крипто-Інтеграції в Telegram | Castle Lab',
            'Підключення автоматичного прийому платежів та криптовалюти (USDT, TON) у Telegram ботах. Надійні виплати та безпека.'
        )
    ]
    for service in services_data:
        cursor.execute('''
            INSERT INTO services (slug, title, short_description, full_description, icon_svg, meta_title, meta_description) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (slug) DO UPDATE SET
                title = EXCLUDED.title,
                short_description = EXCLUDED.short_description,
                full_description = EXCLUDED.full_description,
                icon_svg = EXCLUDED.icon_svg,
                meta_title = EXCLUDED.meta_title,
                meta_description = EXCLUDED.meta_description
        ''', service)

    # Портфолио
    cursor.execute('''
        INSERT INTO portfolio (id, title, description, stack, image_url, project_url)
        VALUES (
            1,
            'Crypto Pay Bot & Автоматичні Виплати',
            'Багатофункціональна крипто-система в Telegram. Бот реалізує автоматичний прийом платежів через Crypto Pay API, безпечні виплати користувачам, багаторівневу реферальну систему, гнучку адмін-панель для управління балансами та автоматичний парсинг курсів валют. Повністю автономний бекенд з базою даних.',
            'Python, aiogram, Crypto Pay API, SQLite, aiohttp',
            'crypto_project.jpg',
            'https://t.me/tgbotegor'
        )
        ON CONFLICT (id) DO UPDATE SET
            title = EXCLUDED.title,
            description = EXCLUDED.description,
            stack = EXCLUDED.stack,
            image_url = EXCLUDED.image_url,
            project_url = EXCLUDED.project_url
    ''')

    # Преимущества
    cursor.execute('TRUNCATE TABLE service_benefits RESTART IDENTITY CASCADE')
    benefits_data = [
        ('Логіка', 'Повний функціонал', 'Продумані сценарії роботи, інтеграція з API та повна автоматизація рутинних дій.'),
        ('База даних', 'Надійне збереження', 'Проектування архітектури БД на SQLite або PostgreSQL для швидкої роботи без збоїв.'),
        ('Сервер', 'Запуск «під ключ»', 'Допомога з купівлею та налаштуванням VPS, деплой бота та безкоштовний моніторинг.')
    ]
    for benefit in benefits_data:
        cursor.execute('INSERT INTO service_benefits (badge, title, description) VALUES (%s, %s, %s)', benefit)

    # Шаги работы
    cursor.execute('TRUNCATE TABLE steps RESTART IDENTITY CASCADE')
    steps_data = [
        ('01', 'Обговорення та ТЗ', 'Аналізуємо задачу, прописуємо детальний сценарій роботи бота та погоджуємо технологічний стек.'),
        ('02', 'Розробка та Тести', 'Пишу чистий асинхронний код на Python, проектую базу даних та проводжу детальне тестування.'),
        ('03', 'Деплой та Підтримка', 'Розгортаю проект на надійному VPS-сервері, підключаю моніторинг та консультую з усіх питань.')
    ]
    for step in steps_data:
        cursor.execute('INSERT INTO steps (step_num, title, description) VALUES (%s, %s, %s)', step)

    # Категории стека
    cursor.execute('TRUNCATE TABLE tech_categories RESTART IDENTITY CASCADE')
    tech_data = [
        ('🤖', 'Бекенд & Боти', 'Python, aiogram, FastAPI, Flask, aiohttp, Celery'),
        ('💾', 'Бази даних', 'SQLite, PostgreSQL, SQLAlchemy, aiosqlite, Redis'),
        ('⚙️', 'Деплой & Інструменти', 'Git, Docker, Linux (Ubuntu), Nginx, Systemd, VPS')
    ]
    for tech in tech_data:
        cursor.execute('INSERT INTO tech_categories (icon, title, tags) VALUES (%s, %s, %s)', tech)

    conn.commit()
    cursor.close()
    conn.close()
    print("База даних PostgreSQL на Supabase успішно ініціалізована та заповнена!")

if __name__ == '__main__':
    init_db()