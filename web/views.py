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
	    return redirect(url_for('badlogin'))
    print request.form.get('pw')
    if request.form.get('pw') == users.get(email).get('pw'):
        user = User()
        user.id = email
        flask_login.login_user(user)
        return redirect(url_for('protected'))

    return redirect(url_for('badlogin'))

@app.route('/badlogin')
def badlogin():
    html = '''<head>
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

                  <h2>Bad Login. <a href = "/login">Try Again. </a> <small></small></h2>

    </body>'''
    return html


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

  <a href="/charting" class="menu-item"> <i class="fa fa-bar-chart"></i> </a>
  <a href="/dataentry" class="menu-item"> <i class="fa fa-plus"></i> </a>
  <a href="/icounts" class="menu-item"> <i class="fa fa-heart"></i> </a>
  <a href="#" class="menu-item"> <i class="fa fa-envelope"></i> </a>
  <a href="#" class="menu-item"> <i class="fa fa-cog"></i> </a>
  <a href="levels" class="menu-item"> <i class="fa fa-ellipsis-h"></i> </a>

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

@app.route('/levels')
@flask_login.login_required
def levels():
    html = '''
            <head>
                <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Tangerine">
                <link rel="stylesheet" href="/static/styles/levels.css">


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

            	<div class="container group">
		<div class="grid-1-5">
			<h2>Basic</h2>
			<h3><span class="uppercase">Free</span></h3>
			<p>10,000 monthly visits</p>
			<ul>
				<li>Limited Email Support</li>
				<li>Unlimited Data Transfer</li>
				<li>10GB Local Storage</li>
			</ul>
			<a href="" class="button">Sign Up</a>
		</div>
		<div class="grid-1-5">
			<h2>Startup</h2>
			<h3><sup>$</sup>79<span class="small">/mo</span></h3>
			<p>25,000 monthly visits</p>
			<ul>
				<li>Limited Email Support</li>
				<li>Unlimited Data Transfer</li>
				<li>20GB Local Storage</li>
			</ul>
			<a href="" class="button">Sign Up</a>
		</div>
		<div class="grid-1-5">
			<h2>Growth</h2>
			<h3><sup>$</sup>179<span class="small">/mo</span></h3>
			<p>75,000 monthly visits</p>
			<ul>
				<li>Email Support</li>
				<li>Unlimited Data Transfer</li>
				<li>30GB Local Storage</li>
			</ul>
			<a href="" class="button">Sign Up</a>
		</div>
		<div class="grid-1-5">
			<h2>Premium</h2>
			<h3><sup>$</sup>499<span class="small">/mo</span></h3>
			<p>225,000 monthly visits</p>
			<ul>
				<li>Email Support</li>
				<li>Phone Support</li>
				<li>Unlimited Data Transfer</li>
			</ul>
			<a href="" class="button">Sign Up</a>
		</div>
		<div class="grid-1-5">
			<h2>Enterprise</h2>
			<h3><span class="uppercase">Let's Talk</span></h3>
			<p>1M+ monthly visits</p>
			<ul>
				<li>Email Support</li>
				<li>Phone Support</li>
				<li>Dedicated Environment</li>
				<li>Customized Plan</li>
			</ul>
			<a href="" class="button">Sign Up</a>
		</div>
	</div>
    </body>
    '''

    return html


@app.route('/icounts')
@flask_login.login_required
def icounts():
    html = '''
    <head>
            <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Tangerine">
            <link rel="stylesheet" href="/static/styles/notification.css">

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
    <ul class="menu">
		<li><a href="#" data-bubble="117">Interactions</a></li>
		<li><a href="#" data-bubble="4">Angry</a></li>
		<li><a href="#" data-bubble="19">Felt Uplifted</a></li>
		<li><a class="gold" href="#" data-bubble="1">Amazings</a></li>
	</ul>
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
<h1>Interaction Logger! </h1>
<div align="right"> Logged in as: ''' + flask_login.current_user.id+ '''
<br> <a href="/logout">Logout</a>


</div>
<hr>
<form>
  <h1><span>This is how it begins. Your interactions are logged, so we can tell you how to change yourself and others!!</span></h1>
  <div class="controls">
      <h1> The Basics </h1>
    <input id='check-1' type="checkbox" name='check-1' checked='checked' />
    <label for="check-1">Made by happy</label>

     <input id='check-2' type="checkbox" name='check-1' />
    <label for="check-2">Made by sad</label>
  </div>


  <div class="controls">
      <h1>Traits</h1>
    <input id='radio-1' type="radio" name='r-group-1' checked='checked' />
    <label for="radio-1">Reserved</label>

    <input id='radio-2' type="radio" name='r-group-1' />
    <label for="radio-2">Aggresive</label>

    <input id='radio-3' type="radio" name='r-group-1' />
    <label for="radio-3">Patient</label>

    <input id='radio-4' type="radio" name='r-group-1' />
    <label for="radio-4">Caring</label>

    <input id='radio-5' type="radio" name='r-group-1' />
    <label for="radio-5">Exciting</label>

  </div>

  <div class="controls">
     <h1>Visible</h1>
    <input class='toggle' type="checkbox" name='check-3' checked='checked' />
    Sad
    <input class='toggle' type="checkbox" name='check-4' />
  </div>

<div class="controls">
   <h1>Text</h1>
  <input class='toggle' type="text" name='check-3' checked='checked' />

</div>

<input type="submit" value="Submit">

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

@app.route('/charting')
@flask_login.login_required
def charting():
    html = '''
    <!DOCTYPE html>
<html>
	<head>
		<meta http-equiv="Content-Type" content="text/html;charset=utf-8"/ >
		<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Tangerine">

		<!-- Google fonts -->
		<link href='http://fonts.googleapis.com/css?family=Open+Sans:400,300' rel='stylesheet' type='text/css'>
		<link href='https://fonts.googleapis.com/css?family=Raleway' rel='stylesheet' type='text/css'>

		<!-- D3.js -->
		<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.6/d3.min.js" charset="utf-8"></script>

		<style>
			body {
				font-family: 'Open Sans', sans-serif;
				font-size: 25px;
				font-weight: 1000;
				fill: #54bded;
				text-align: center;
				text-shadow: 0 1px 0 #fff, 1px 0 0 #fff, -1px 0 0 #fff, 0 -1px 0 #fff;
				cursor: default;

			}
            some {
              font-family: 'Tangerine', serif;
              font-size: 48px;
                  }

			.legend {
				font-family: 'Raleway', sans-serif;
				fill: #333333;
			}

			.tooltip {
				fill: #333333;
			}
		</style>

        <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css">
        <link rel="stylesheet" href="/static/styles/menuInPlace.css">


	</head>
	<body>
        <div align="center"> <some>DeepWave 1.0 </some> </div> <hr>


        <nav class="menu">
          <input type="checkbox" href="#" class="menu-open" name="menu-open" id="menu-open"/>
          <label class="menu-open-button" for="menu-open">
            <span class="hamburger hamburger-1"></span>
            <span class="hamburger hamburger-2"></span>
            <span class="hamburger hamburger-3"></span>
          </label>
          <a href="#" class="menu-item"> <i class="fa fa-bar-chart"></i> </a>
          <a href="/dataentry" class="menu-item"> <i class="fa fa-plus"></i> </a>
          <a href="#" class="menu-item"> <i class="fa fa-heart"></i> </a>
          <a href="#" class="menu-item"> <i class="fa fa-envelope"></i> </a>
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

		<div class="radarChart"></div>

		<script src="/static/js/radarChart.js"></script>

        <script>



			var margin = {top: 100, right: 100, bottom: 100, left: 100},
				width = Math.min(700, window.innerWidth - 10) - margin.left - margin.right,
				height = Math.min(width, window.innerHeight - margin.top - margin.bottom - 20);

		var data = [
					  [//Positivity
						{axis:"Battery Life",value:0.22},
						{axis:"Brand",value:0.28},
						{axis:"Contract Cost",value:0.29},
						{axis:"Angry",value:0.17},
						{axis:"Aggresive",value:0.22},
						{axis:"Large Screen",value:0.02},
						{axis:"Price Of Device",value:0.21},
						{axis:"Attraction",value:0.50}
					  ],[//Samsung
						{axis:"Battery Life",value:0.27},
						{axis:"Brand",value:0.16},
						{axis:"Contract Cost",value:0.35},
						{axis:"Angry",value:0.33},
						{axis:"Aggresive",value:0.20},
						{axis:"Large Screen",value:0.13},
						{axis:"Price Of Device",value:0.35},
						{axis:"Attraction",value:0.38}
					  ],[//Nokia Smartphone
						{axis:"Battery Life",value:0.26},
						{axis:"Brand",value:0.10},
						{axis:"Contract Cost",value:0.30},
						{axis:"Angry",value:0.14},
						{axis:"Aggresive",value:0.42},
						{axis:"Large Screen",value:0.04},
						{axis:"Price Of Device",value:0.41},
						{axis:"Attraction",value:0.30}
					  ]
					];
			//////////////////////////////////////////////////////////////
			//////////////////// Draw the Chart //////////////////////////
			//////////////////////////////////////////////////////////////

			var color = d3.scale.ordinal()
				.range(["#EDC951","#CC333F","#00A0B0"]);

			var radarChartOptions = {
			  w: width,
			  h: height,
			  margin: margin,
			  maxValue: 0.5,
			  levels: 5,
			  roundStrokes: true,
			  color: color
			};
			//Call function to draw the Radar chart
			RadarChart(".radarChart", data, radarChartOptions);
		</script>
	</body>
</html>

    '''
    return html

@app.route('/crunching')
@flask_login.login_required
def crunching():
    html = '''
        <head>

<link rel="stylesheet" href="/static/styles/crunch.css">
                </head>
                <body>
        </head>
        <body>

            <div class="container">
          <div class="cube">
            <div class="sides">
              <div class="top"></div>
              <div class="right"></div>
              <div class="bottom"></div>
              <div class="left"></div>
              <div class="front"></div>
              <div class="back"></div>
            </div>
          </div>
          <div class="text">CRUNCHING DATA ... </div>
        </div>
        </body>
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
    html = '''
                <head>
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

                              <h2>Logged you out. <a href = "/login">Login again. </a> <small></small></h2>

                </body>
    '''
    return html

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
