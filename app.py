from flask import Flask, request, render_template, jsonify
import mysql.connector

app = Flask(__name__)

# 데이터베이스 연결 설정
db_config = {
    'host': 'localhost',
    'user': 'root',  # 실제 사용자명으로 변경
    'password': '1234',  # 실제 비밀번호로 변경
    'database': 'recipe_db'
}

@app.route('/')
def search():
    return render_template('search.html')

@app.route('/search', methods=['GET'])
def search_recipes():
    query = request.args.get('query', '').strip()

    if not query:
        return jsonify([])

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        # 재료를 공백으로 구분하여 검색
        sql = "SELECT name, ingredients, youtube_url FROM recipes WHERE ingredients LIKE %s"
        cursor.execute(sql, ('%' + query + '%',))
        results = cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        results = []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

    return jsonify(results)

@app.route('/save', methods=['GET', 'POST'])
def save_recipe():
    message = ''
    if request.method == 'POST':
        name = request.form['name']
        ingredients = request.form['ingredients']
        youtube_url = request.form['youtube_url']

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            sql = "INSERT INTO recipes (name, ingredients, youtube_url) VALUES (%s, %s, %s)"
            cursor.execute(sql, (name, ingredients, youtube_url))
            conn.commit()
            message = '레시피가 성공적으로 저장되었습니다.'
        except mysql.connector.Error as err:
            message = f"오류: {err}"
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    return render_template('save.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)
