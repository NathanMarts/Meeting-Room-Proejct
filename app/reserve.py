from flask import (
    Blueprint, abort, render_template, request
)

from app.db import get_db
import dateutil.parser

bp = Blueprint('reserve', __name__)

@bp.route('/')
def index():
  reservations = get_reservations()

  return render_template('index.html', reservations=reservations)

@bp.route('/search', methods=['POST'])
def search():
  search_query = request.form['search']
  conn = get_db()
  cursor = conn.cursor()
  query = '''
  SELECT * FROM reserve 
  WHERE user LIKE ? OR room LIKE ?
  '''
  like_query = '%' + search_query + '%'
  cursor.execute(query, (like_query, like_query))
  resultados = cursor.fetchall()
  
  return render_template('components/table.html', reservations=resultados)

@bp.route('/<int:id>')
def show(id):
  reserve = get_reserve(id)
  return render_template('components/show.html', reserve=reserve)

@bp.route('/', methods=["POST"])
def store():
  user = request.form['user']
  room = request.form['room']
  date_time = dateutil.parser.parse(request.form['date'] + " " + request.form['time'])
  error = None

  if not (user or room or date_time):
      error = {
         user: '' if user else 'Campo Obrigatório.',
         room: '' if room else 'Campo Obrigatório.',
         date_time: '' if date_time else 'Campo Obrigatório.'
      }

  if alreadyReserved(room, date_time):
     error = "Sala já reservada nessa data e hora!"

  if error is not None:
      return error, 400
  else:
      db = get_db().cursor()
      db.execute(
          'INSERT INTO reserve (user, room, date_time)'
          ' VALUES (?, ?, ?)',
          (user, room, date_time)
      )
      get_db().commit()
      newReserve = get_reserve(db.lastrowid)
  
  return render_template('components/newReserveRow.html', reserve=newReserve)

@bp.route('/<int:id>', methods=["DELETE"])
def destroy(id):
  get_reserve(id)
  db = get_db()
  db.execute('DELETE FROM reserve WHERE id = ?', (id,))
  db.commit()

  return '', 200

def get_reserve(id):
    reserve = get_db().execute(
        'SELECT *'
        ' FROM reserve'
        ' WHERE id = ?',
        (id,)
    ).fetchone()

    if reserve is None:
        abort(404, f"reserve id {id} doesn't exist.")

    return reserve

def get_reservations():
  reservations = get_db().execute(
    'SELECT *'
    ' FROM reserve'
  ).fetchall()
  
  return reservations

def alreadyReserved(room, dateTime):
  db = get_db()
  result = db.execute(
    'SELECT *'
    ' FROM reserve'
    ' WHERE  room = ? AND date_time = ?',
    (room, dateTime,)
  ).fetchone()

  return result is not None
