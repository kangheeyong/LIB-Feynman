import pandas as pd

from feynman.models.kobert import convert_data


def test_convert_data():

    data_df = pd.DataFrame({'text': ["안녕하세요", "반갑습니다."], 'label': [0, 1]})
    (tokens, masks, segments), targets = convert_data(data_df, SEQ_LEN=128, DATA_COLUMN="text", LABEL_COLUMN="label")

    assert len(tokens) == 2
    assert len(masks) == 2
    assert len(segments) == 2






