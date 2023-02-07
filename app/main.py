from flask import Blueprint, render_template, flash, redirect, url_for, request, session
from app.models import URL
from app.forms import URLForm
from . import db
from hashids import Hashids

main = Blueprint('main', __name__)

@main.route('/')
def index():
    url_form = URLForm()

    hash = None

    if 'hash' in session:
        hash = session['hash']
        del session['hash']
    
    return render_template('index.html', url_form = url_form, hash=hash)

@main.route('/', methods=["POST"])
def index_post():
    url_form = URLForm()
    
    if not url_form.validate_on_submit():
        flash('You should pass proper link.')
        return redirect(url_for('main.index'))

    original_url = url_form.data["url"]

    hash = create_entry_in_db(original_url)

    hash = request.base_url + hash
    session['hash'] = hash

    return redirect(url_for('main.index'))

def create_entry_in_db(original_url):
    last_row = URL.query.order_by(URL.id.desc()).first()

    if not last_row:
        id = 1
    else:
        id = last_row.id + 1
    
    hash = generate_hash(id)
    url_object = URL(id=id, original_link=original_url, hash=hash)
    db.session.add(url_object)
    db.session.commit()

    return hash

def generate_hash(id):
    hashid = Hashids("salt", 8, "qwertyuioplkjhgfdsamnbvcxzqwertyuioplkjhgfdsazxcvbnm09877654321")
    hash = hashid.encode(id)
    return hash

@main.route('/<short_url>')
def url_access(short_url):
    url = URL.query.filter_by(hash = short_url).first()
    if url is None:
        flash('Link does not exist.')
        return redirect(url_for('main.index'))
    return redirect(url.original_link)