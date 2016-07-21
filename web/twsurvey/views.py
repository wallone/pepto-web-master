
from flask import  Flask, request, redirect, url_for, session, g, flash, render_template
import sqlite3


from . import twsurvey

from . import config_key

from flask_oauth import OAuth
import os


# configuration
SECRET_KEY = config_key.SECRET_KEY
DEBUG = True

app = twsurvey
app.debug = DEBUG
app.secret_key = SECRET_KEY
oauth = OAuth()


# Use Twitter as example remote application
twitter = oauth.remote_app('twitter',
    # unless absolute urls are used to make requests, this will be added
    # before all URLs.  This is also true for request_token_url and others.
    base_url='https://api.twitter.com/1.1/',
    # where flask should look for new request tokens
    request_token_url='https://api.twitter.com/oauth/request_token',
    # where flask should exchange the token with the remote application
    access_token_url='https://api.twitter.com/oauth/access_token',
    # twitter knows two authorizatiom URLs.  /authorize and /authenticate.
    # they mostly work the same, but for sign on /authenticate is
    # expected because this will give the user a slightly different
    # user interface on the twitter side.
    authorize_url='https://api.twitter.com/oauth/authenticate',
    # the consumer keys from the twitter application registry.
    consumer_key=config_key.consumer_key,
    consumer_secret=config_key.consumer_secret
)


@twsurvey.route('/')
def home():
    return render_template('twsurvey/index.html')


@twsurvey.route('/submit',methods=['POST'])
def submit():

    conn = sqlite3.connect('pepto.db')
    with conn:
        cur = conn.cursor()
        cur.execute('INSERT INTO Survey(account,handle,gender,age,education,houseHoldIncome,favoriteFoods,employed,publicWork,zipcode,status,ethnicity) '
                         'VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',
                         (request.form['account'],request.form['handle'],request.form['gender'],request.form['Age'],request.form['education'],request.form['houseHoldIncome'],request.form['favoriteFoods'],request.form['employed'],request.form['publicWork'],request.form['zipCode'],request.form['status'],request.form['ethnicity']))

    conn.close()
    return render_template('twsurvey/index.html')


@twitter.tokengetter
def get_twitter_token(token=None):
    return session.get(config_key.access_key)


@app.route('/')
def index():
    access_token = session.get(config_key.access_key)
    if access_token is None:
        return redirect(url_for('twsurvey.login'))

    access_token = access_token[0]

    return render_template('index.html')


@app.route('/login',methods=['GET', 'POST'])
def login():
    return twitter.authorize(callback=url_for('twsurvey.oauth_authorized',
                                              next=request.args.get('next') or request.referrer or None))


@app.route('/getinfo',methods=['GET', 'POST'])
def getinfo():

    session.pop('screen_name', None)
    flash('You were signed out')
    return redirect(request.referrer or url_for('twsurvey.index'))


@app.route('/logout')
def logout():
    session.pop('screen_name', None)
    flash('You were signed out')
    return redirect(request.referrer or url_for('twsurvey.index'))


@app.route('/oauth-authorized')
@twitter.authorized_handler
def oauth_authorized(resp):
    next_url = request.args.get('next') or url_for('twsurvey.index')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    access_token = resp['oauth_token']
    session['access_token'] = access_token
    session['screen_name'] = resp['screen_name']


    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )


    return redirect(url_for('twsurvey.index'))


if __name__ == '__main__':
    app.run()