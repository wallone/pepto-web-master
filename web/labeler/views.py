from flask import *
from . import labeler
import sqlite3 as lite
from functools import wraps


# Function that makes sure that the user is logged in before accessing certain page
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Please login first.')
            return redirect(url_for('labeler.login'))
    return wrap


# Index of the labeler website
@labeler.route('/')
def index():
    return render_template('labeler/index.html')


# One of the project for the labeler website
@labeler.route('/gi', methods=['GET', 'POST'])
@login_required
def gi():
    # Connects to the database
    con = lite.connect('pepto.db')

    # Create option variables to later get the following data with POST method
    tw_options = ['tw_0', 'tw_1', 'tw_2', 'tw_3', 'tw_4']
    tw_id_options = ['tw_id_0', 'tw_id_1', 'tw_id_2', 'tw_id_3', 'tw_id_4']
    run_id_options = ['run_0', 'run_1', 'run_2', 'run_3', 'run_4']
    classification = []

    # Fetches data from the database
    with con:
        cur = con.cursor()

        # Selects random values that are not already classified
        cur.execute('SELECT * FROM tweets WHERE tweetid NOT IN(SELECT tweetid FROM count)'
                    ' ORDER BY rowid LIMIT 5')
        data = cur.fetchall()
        ids = [dat[0] for dat in data]
        for i in range(len(ids)):
            count_data = []
            count_data.append(ids[i])
            count_data.append(1)
            cur.executemany('INSERT INTO count(tweetid, count) VALUES (?, ?)', (count_data,))

    # Convert tuple list into String list of Tweet_IDs
    tweet_ids = [dat[0] for dat in data]

    # Convert tuple list into String list of Run_IDs
    run_ids = [dat[1] for dat in data]

    # Convert tuple list into String list of Tweets
    tweets = [dat[2] for dat in data]

    length = len(tweets)

    # If user requests more tweets
    if request.method == 'POST':
        for i in range(length):
            # If the tweet was classified
            if request.form[str(i)] != '':
                # puts the data into the database
                classification.append(request.form[str(tw_id_options[i])])
                classification.append(request.form[run_id_options[i]])
                classification.append(request.form[str(i)])
                classification.append('TESTCLASS')
                classification.append(1)
                with con:
                    cur.executemany('INSERT INTO classification(tweetid, runid, label_data, class, conf) VALUES '
                                    '(?, ?, ?, ?, ?)', (classification,))
                classification[:] = []


    # Closes the database before returning
    con.close()

    return render_template('labeler/gi.html', tweets=tweets, tweet_ids=tweet_ids, run_ids=run_ids, length=length,
                           tw_options=tw_options, tw_id_options=tw_id_options, run_id_options=run_id_options, count_data=count_data)


@labeler.route('/chd')
@login_required
def soon():
    return render_template('labeler/chd.html')


# Login page of the labeler website
@labeler.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    # Connects to the database
    con = lite.connect('user_info.db')

    # Gets all existing user data from the database
    with con:
        cur = con.cursor()
        cur.execute('SELECT * FROM user')
        users = cur.fetchall()

    # If user tries to login
    if request.method == 'POST':
        # Check if the credential matches.
        for user in users:
            # If username and password does not match, update error message
            if request.form['username'] != user[1] or request.form['password'] != user[2]:
                error = 'Invalid credentials. Please try again.'
            # Else set logged in session to be true and redirect user to index
            else:
                session['logged_in'] = request.form['username']
                return redirect(url_for('labeler.index'))

    return render_template('labeler/login.html',error=error)


# Logout function. Pops the logged in session
@labeler.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('labeler.login'))


# Register page for the labeler website
@labeler.route('/register', methods=['GET', 'POST'])
def register():
    error = None

    # Connects to the database
    con = lite.connect('user_info.db')

    # Gets existing usernames from the database
    with con:
        cur = con.cursor()
        cur.execute('SELECT username FROM user')
        usernames = cur.fetchall()
        usernames = [username[0] for username in usernames]

    # If user tries to register
    if request.method == 'POST':
        # If username already exists, change error message and then return
        for username in usernames:
            if username == request.form['username']:
                error = 'Username Already exists'
                con.close()
                return render_template('labeler/register.html', error=error)

        # If one of the fields are empty, change error message and set availability to false
        if request.form['name'] == '' or request.form['username'] == '' or request.form['password'] == '' or request.form['email'] == '':
            error = 'Please fill in every section'
            available = False
        # available variable is only true if all the fields are filled and username is unique
        else:
            available = True

        # if available, then puts the user information to the database and redirect user to the login page
        if available:
            user_info = [request.form['name'], request.form['username'], request.form['password'],
                         request.form['email']]
            cur.executemany('INSERT INTO user(name, username, password, email) VALUES (?, ?, ?, ?)', (user_info,))
            con.commit()
            con.close()
            return redirect(url_for('labeler.login'))

    # Close the database before exiting
    con.close()
    return render_template('labeler/register.html', error=error)
