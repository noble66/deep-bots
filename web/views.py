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

with open('/home/ubuntu/deep-bots/web/users.dict','r') as fr:
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


@app.route('/why', methods=['GET', 'POST'])
def why():
    html = '''
    working on This
    '''
    return html



@app.route('/login', methods=['GET', 'POST'])
def login():
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
    <script async src='https://pepper.swat.io/embed.js?eyJwb3NpdGlvbiI6InJpZ2h0IiwiY29sb3IiOiJGNjcyODAiLCJjdXN0b21Db2xvciI6ZmFsc2UsImljb24iOiJwYWNtYW4iLCJwcm9ub3VuIjoibWUiLCJsYW5ndWFnZSI6ImVuIiwiYnJhbmRlZCI6ZmFsc2UsImludHJvVGV4dCI6IkhleSAtIGxldHMgdGFsayBhbmQgZmlndXJlIHRoaXMgdGhpbmcgb3V0IHRvZ2V0aGVyIiwiY2hhbm5lbHMiOltbInR3aXR0ZXIiLCJfcm95c2QiLCJzb2NpYWwiXSxbIm1lc3NlbmdlciIsImZpcmVrbmlnaHQiLCJzb2NpYWwiXSxbInNuYXBjaGF0IiwibmRvcjkiLCJzb2NpYWwiXSxbInBob25lIiwiKzU3MzIyODg0OTciLCJjbGFzc2ljIl0sWyJlbWFpbCIsInJveS5kYXRhMTdAZ21haWwuY29tIiwiY2xhc3NpYyJdXX0='></script>
  </head>
  <body>  <div class="container"><div align="center"> <some>DeepWave 1.0 </some> </div> <hr>



                      <h2>Your Mirror is Ready<small>.</small></h2>

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



                        <input type="submit" name="Submit" class="btn-style" value="Login" >

                      </form>
                      <br> <br> <br>
        </div>



        </body>
               '''

    email = request.form['email']
    print email
    if users.get(email) is None:
	    return 'That user does not exist'
    print request.form.get('pw')
    if request.form.get('pw') == users.get(email).get('pw'):
        user = User()
        user.id = email
        flask_login.login_user(user)
        return redirect(url_for('protected'))

    return 'Bad login'+'''<hr><form action='login2' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'></input>
                <input type='password' name='pw' id='pw' placeholder='password'></input>
                <input type='submit' name='submit'></input>
               </form>'''


@app.route('/menu')
@flask_login.login_required
def menu():
    html = '''


<head>
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Tangerine">
<link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css">
<link rel="stylesheet" href="/static/styles/menu.css">
<style>
 some {
   font-family: 'Tangerine', serif;
   font-size: 48px;
       }

</style>
<script async src='https://pepper.swat.io/embed.js?eyJwb3NpdGlvbiI6InJpZ2h0IiwiY29sb3IiOiJGNjcyODAiLCJjdXN0b21Db2xvciI6ZmFsc2UsImljb24iOiJwYWNtYW4iLCJwcm9ub3VuIjoibWUiLCJsYW5ndWFnZSI6ImVuIiwiYnJhbmRlZCI6ZmFsc2UsImludHJvVGV4dCI6IkhleSAtIGxldHMgdGFsayBhbmQgZmlndXJlIHRoaXMgdGhpbmcgb3V0IHRvZ2V0aGVyIiwiY2hhbm5lbHMiOltbInR3aXR0ZXIiLCJfcm95c2QiLCJzb2NpYWwiXSxbIm1lc3NlbmdlciIsImZpcmVrbmlnaHQiLCJzb2NpYWwiXSxbInNuYXBjaGF0IiwibmRvcjkiLCJzb2NpYWwiXSxbInBob25lIiwiKzU3MzIyODg0OTciLCJjbGFzc2ljIl0sWyJlbWFpbCIsInJveS5kYXRhMTdAZ21haWwuY29tIiwiY2xhc3NpYyJdXX0='></script>

</head>
<body>
<div align="center"> <some>DeepWave 1.0 </some> </div> <hr>
<div align="right"> Logged in as: ''' + flask_login.current_user.id+ '''
<br> <a href="/logout">Logout</a> </div>
<hr>

<br> <br> <br> <br>
<nav class="menu">
  <input type="checkbox" href="#" class="menu-open" name="menu-open" id="menu-open"/>
  <label class="menu-open-button" for="menu-open">
    <span class="hamburger hamburger-1"></span>
    <span class="hamburger hamburger-2"></span>
    <span class="hamburger hamburger-3"></span>
  </label>

  <a href="http://www.sumandebroy.com" class="menu-item"> <i class="fa fa-bar-chart"></i> </a>
  <a href="/dataentry" class="menu-item"> <i class="fa fa-plus"></i> </a>
  <a href="#" class="menu-item"> <i class="fa fa-heart"></i> </a>
  <a href="#" class="menu-item"> <i class="fa fa-envelope"></i> </a>
  <a href="#" class="menu-item"> <i class="fa fa-cog"></i> </a>
  <a href="#" class="menu-item"> <i class="fa fa-ellipsis-h"></i> </a>

</nav>


<!-- filters -->
<svg xmlns="http://www.w3.org/2000/svg" version="1.1">
    <defs>
      <filter id="shadowed-goo">

          <feGaussianBlur in="SourceGraphic" result="blur" stdDeviation="10" />
          <feColorMatrix in="blur" mode="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 18 -7" result="goo" />
          <feGaussianBlur in="goo" stdDeviation="3" result="shadow" />
          <feColorMatrix in="shadow" mode="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1 -0.2" result="shadow" />
          <feOffset in="shadow" dx="1" dy="1" result="shadow" />
          <feComposite in2="shadow" in="goo" result="goo" />
          <feComposite in2="goo" in="SourceGraphic" result="mix" />
      </filter>
      <filter id="goo">
          <feGaussianBlur in="SourceGraphic" result="blur" stdDeviation="10" />
          <feColorMatrix in="blur" mode="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 18 -7" result="goo" />
          <feComposite in2="goo" in="SourceGraphic" result="mix" />
      </filter>
    </defs>
</svg>
</body>
'''
    return html


@app.route('/dataentry')
@flask_login.login_required
def dataentry():
    html = '''

<head>
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Tangerine">
<link rel="stylesheet" href="/static/styles/dataform.css">
<link rel="stylesheet" href="/static/styles/loading.css">
<style>
 some {
   font-family: 'Tangerine', serif;
   font-size: 48px;
       }

</style>

</head>
<body>

<div align="center"> <some>DeepWave 1.0 </some> </div> <hr>
<div align="right"> Logged in as: ''' + flask_login.current_user.id+ '''
<br> <a href="/logout">Logout</a> </div>
<hr>
<form>
  <h1>Interaction Logger! <span>This is how it begins. Your interactions are logged, so we can tell you how to change yourself and others!!</span></h1>
  <div class="controls">
      <h1>Check Boxes</h1>
    <input id='check-1' type="checkbox" name='check-1' checked='checked' />
    <label for="check-1">Apples</label>

     <input id='check-2' type="checkbox" name='check-1' />
    <label for="check-2">Oranges</label>
  </div>


  <div class="controls">
      <h1>Radio Boxes</h1>
    <input id='radio-1' type="radio" name='r-group-1' checked='checked' />
    <label for="radio-1">Day</label>

    <input id='radio-2' type="radio" name='r-group-1' />
    <label for="radio-2">Night</label>
  </div>

  <div class="controls">
     <h1>Toggles</h1>
    <input class='toggle' type="checkbox" name='check-3' checked='checked' />
    <input class='toggle' type="checkbox" name='check-4' />
  </div>
</form>

<h1> <span> Done? Go back to <a href="menu"> Menu </a> 

<div class="loadingcontent">
    <div class="load-wrapp">
        <div class="load-9" align="center">
                <div class="spinner" align="center">
                    <div class="bubble-1"></div>
                    <div class="bubble-2"></div>
                 </div>
        </div>
    </div>
</div>
    '''
    return html


@app.route('/protected')
@flask_login.login_required
def protected():
    return '''<head>
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Tangerine">
<link rel="stylesheet" type= "text/css" href= "/static/styles/login.css">
<link rel="stylesheet" href="/static/styles/menu.css">

 <style>
  some {
    font-family: 'Tangerine', serif;
    font-size: 48px;
        }

</style>

<script async src='https://pepper.swat.io/embed.js?eyJwb3NpdGlvbiI6InJpZ2h0IiwiY29sb3IiOiJGNjcyODAiLCJjdXN0b21Db2xvciI6ZmFsc2UsImljb24iOiJwYWNtYW4iLCJwcm9ub3VuIjoibWUiLCJsYW5ndWFnZSI6ImVuIiwiYnJhbmRlZCI6ZmFsc2UsImludHJvVGV4dCI6IkhleSAtIGxldHMgdGFsayBhbmQgZmlndXJlIHRoaXMgdGhpbmcgb3V0IHRvZ2V0aGVyIiwiY2hhbm5lbHMiOltbInR3aXR0ZXIiLCJfcm95c2QiLCJzb2NpYWwiXSxbIm1lc3NlbmdlciIsImZpcmVrbmlnaHQiLCJzb2NpYWwiXSxbInNuYXBjaGF0IiwibmRvcjkiLCJzb2NpYWwiXSxbInBob25lIiwiKzU3MzIyODg0OTciLCJjbGFzc2ljIl0sWyJlbWFpbCIsInJveS5kYXRhMTdAZ21haWwuY29tIiwiY2xhc3NpYyJdXX0='></script>
</head>
<body>

<div align="center"> <some>DeepWave 1.0 </some> </div> <hr>
<div align="right"> Logged in as: ''' + flask_login.current_user.id+ '''
<br> <a href="/logout">Logout</a> </div>
<hr>

<div class="container">

 <h2>This is version 1 of deep wave...How did your interactions go today?  </h2>
 <h1 align = "center"> <a href="/menu"> Document It. </a> </h1>
 <br> <br><br><br>
 <div class="footer"> . </div>
<br>

</div>


'''

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return '<h2> Logged out </h2> <hr> Want to <a href="/login">Login</a> again? '

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
