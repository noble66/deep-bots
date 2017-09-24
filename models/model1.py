
import pickle
from textblob import TextBlob as tb
from operator import itemgetter

f = open('/home/ubuntu/deep-bots/models/hedon.dict','r')
dat = pickle.load(f)

def analyze_sent(sent, debug=True):
    ngtags = tb(sent).tags
    sScore = 0
    if debug==True:
        print ngtags
    for w,pos in ngtags:
        if pos in ['DT','VBZ','PRP', 'NNS']:
            continue
        if w in dat:
            s=(5000-int(dat[w]['happiness_rank']))*1.0/5000
            print w, ': ', s
            sScore+=s
    return sScore


# uses semeval
def load_semeval_data():
    with open('/home/ubuntu/data/semeval2007/trial/processed/emolabels.list','r') as fr:
        emoK = pickle.load(fr)
    with open('/home/ubuntu/data/semeval2007/trial/processed/txtdat.list','r') as fr:
        dat = pickle.load(fr)
    return emoK, dat

def show_sem_eval_data(n=50, emoK=None, dat=None):
    anot = ['id', 'anger', 'disgust', 'fear', 'joy', 'sadness', 'surprise']
    if emoK is None or dat is None:
        emoK, dat = load_semeval_data()
    for i in range(0,n):
        print dat[i]
        d = {j:i for (i,j) in zip(emoK[i][1:],anot[1:])}
        print sorted(d.iteritems(), key = itemgetter(1), reverse= True)
        print ''
