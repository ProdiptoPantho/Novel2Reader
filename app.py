from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, send_file, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from forms import RegistrationForm, LoginForm, SearchForm
from models import db, User, TempLink
from flask_migrate import Migrate
import signal
from crawler import OneKissNovelCrawler  # Ensure this import is correct
import subprocess  # Import subprocess for running shell commands
import glob
import os
import shutil
import time
import logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a strong secret key
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    return render_template('home.html')  # Create a home.html template if needed


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:  # Use hashed passwords in production
            login_user(user)
            return redirect(url_for('search'))
        flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()  # This logs out the current user
    flash('You have been logged out.', 'success')  # Optional: Flash a message
    return redirect(url_for('login'))  # Redirect to the login page


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    results = []
    if form.validate_on_submit():
        query = form.query.data
        crawler = OneKissNovelCrawler()  # Create an instance of the OneKissNovelCrawler
        results.extend(crawler.search_novel(query))# Use the crawler to search for novels
    return render_template('search.html', form=form, results=results)


@app.route('/download', methods=['Get', 'POST'])
@login_required
def download():
    if request.method == 'POST':
        link = request.form["link"]
        novel_name = request.form['novel_name']
        chapter_range = request.form['chapter_range']
        chapter_range = chapter_range.replace('-', ' - ')
        cr = chapter_range.replace('-', ' ')
        format = request.form['format']

        # Generate a more descriptive name for the output directory
        timestamp = int(time.time())  # Get the current timestamp
        name = f"novel_{timestamp}"  # Create a name based on the timestamp
        downloads_dir = os.path.normpath(os.path.join(f"C:\\Novel2Reader\\download", name, "epub"))  # Normalize the path

        

        # Create the output directory
        os.makedirs(downloads_dir, exist_ok=True)

        # Run the lnrawl command
        try:
            command = f'lncrawl -s "{link}" --range {cr} --format {format} -o "{downloads_dir}" --suppress'
            print(f"Running command: {command}")  # Debugging statement
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            return render_template('download.html', error=f'Download failed: {e}')

        # Adjust the path to the nested EPUB directory
        nested_epub_dir = os.path.join(downloads_dir, "epub")  # Adjusted path to the nested epub directory

        # Find the EPUB file in the nested directory
        epub_files = glob.glob(os.path.join(nested_epub_dir, "*.epub"))

        if epub_files:
            zipfile = epub_files[0]  # Get the first EPUB file found

            # Upload to temp.sh
            upload_url = upload_to_temp_sh(zipfile)

            # Store the link and expiration date in the database
            expiration_date = datetime.now() + timedelta(days=3)  # Set expiration to 7 days from now
            
            store_link_in_db(upload_url, chapter_range, expiration_date, current_user.id, novel_name)

            response = send_file(zipfile, as_attachment=True)  # Serve the file directly for download

            # Cleanup the downloads directory after serving the file
            

            return response
        else:
            cleanup_previous_downloads(r'C:\Novel2Reader\download')  # Cleanup if no file found
            return render_template('download.html', error='No EPUB files found in the output directory.')




def upload_to_temp_sh(zipfile):
    try:
        # Upload the file
        result = subprocess.run(
            ['curl', '-F', f'file=@{zipfile}', 'https://temp.sh/upload'],
            capture_output=True,
            text=True,
            check=True
        )

        # Save the link to a variable (simulating database)
        upload_link = result.stdout.strip() if result.stdout else None
        return upload_link
    except subprocess.CalledProcessError as e:
        return None
    except Exception as e:
        return None


def store_link_in_db(link, chapter_range, expiration_date, user_id, novel_name):
    """Store the upload link and its expiration date in the database, linked to a user."""
    new_link = TempLink(novel_name=novel_name, chapter_range=chapter_range, link=link, expiration_date=expiration_date, user_id=user_id)
    db.session.add(new_link)
    db.session.commit()



def get_all_temp_links():
    try:
        temp_links = TempLink.query.all()
        return temp_links
    except Exception as e:
        print(f"Error retrieving temp links: {e}")
        return []


def cleanup_expired_links():
    """Remove expired links from the database."""
    expired_links = TempLink.query.filter(TempLink.expiration_date < datetime.utcnow()).all()
    for link in expired_links:
        db.session.delete(link)
    db.session.commit()


def cleanup_previous_downloads(directory):
    """Remove the specified directory if it exists."""
    if os.path.exists(directory):
        print(f"Cleaning up previous downloads in: {directory}")  # Debugging statement
        shutil.rmtree(directory)

def signal_handler(sig, frame):
    cleanup_previous_downloads(r'C:\Novel2Reader\download')
    os._exit(0)
    
signal.signal(signal.SIGINT, signal_handler)


@app.route('/temp_links', methods=['GET'])
@login_required
def temp_links():
    # Retrieve all temporary links from the database
    links = TempLink.query.filter_by(user_id=current_user.id).all()
    return render_template('temp_links.html', links=links)  # Pass links to the template


migrate = Migrate(app, db)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Initialize the database
    app.run(debug=True)