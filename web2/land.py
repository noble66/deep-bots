from flask import Flask
app = Flask(__name__)
from flask import request
app.secret_key = 'requiem for a dream'
import flask_login
from flask import redirect
from flask import url_for

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_message = u"Please login ...."
login_manager.login_message_category = "info"

@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email


@app.route('/login1', methods=['GET', 'POST'])
def loin():
    if request.method == 'GET':
        return '''<head>
            	<link rel="stylesheet" type= "text/css" href= "/static/styles/style.css">
            </head>
            <body> <h2> deepwave v1.0 </h2> <hr>
            <form action="login" method="POST">
              <input checked id='signin' name='email' type='radio' value='signin'>
              <label for='signin'>Sign in</label>
              <input id='signup' name='email' type='radio' value='signup'>
              <label for='signup'>Sign up</label>
              <input id='reset' name='action' type='radio' value='reset'>
              <label for='reset'>Reset</label>
              <div id='wrapper'>
                <div id='arrow'></div>
                <input id='email' placeholder='Email' type='text'>
                <input id='pass' placeholder='Password' type='password'>
                <input id='repass' placeholder='Repeat password' type='password'>
              </div>
              <button type='submit'>
                <span>
                  Reset password
                  <br>
                  Sign in
                  <br>
                  Sign up
                </span>
              </button>
            </form>
            <div id='hint'>Click on the tabs, made by sdr</div>
            </body>'''

    email = request.form['email']
    print email
    if users.get(email) is None:
        return 'That User does not exist.'
    if request.form.get('pass') == users.get(email).get('pass'):
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
    return 'Logged in as: ' + flask_login.current_user.id+ '''<hr> <head><link href="https://fonts.googleapis.com/css?family=Sedgwick+Ave" rel="stylesheet"><style>
      p {
        font-family: 'Sedgwick Ave', cursive;
        font-size: 18px;
      }
    </style> </head> <p> This is version 1 of deep wave...How did you feel today. <p> <br> Document it. <br><hr><a href="/logout">Logout</a>'''


@app.route('/login2')
def login2():
    html = '''
    <head>
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons"
      rel="stylesheet">
        <link rel="stylesheet" type= "text/css" href= "/static/styles/stl.css">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js"> </script>
    <script src="static/js/try1.js" </script>
    </head>

    <body>

                <div class="container">
	<form class="signUp">
		<h3>Create Your Account</h3>
		<p>Just enter your email address</br>
and your password for join.
		</p>
		<input class="w100" type="email" placeholder="Insert eMail" reqired autocomplete='off' />
		<input type="password" placeholder="Insert Password" reqired />
		<input type="password" placeholder="Verify Password" reqired />
		<button class="form-btn sx log-in" type="button">Log In</button>
		<button class="form-btn dx" type="submit">Sign Up</button>
	</form>
	<form class="signIn">
		<h3>Welcome</br>Back !</h3>
		<button class="fb" type="button">Log In With Facebook</button>
		<p>- or -</p>
		<input type="email" placeholder="Insert eMail" autocomplete='off' reqired />
		<input type="password" placeholder="Insert Password" reqired />
		<button class="form-btn sx back" type="button">Back</button>
		<button class="form-btn dx" type="submit">Log In</button>
	</form>
</div>
    </body>
    '''
    return html



@app.route('/hello/')
def hello():
    #
    return 'hi.. im up. Hit me !!'

if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run(host='0.0.0.0',port = 8081, threaded=False)
