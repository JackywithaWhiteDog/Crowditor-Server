"""Project estimator

This module provides function to estimate project.

    Typical usage example:

    from app.utils.estimate import get_estimation

    get_estimation(project)

"""
import pathlib
import pickle
import time

import numpy as np
import pandas as pd
from ckip_transformers.nlp import CkipWordSegmenter

from app import logger
from app.utils.preprocessor import Preprocessor
from app.utils.thresholder import Thresholder
from app.utils.suggest import get_suggestion

FILE_PATH = pathlib.Path(__file__).parent.resolve()

segmentor = CkipWordSegmenter(level=3)
preprocessor = Preprocessor()
thresholder = Thresholder().load(FILE_PATH / '../data/model/model.pickle')

with open(FILE_PATH / '../data/model/vectorizer.pickle', 'rb') as file:
    vectorizer = pickle.load(file)

with open(FILE_PATH / '../data/model/selected_tokens.pickle', 'rb') as file:
    selected_tokens = pickle.load(file)

with open(FILE_PATH / '../data/model/scores.pickle', 'rb') as file:
    dataset_scores = pickle.load(file)

with open(FILE_PATH / '../data/model/filter_tokens.pickle', 'rb') as file:
    filter_tokens = pickle.load(file)

features = {
    c: v.get_feature_names()
    for c, v in vectorizer.items()
}
features = {
    c: np.array(v)[np.isin(v, selected_tokens[c])]
    for c, v in features.items()
}

def tokenize(project: dict) -> dict:
    """Tokenizes text data"""
    cols = ['title', 'description', 'content']
    start_time = time.time()
    tmp = segmentor([project[c] for c in cols], show_progress=False)
    logger.info('Segmentation Time: %f', time.time() - start_time)
    start_time = time.time()
    result = {
        c: preprocessor.preprocess(t)
        for c, t in zip(cols, tmp)
    }
    logger.info('Preprocessing Time: %f', time.time() - start_time)
    return result

def vectorize(tokens: dict) -> dict:
    """Vectorizes text data"""
    start_time = time.time()
    vector_all = {
        c: vectorizer[c].transform([' '.join(v)])
        for c, v in tokens.items()
    }
    logger.info('Vectorization Time: %f', time.time() - start_time)
    start_time = time.time()
    norm_filtered_vector = {
        k: v[:, filter_tokens[k]]
        for k, v in vector_all.items()
    }
    norm_filtered_vector = {
        k: v / np.linalg.norm(v.A)
        for k, v in norm_filtered_vector.items()
    }
    logger.info('Normalization Time: %f', time.time() - start_time)
    start_time = time.time()
    input_vector = {
        k: v[:, np.isin(
            vectorizer[k].get_feature_names(), selected_tokens[k])
        ]
        for k, v in vector_all.items()
    }
    logger.info('Vector Filtering Time: %f', time.time() - start_time)
    return norm_filtered_vector, input_vector

def get_metadata(project: dict):
    """Preprocesses metadata and feature names"""
    cols = ['facebook', 'instagram', 'youtube', 'website', 'set_count', 'start_time', 'end_time']
    df_project = pd.DataFrame([project])[cols]

    df_project['duration_days'] = (df_project['end_time'] - df_project['start_time']).dt.days
    project['duration_days'] = int(df_project['duration_days'].values[0])

    df_project['description_length'] = project['description_length'] = len(project['description'])
    df_project['content_length'] = project['content_length'] = len(project['content'])
    df_project['title_length'] = len(project['title'])

    cate = ['type_群眾集資', 'type_訂閱式專案', 'type_預購式專案', 'domain_出版', 'domain_地方創生',
        'domain_挺好店', 'domain_插畫漫畫', 'domain_攝影', 'domain_教育', 'domain_時尚',
        'domain_社會', 'domain_科技', 'domain_空間', 'domain_藝術', 'domain_表演',
        'domain_設計', 'domain_遊戲', 'domain_電影動畫', 'domain_音樂', 'domain_飲食']

    df_project[cate] = 0
    df_project[f'type_{project["type"]}'] = 1
    df_project[f'domain_{project["domain"]}'] = 1

    df_project['log_goal'] = np.log(project['goal']) if project['goal'] else 1
    df_project['log_max_set_prices'] = np.log(
        project['max_set_prices']) if project['max_set_prices'] else 1
    df_project['log_min_set_prices'] = np.log(project['min_set_prices'] + 1)

    drop_cols = ['start_time', 'end_time']

    df_project = df_project.drop(columns=drop_cols)

    cols = ['facebook', 'instagram', 'youtube', 'website', 'set_count',
        'duration_days', 'description_length', 'content_length', 'title_length',
        'type_群眾集資', 'type_訂閱式專案', 'type_預購式專案', 'domain_出版', 'domain_地方創生',
        'domain_挺好店', 'domain_插畫漫畫', 'domain_攝影', 'domain_教育', 'domain_時尚',
        'domain_社會', 'domain_科技', 'domain_空間', 'domain_藝術', 'domain_表演',
        'domain_設計', 'domain_遊戲', 'domain_電影動畫', 'domain_音樂', 'domain_飲食',
        'log_goal', 'log_max_set_prices', 'log_min_set_prices']

    df_project = df_project[cols]
    return df_project.to_numpy().astype(float), df_project.columns, project

def get_input(project: dict, vector: dict):
    """Construct input dataframe for model"""
    start_time = time.time()
    x_meta, meta_features, project = get_metadata(project)
    logger.info('Getting Metadata Time: %f', time.time() - start_time)
    start_time = time.time()
    cols = ['title', 'description', 'content']
    x_all = vector[cols[0]].A
    feature_name = [f'{cols[0]}:{f}' for f in features[cols[0]]]
    for col in cols[1:]:
        x_all = np.hstack((x_all, vector[col].A))
        feature_name.extend([f'{col}:{f}' for f in features[col]])
    x_all = np.hstack((x_all, x_meta))
    feature_name.extend([f'meta:{f}' for f in meta_features])
    df_x = pd.DataFrame(x_all, columns=feature_name)
    logger.info('Input Construction Time: %f', time.time() - start_time)
    return df_x, project

def get_estimation(project: dict) -> dict:
    """Estimates project"""
    tokens = tokenize(project)
    norm_filtered_vector, input_vector = vectorize(tokens)
    df_x, project = get_input(project, input_vector)
    start_time = time.time()
    prob = float(thresholder.predict_prob(df_x)[0])
    logger.info('Model Prediction Time: %f', time.time() - start_time)
    greater_than = float((dataset_scores < prob).mean())
    suggestion = get_suggestion(project, norm_filtered_vector, tokens)
    result = {
        'score': prob,
        'greater_than': greater_than,
        **suggestion
    }
    return result
