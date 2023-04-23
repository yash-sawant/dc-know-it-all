import pandas as pd
import spacy
from sklearn.metrics.pairwise import cosine_similarity
# load spacy model
import numpy as np

DATA_PATH = 'dc-know-it-all/dc_data.xlsx'

class DCExpert:
    def __init__(self, path):
        self.df = pd.read_excel(path,
                           header=[0],
                           index_col=[0,1,2]
                           )
        self.df.dropna(inplace=True)
        print('Loading spacy...')
        self.nlp = spacy.load('en_core_web_md')#, disable=["lemmatizer", "tagger", "parser", "ner"])
        print('spacy data loaded')
        self.question_encoding = np.vstack(self.df['questions'].apply(lambda p:self.nlp(p).vector))
        # print(self.question_encoding)

    def get_context(self, ques):
        ques_enc = self.nlp(ques).vector.reshape((1, -1))
        similarity_scores = cosine_similarity(ques_enc, self.question_encoding)
        similarity_scores=similarity_scores.reshape((-1))
        q_idx = np.argsort(similarity_scores)[::-1][0]

        return self.df.iloc[q_idx, :].name[1]



if __name__ == '__main__':

    exp1 = DCExpert(DATA_PATH)

    print(exp1.get_context('How are students chosen for very programs that are difficult to get into?'))

    # Expected Answer: How are applicants selected for highly competitive programs?