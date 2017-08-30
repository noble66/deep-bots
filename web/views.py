# endpoints for trending data
from flask import Flask
app = Flask(__name__)
from flask import request
app.secret_key = 'requiem for a dream'
import flask_login
from flask import redirect
from flask import url_for

import pickle

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_message = u"Please login ...."
login_manager.login_message_category = "info"

with open('users.dict','r') as fr:
    users = pickle.load(fr)

class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['pw'] == users[email]['pw']

    return user

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''<head>
    <link rel="stylesheet"
          href="https://fonts.googleapis.com/css?family=Tangerine">
    <style>
      body {
        font-family: 'Tangerine', serif;
        font-size: 48px;
      }
    </style>
  </head><body>deepwave v1.0 <hr>
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'></input>
                <input type='password' name='pw' id='pw' placeholder='password'></input>
                <input type='submit' name='submit'></input>
               </form></body>
               '''

    email = request.form['email']
    if users.get(email) is None:
	return 'That user does not exist'
    if request.form.get('pw') == users.get(email).get('pw'):
        user = User()
        user.id = email
        flask_login.login_user(user)
        return redirect(url_for('protected'))

    return 'Bad login'+'''<hr><form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'></input>
                <input type='password' name='pw' id='pw' placeholder='password'></input>
                <input type='submit' name='submit'></input>
               </form>'''


@app.route('/login2', methods=['GET', 'POST'])
def login2():
    if request.method == 'GET':
        return '''<head>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Tangerine">
    <link rel="stylesheet" type= "text/css" href= "/static/styles/login.css">


     <style>
      some {
        font-family: 'Tangerine', serif;
        font-size: 48px;
            }

    </style>

  </head>
  <body> <div align="center"> <some>DeepWave 1.0 </some> </div> <hr>

               <div class="container">

                      <h2>Your Mirror is Ready<small>Login</small></h2>

                      <form action='login' method='POST'>

                        <div class="group">
                          <input type="text" name='email' id='email' required>
                          <span class="highlight"></span>
                          <span class="bar"></span>
                          <label>Email</label>
                        </div>

                        <div class="group">
                          <input type="password" name='pw' id='pw' required>
                          <span class="highlight"></span>
                          <span class="bar"></span>
                          <label>Password</label>
                        </div>



                        <input type="submit" name="Submit" class="btn-style" value="Submit" >

                      </form>
                      <br> <br> <br>
        </div>



</body>
               '''

    email = request.form['email']
    if users.get(email) is None:
	return 'That user does not exist'
    if request.form.get('pw') == users.get(email).get('pw'):
        user = User()
        user.id = email
        flask_login.login_user(user)
        return redirect(url_for('protected'))

    return 'Bad login'+'''<hr><form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'></input>
                <input type='password' name='pw' id='pw' placeholder='password'></input>
                <input type='submit' name='submit'></input>
               </form>'''




@app.route('/protected')
@flask_login.login_required
def protected():
    return '''<head>
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Tangerine">
<link rel="stylesheet" type= "text/css" href= "/static/styles/login.css">


 <style>
  some {
    font-family: 'Tangerine', serif;
    font-size: 48px;
        }

</style>

</head>
<body> <div align="center"> <some>DeepWave 1.0 </some> </div> <hr>Logged in as: ''' + flask_login.current_user.id+ '''
<br> <a href="/logout">Logout</a>
<hr>

<div class="container">

 <h2><small>This is version 1 of deep wave...How did you feel today. </small></h2>
 <div class="footer"> Document it. </div>

<br>


</div>
'''

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return '<h2> Logged out </h2> <hr> Want to <a href="/login2">Login</a> again? '

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'


@app.route('/hello/')
def hello():
    #
    return 'hi.. im up. Hit me !!'

if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run(host='0.0.0.0',port = 8081, threaded=True, use_reloader=True)
