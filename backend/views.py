from flask import Blueprint, render_template, send_file, flash, redirect, url_for, session
from .models import Image, User
from .models import db
from io import BytesIO
from .forms import LoginForm, RegistrationForm, LogoutForm, DeleteImageForm
from flask import current_app, request, abort
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from PIL import Image as PilImage
import os
from flask_login import current_user

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_thumbnail(image_path):
    with PilImage.open(image_path) as img:
        img.thumbnail((200, 200))
        base, ext = os.path.splitext(image_path)
        img.save(f"{base}.thumb{ext}")

bp = Blueprint('main', __name__)

@bp.route("/", methods=['GET'])
def photos():
    categories = ['nature', 'animals', 'cities', 'people', 'abstract']
    selected_category = request.args.get('category', default = categories[0], type = str).lower()  # Convert selected category to lowercase
    images = Image.query.all()  # Query all images
    images = [image for image in images if image.category.lower() == selected_category]  # Filter images by category in a case-insensitive way
    return render_template("photos.html", current_page="photos", categories=categories, images=images, selected_category=selected_category)

@bp.route("/about")
def about():
    return render_template("about.html", current_page="about")

@bp.route("/login", methods=['GET', 'POST'])
def login():
    print("login route hit with:", request.form)
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):  # Use the check_password method
            login_user(user)
            flash('Logged in successfully.', 'succes')
            return redirect(url_for('main.photos'))
        else:
            flash('Invalid username or password.', 'error')
    else:
        print("Form validation failed with errors:", form.errors)
    return render_template("login.html", current_page="login", form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    print("register route hit wth:", request.form)
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter(User.username == form.username.data).first()
        existing_email = User.query.filter(User.email == form.email.data).first()
        if existing_user:
            flash('A user with that username already exists.', 'error')
        elif existing_email:
            flash('A user with that email already exists.', 'error')
        else:
            new_user = User(username=form.username.data, email=form.email.data)
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('main.login'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {field}: {error}", 'error')
    return render_template('register.html', title='Register', form=form)


@bp.route("/logout", methods=['POST'])
def logout():
    form = LogoutForm()
    if form.validate_on_submit():
        logout_user()
        return redirect(url_for('main.photos'))
    return redirect(url_for('main.profile'))


@bp.route("/upload", methods=['GET', 'POST'])
@login_required
def upload():
    csrf_token = session.get('csrf_token')
    if request.method == 'POST':
        if 'image' not in request.files:
            #flash('No file part')
            return redirect(request.url)
        file = request.files['image']
        name = request.form.get('name')  # Only use the provided name
        if not name:  # If no name was provided, show an error
            #flash('No name provided')
            return redirect(request.url)
        category = request.form.get('category', 'Uncategorized')  # Use the provided category or 'Uncategorized'
        if file.filename == '':
            #flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            new_image = Image(name=name, category=category, data=file.read(), user=current_user)
            db.session.add(new_image)
            db.session.commit()
            return redirect(url_for('main.photos'))
    return render_template("upload.html", current_page="upload")

@bp.route('/images/', methods=['POST'])
def create_image():
    if 'file' not in request.files:
        #flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    name = request.form.get('name')  # Get the name from the form data
    if not name:  # If no name was provided, show an error
        #flash('No name provided')
        return redirect(request.url)
    category = request.form.get('category')  # Get the category from the form data
    if file.filename == '':
        #flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        new_image = Image(name=name, data=file.read(), category=category, user=current_user)  # Set the name and category
        db.session.add(new_image)
        db.session.commit()
        return redirect(url_for('main.photos'))
    
    
@bp.route('/images/<int:image_id>')
def read_image(image_id):
    image = Image.query.get(image_id)
    return send_file(BytesIO(image.data), mimetype='image/jpeg')

@bp.route("/profile")
@login_required
def profile():
    form = LogoutForm()
    images = Image.query.filter_by(user_id=current_user.id).all()  # Query images associated with the current user
    delete_image_form = DeleteImageForm()
    return render_template("profile.html", delete_image_form=delete_image_form, current_page="profile", form=form, images=images)

@bp.route('/images/<int:image_id>/delete', methods=['POST'])
@login_required
def delete_image(image_id):
    image = Image.query.get(image_id)
    if image.user != current_user:
        abort(403)  # Forbidden, the current user does not own this image
    db.session.delete(image)
    db.session.commit()
    #flash('Your image has been deleted!', 'success')
    return redirect(url_for('main.photos'))

@bp.route('/statistics')
def statistics():
    total_images = Image.query.count()
    total_users = User.query.count()
    images_per_category = db.session.query(Image.category, db.func.count(Image.id)).group_by(Image.category).all()
    images_per_category_dict = [{ 'category': row[0], 'count': row[1] } for row in images_per_category]
    return render_template('statistics.html', total_images=total_images, total_users=total_users, images_per_category=images_per_category_dict, current_page='statistics')