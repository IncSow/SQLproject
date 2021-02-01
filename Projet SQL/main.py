# Serveur Python

# 1 - on importe les librairies dont on a besoin
# flask est le framework web
from flask import Flask, render_template
# sqlite pour faire du sqlite :)
import sqlite3

database_path = "data/songify.db"

# 2 - on instancie notre app flask
app = Flask('app', template_folder='views')

# 3 - on définit les pages

# .. sur la page d'accueil


@app.route('/')
def home_page():
    conn = sqlite3.connect(database_path)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    results = cursor.execute(
        "SELECT * FROM Songs LEFT JOIN Albums on Albums.id = Songs.Albums_id LEFT Join Singers on Singers.id = Songs.Singers_id LEFT JOIN Categories on Categories.id = Albums.Categories_id")

    return render_template('index.html', all_songs=results)




# .. sur l'url d'un film


@app.route('/song/<id>')
def Songs_page(id):
    conn = sqlite3.connect(database_path)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    # en réalité cette approche est dangereuse (-> injections SQL)
    # mais dans un souci de simplicité on le garde comme ça :)
    result = cursor.execute("SELECT * FROM Songs LEFT JOIN Albums on Albums.id = Songs.Albums_id Join Singers on Singers.id = Songs.Singers_id LEFT JOIN Categories on Categories.id = Albums.Categories_id WHERE Songs.id=" +id)

    result = result.fetchone()

    return render_template('song.html', Song=result)


@app.route('/singer/<id>')
def singer_page(id):
    conn = sqlite3.connect(database_path)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    # en réalité cette approche est dangereuse (-> injections SQL)
    # mais dans un souci de simplicité on le garde comme ça :)
    singer = cursor.execute("SELECT * FROM Singers WHERE Singers.id = " + id)
    singer = singer.fetchone()

    albums = cursor.execute("SELECT *, Categories.name as category_name FROM Singers LEFT JOIN Albums on Albums.singers_id = Singers.id LEFT JOIN Categories on Categories.id = Albums.Categories_id WHERE Singers.id = " + id)

    return render_template('singer.html', singer=singer, albums=albums)



@app.route('/artists/')
def artists_page():
    conn = sqlite3.connect(database_path)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    results = cursor.execute(
        "SELECT DISTINCT * FROM Singers")

    return render_template('singers.html', all_artists=results)

# 4 - on lance notre serveur web
app.run(host='localhost', port=3000, debug=True)

