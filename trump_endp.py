# an endpoint that responds like trump

from flask import Flask
from flask import request, url_for
app = Flask(__name__)
import json
from src import test

vLen = 5
diversity = 0.3
modelParams = test.recalc_model_params('./src/models/trump/source.txt','./src/models/trump/trump.w2v', vLen)
weights = './src/models/trump/tb-weights-trump'



@app.route('/handleMessage', methods=['GET','POST'])
def handleMessage():
    msgBase=request.args.get('message')
    msg = ' '.join(msgBase.split('%20'))
    if len(msg)<3 or msg==None:
        res={'response':'''sorry didn't get you''', 'status':'Fail', 'message':msg}
    elif len(msg.split(' '))<6:
        res = {'response':'''Too few words, speak up''', 'status':'Fail', 'message':msg}
    else:
        resMsg = test.process_message(msg, modelParams,weights,diversity,vLen)
        res = {'response':resMsg, 'status':'ok', 'message':msg}
    return json.dumps(res)

@app.route('/hello/')
def hello_world():
    return 'umm.. hey .. this is ackward'


if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run(host='0.0.0.0',port = 8084, threaded=False)
