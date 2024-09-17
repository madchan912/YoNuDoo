import sqlite3
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# python app.py 시작 명령어

# SQLite는 파일 경로만 필요합니다.
db_file = 'recipe_db.sqlite'  # 데이터베이스 파일 이름

@app.route('/')
def search():
    return render_template('search.html')

@app.route('/save', methods=['GET', 'POST'])
def save_recipe():
    if request.method == 'POST':
        name = request.form['name']
        ingredients = request.form['ingredients']
        youtube_url = request.form['youtube_url']

        try:
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            sql = "INSERT INTO recipes (name, ingredients, youtube_url) VALUES (?, ?, ?)"
            cursor.execute(sql, (name, ingredients, youtube_url))
            conn.commit()
            return jsonify(success=True, message='레시피가 성공적으로 저장되었습니다.')
        except sqlite3.Error as err:
            return jsonify(success=False, message=f"오류: {err}")
        finally:
            if conn:
                cursor.close()
                conn.close()

    return render_template('save.html')

@app.route('/search')
def search_recipes():
    query = request.args.get('q', '')
    results = []

    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        if query:
            # 검색어가 있을 때
            sql = """
                SELECT name, ingredients, youtube_url 
                FROM recipes 
                WHERE name LIKE ? OR ingredients LIKE ?
            """
            cursor.execute(sql, ('%' + query + '%', '%' + query + '%'))
        else:
            # 검색어가 없을 때 모든 레시피 반환
            sql = "SELECT name, ingredients, youtube_url FROM recipes"
            cursor.execute(sql)

        # 데이터 딕셔너리 형태로 변환
        results = [dict(name=row[0], ingredients=row[1], youtube_url=row[2]) for row in cursor.fetchall()]
    except sqlite3.Error as err:
        print(f"오류: {err}")
    finally:
        if conn:
            cursor.close()
            conn.close()

    return jsonify(results=results)

@app.route('/init_db')
def init_db():
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        # 테이블 생성 SQL
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                ingredients TEXT NOT NULL,
                youtube_url TEXT NOT NULL
            )
        ''')
        conn.commit()
        return "데이터베이스가 초기화되었습니다!"
    except sqlite3.Error as err:
        return f"오류: {err}"
    finally:
        if conn:
            cursor.close()
            conn.close()


if __name__ == '__main__':
    app.run(debug=True)
