from flask import (
    Blueprint, abort, flash, g, redirect, render_template, request, session, url_for
)

from app.db import get_db

bp = Blueprint('reserve', __name__)

@bp.route('/')
def index():
  reservations = get_db().execute(
    'SELECT * FROM reserve'
  )
  return render_template('index.html', reservations=reservations)

@bp.route('/<int:id>')
def show(id):
  reserve = get_reserve(id)
  return render_template('index.html', reserve=reserve)

@bp.route('/create', methods=["POST"])
def store():
  user = request.form['user']
  room = request.form['room']
  date_time = request.form['date_time']
  error = None

  if not (user or room or date_time):
      error = {
         user: '' if user else 'Campo Obrigatório.',
         room: '' if room else 'Campo Obrigatório.',
         date_time: '' if date_time else 'Campo Obrigatório.'
      }

  if error is not None:
      flash(error)
  else:
      db = get_db()
      db.execute(
          'INSERT INTO reserve (user, room, date_time)'
          ' VALUES (?, ?, ?)',
          (user, room, date_time)
      )
      db.commit()
  
  return redirect(url_for('index.html'))

@bp.route('/<int:id>', methods=["DELETE"])
def destroy(id):
  get_reserve(id)
  db = get_db()
  db.execute('DELETE FROM reserve WHERE id = ?', (id,))
  db.commit()
  return render_template('index.html')

def get_reserve(id):
    reserve = get_db().execute(
        'SELECT * FROM reserve WHERE p.id = ?',
        (id,)
    ).fetchone()

    if reserve is None:
        abort(404, f"reserve id {id} doesn't exist.")

    return redirect(url_for('index.html'))