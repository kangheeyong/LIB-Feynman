import sys

import pandas as pd

from feynman.models.kobert import convert_data


if __name__ == '__main__':
    argv = sys.argv
    if len(argv) != 1:
        print(
            "Usage: python inference_kobert_tokenizker.py '[korean test]'")
        print("e.g.python inference_kobert_tokenizker.py 안녕하세요 만나서 반갑습니다.'")
        raise

    data_df = pd.DataFrame({'test': argv[0], 'label': 0})
    
    (tokens, masks, segments), targets = convert_data(data_df, SEQ_LEN = 128, DATA_COLUMN = "text", LABEL_COLUMN = "label")
  
    print(f"origin text : {argv[0]}") 
    print(f"tokens      : {tokens}") 
    print(f"masks       : {masks}") 
    print(f"segments    : {segments}") 
    
    