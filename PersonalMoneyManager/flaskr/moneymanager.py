from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flask import Flask
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('moneymanager', __name__)


@bp.route('/', methods=['GET'])
def index():
    return render_template('moneymanager/index.html')

@bp.route('/account', methods=['GET'])
def account():
    db = get_db()
    id = request.args.get('id')
    print(id)
    query = '''
    SELECT *
    FROM user
    INNER JOIN conto ON user.id = conto.user_id
    WHERE user.id = ?
    '''
    cursor = db.execute(query, (id,))
    result = cursor.fetchone()
    
    query = '''
    SELECT *
    FROM user
    INNER JOIN transazioni ON user.id = transazioni.user_id
    WHERE user.id = ?
    ORDER BY created DESC
    '''
    cursor = db.execute(query, (id,))
    result1 = cursor.fetchall()
    
    return render_template('moneymanager/account.html', conto = result, transazioni = result1)

@bp.route('/add', methods=['GET'])
def add():
    
    db = get_db()
    soldi = request.args.get('soldi')
    id = request.args.get('id')
    saldo = request.args.get('saldo')
    tot = int(soldi)+int(saldo)
    query = '''
    UPDATE conto SET soldi = ? WHERE user_id = ?
    '''
    db.execute(query, (tot, id,))
    db.commit()
    
    query = '''
    INSERT INTO transazioni (conto_id, user_id, soldi) VALUES (?,?,?)
    '''
    db.execute(query, (id, id, soldi))
    db.commit()
    return redirect(url_for('moneymanager.account', id = id))