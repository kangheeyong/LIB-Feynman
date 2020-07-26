import sys

import pandas as pd

from feynman.models.kobert import convert_data



if __name__ == '__main__':
    argv = sys.argv
    
    if len(argv) != 2:
        print(
            "Usage: python inference_kobert_tokenizker.py '[korean test]'")
        print("e.g.python inference_kobert_tokenizker.py 안녕하세요 만나서 반갑습니다.'")
        sys.exit(0)

    data_df = pd.DataFrame({'text': [argv[1]], 'label': [0]})

    (tokens, masks, segments), targets = convert_data(data_df, SEQ_LEN = 128, DATA_COLUMN = "text", LABEL_COLUMN = "label")

    print(f"origin text : {argv[1]}")
    print(f"tokens      : {tokens}")
    print(f"masks       : {masks}")
    print(f"segments    : {segments}")


