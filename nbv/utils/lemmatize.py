from nltk.stem import PorterStemmer
from nltk import pos_tag

def stem(keyword):
    ps = PorterStemmer()

    print(ps.stem(keyword))

if __name__ == '__main__':
    stem("is")
    stem("running")
    stem("immigrant")
    stem("immigration")
    stem("newspaper")
    stem("Trump")
    stem("presidential")
    stem("President")
    stem("program")
    stem("programmer")
    stem("programming")