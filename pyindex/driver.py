import glob
import pickle
import time

from compressed_index import Compressed
from inverted_index import SPIMI
from tokenizer import token_stream

if __name__ == '__main__':
    tokens = token_stream(glob.glob('../../tokenizer/Cranfield/cranfield00*'))
    try:
        with open('index.pkl', 'rb') as fp:
            indexer = pickle.load(fp)
        end = time.time()
    except IOError:
        indexer = SPIMI()
        start = time.time()
        indexer.build_index(tokens)
        end = time.time()
        print('Built index in', end - start, 'sec')
        with open('index.pkl', 'wb') as fp:
            pickle.dump(indexer, fp)
    indexer.to_disk('data/')
    compressor = Compressed(indexer)
    compressor.blocking_gamma('data/', k=8)
    compressor.frontcoding_delta('data/', k=8)
