from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from app.db import get_db

bp = Blueprint('reserve', __name__)

@bp.route('/')
def index():
  return render_template('index.html')