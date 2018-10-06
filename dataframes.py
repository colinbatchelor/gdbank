import numpy as np
import pandas as pd
from innealan.acainn import Lemmatizer

class Frame():
    def __init__(self):
        self.l = Lemmatizer()
    
    def make(self, tagged_tokens):
        text = pd.DataFrame({'token': [t[0] for t in tagged_tokens],
                             'pos': [t[1] for t in tagged_tokens]}).append(pd.DataFrame({'token':['<END>','<END>'], 'pos':['','']}),ignore_index =True)
        text_1 = pd.DataFrame({'token':['<START>'], 'pos':['']}).append(text, ignore_index = True).rename(columns={'token':'t_1', 'pos':'p_1'})
        text_2 = pd.DataFrame({'t_1':['<START>'], 'p_1':['']}).append(text_1, ignore_index = True).rename(columns={'t_1':'t_2', 'p_1':'p_2'})
        text1 = text.drop(0).reset_index(drop=True).rename(columns={'token':'t1','pos':'p1'})
        text2 = text1.drop(0).reset_index(drop=True).rename(columns={'t1':'t2', 'p1':'p2'})
        tt = text_2.join(text_1).join(text).join(text1).join(text2).dropna()
        print([lambda tt: tt.token.str.match(r'.h')])
        #new_result = tt.assign(lenited = lambda tt: self._lenited(tt['token'])) 
        tt.assign(lenited = lambda tt: self.l.lenited_pd(tt.token.str))
        return tt

