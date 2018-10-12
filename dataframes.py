import numpy as np
import pandas as pd
from innealan.acainn import Lemmatizer

class Frame():
    def __init__(self):
        self.l = Lemmatizer()
    
    def make(self, tagged_tokens):
        text = pd.DataFrame({
            'token': [t[0] for t in tagged_tokens],
            'pos': [t[1] for t in tagged_tokens]}).append(pd.DataFrame({
                'token':['<END>','<END>'],
                'pos':['','']}),ignore_index =True)
        text_1 = pd.DataFrame({
            'token':['<START>'],
            'pos':['']}).append(text, ignore_index = True).rename(columns={
                'token':'_t_1',
                'pos':'_p_1'})
        text_2 = pd.DataFrame({
            '_t_1':['<START>'],
            '_p_1':['']}).append(text_1, ignore_index = True).rename(columns={
                '_t_1':'_t_2',
                '_p_1':'_p_2'})
        text1 = text.drop(0).reset_index(drop=True).rename(columns={
            'token':'_t1', 'pos':'_p1'})
        text2 = text1.drop(0).reset_index(drop=True).rename(columns={
            '_t1':'_t2', '_p1':'_p2'})
        return text_2.join(text_1).join(text).join(text1).join(text2).dropna()

    def feats(self, df):
        return df.assign(
            _lenited = lambda x: self.l.lenited_pd(x.token.str),
            _chalenited = lambda x: self.l.chalenited_pd(x.token.str),
            _nondentallenited = lambda x: self.l.ndlenited_pd(x.token.str),
            _genitive = lambda x: x.pos.str.match('N.*g'),
            _sing = lambda x: x.pos.str.match('N.s'),
            _genitivesing = lambda x: x.pos.str.match('N.s.g'),
            _pl = lambda x: x.pos.str.match('N.p'),
            _c0 = lambda x: x.token.str[0],
            code = lambda x: '')
            
