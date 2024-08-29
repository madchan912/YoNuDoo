from flask import Flask, request, render_template, jsonify
import mysql.connector

app = Flask(__name__)

# python app.py 시작 명령어

# 데이터베이스 연결 설정
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'recipe_db'
}

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
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            sql = "INSERT INTO recipes (name, ingredients, youtube_url) VALUES (%s, %s, %s)"
            cursor.execute(sql, (name, ingredients, youtube_url))
            conn.commit()
            return jsonify(success=True, message='레시피가 성공적으로 저장되었습니다.')
        except mysql.connector.Error as err:
            return jsonify(success=False, message=f"오류: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    return render_template('save.html')

@app.route('/search')
def search_recipes():
    query = request.args.get('q', '')
    results = []

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        if query:
            # 검색어가 있을 때
            sql = """
                SELECT name, ingredients, youtube_url 
                FROM recipes 
                WHERE name LIKE %s OR ingredients LIKE %s
            """
            cursor.execute(sql, ('%' + query + '%', '%' + query + '%'))
        else:
            # 검색어가 없을 때 모든 레시피 반환
            sql = "SELECT name, ingredients, youtube_url FROM recipes"
            cursor.execute(sql)

        results = cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"오류: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

    return jsonify(results=results)


if __name__ == '__main__':
    app.run(debug=True)
