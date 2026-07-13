import os
import psycopg2
from psycopg2.extras import DictCursor
from flask import Flask, render_template, g, request, redirect, url_for, session, Response, make_response
import datetime

app = Flask(__name__)
app.secret_key = 'castle_lab_secret_key_2026'
ADMIN_PASSWORD = 'Egorb20095658'

# Получаем ссылку на базу из настроек Render
DATABASE_URL = os.environ.get(
    'DATABASE_URL',
    'postgresql://postgres:Egorb20095658@db.dfersqopzrbqzivclgae.supabase.co:5432/postgres'
)

def get_db():
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=DictCursor)
    return conn

@app.route('/')
def index():
    db = get_db()
    cur = db.cursor()

    cur.execute('SELECT * FROM pages WHERE url_path = %s', ('/',))
    page_data = cur.fetchone()

    cur.execute('SELECT * FROM services')
    services_list = cur.fetchall()

    cur.execute('SELECT * FROM portfolio')
    portfolio_list = cur.fetchall()

    cur.execute('SELECT * FROM steps ORDER BY step_num ASC')
    steps_list = cur.fetchall()

    cur.execute('SELECT * FROM tech_categories')
    tech_list = cur.fetchall()

    cur.close()
    db.close()

    return render_template('index.html', page=page_data, services=services_list,
                           portfolio=portfolio_list, steps=steps_list, tech=tech_list)

@app.route('/services/<slug>')
def service_detail(slug):
    db = get_db()
    cur = db.cursor()

    cur.execute('SELECT * FROM pages WHERE url_path = %s', ('/',))
    page_data = cur.fetchone()

    cur.execute('SELECT * FROM services WHERE slug = %s', (slug,))
    service = cur.fetchone()

    cur.execute('SELECT * FROM portfolio ORDER BY id DESC LIMIT 3')
    portfolio_projects = cur.fetchall()

    cur.execute('SELECT * FROM service_benefits ORDER BY id ASC')
    benefits_list = cur.fetchall()

    cur.close()
    db.close()

    if service is None:
        return "Послугу не знайдено", 404

    return render_template('service.html', service=service, portfolio=portfolio_projects,
                           page=page_data, benefits=benefits_list)

def is_logged_in():
    return session.get('admin_logged_in') == True

# --- Вход в админку ---
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if is_logged_in():
        return redirect(url_for('admin_dashboard'))
    error = None
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            error = "Невірний пароль!"
    return render_template('admin_login.html', error=error)

# --- Выход ---
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

# --- Главная страница админки ---
@app.route('/admin')
def admin_dashboard():
    if not is_logged_in():
        return redirect(url_for('admin_login'))

    db = get_db()
    cur = db.cursor()

    cur.execute('SELECT * FROM pages WHERE url_path = %s', ('/',))
    page = cur.fetchone()

    cur.execute('SELECT * FROM services')
    services = cur.fetchall()

    cur.execute('SELECT * FROM portfolio ORDER BY id DESC')
    portfolio = cur.fetchall()

    cur.execute('SELECT * FROM steps ORDER BY id ASC')
    steps = cur.fetchall()

    cur.execute('SELECT * FROM tech_categories ORDER BY id ASC')
    tech = cur.fetchall()

    cur.execute('SELECT * FROM service_benefits ORDER BY id ASC')
    benefits = cur.fetchall()

    cur.close()
    db.close()

    return render_template('admin_dashboard.html', page=page, services=services,
                           portfolio=portfolio, steps=steps, tech=tech, benefits=benefits)
# --- РОУТ ROBOTS.TXT ---
@app.route('/robots.txt')
def robots():
    content = """User-agent: *
Disallow: /admin
Disallow: /admin/
Allow: /

Sitemap: https://castle-lab.top/sitemap.xml
"""
    return Response(content, mimetype='text/plain')

# --- РОУТ SITEMAP.XML ---
@app.route('/sitemap.xml')
def sitemap():
    db = get_db()
    cur = db.cursor()
    base_url = "https://castle-lab.top"
    today = datetime.date.today().isoformat()

    pages = [{"loc": f"{base_url}/", "lastmod": today, "changefreq": "daily", "priority": "1.0"}]

    cur.execute('SELECT slug FROM services')
    services = cur.fetchall()
    for service in services:
        pages.append({
            "loc": f"{base_url}/services/{service['slug']}",
            "lastmod": today,
            "changefreq": "weekly",
            "priority": "0.8"
        })

    cur.close()
    db.close()

    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for page in pages:
        xml_content += '  <url>\n'
        xml_content += f'    <loc>{page["loc"]}</loc>\n'
        xml_content += f'    <lastmod>{page["lastmod"]}</lastmod>\n'
        xml_content += f'    <changefreq>{page["changefreq"]}</changefreq>\n'
        xml_content += f'    <priority>{page["priority"]}</priority>\n'
        xml_content += '  </url>\n'
    xml_content += '</urlset>'

    response = make_response(xml_content)
    response.headers["Content-Type"] = "application/xml"
    return response


