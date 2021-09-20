"""Project suggester

This module provides function to suggest changes for project.

    Typical usage example:

    from app.utils.suggest import get_suggestion

    get_suggestion(project, vector)

"""
from functools import reduce
import pathlib
import pickle
import time

import numpy as np
import pandas as pd

from app import logger

FILE_PATH = pathlib.Path(__file__).parent.resolve()

THRESHOLD = .05

dataset = pd.read_pickle(FILE_PATH / '../data/model/dataset.pickle')
dataset['success'] = dataset['percentage'] >= 1

with open(FILE_PATH / '../data/model/vectors_norm.pickle', 'rb') as file:
    dataset_vectors = pickle.load(file)

with open(FILE_PATH / '../data/model/tokens.pickle', 'rb') as file:
    dataset_tokens = pickle.load(file)

with open(FILE_PATH / '../data/model/filter_corpus.pickle', 'rb') as file:
    filter_corpus = pickle.load(file)

with open(FILE_PATH / '../data/model/chi2.pickle', 'rb') as file:
    chi2 = pickle.load(file)

with open(FILE_PATH / '../data/model/odds.pickle', 'rb') as file:
    odds = pickle.load(file)

def get_similar_project(vector: dict):
    """Get dataframe of similar projects"""
    cos = {
        k: dataset_vectors[k] @ v.A.T
        for k, v in vector.items()
    }
    cos_list = cos['content'].tolist()
    dataset['cos'] = [item for sublist in cos_list for item in sublist]
    return dataset[dataset['cos'] >= THRESHOLD].sort_values('cos', ascending=False).index.to_numpy()[:20]

def get_text_suggestion(sim_proj, tokens: dict) -> dict:
    """Generate text suggestion"""
    peer_docs = {
        c: np.array(v, dtype=object)[sim_proj]
        for c, v in dataset_tokens.items()
    }
    peer_tokens = {
        c: reduce(lambda x, y: x | set(y), v, set())
        for c, v in peer_docs.items()
    }
    not_used_tokens = {
        c: np.array(list(v - set(tokens[c])))
        for c, v in peer_tokens.items()
    }
    not_used_tokens = {
        k: v[np.isin(v, filter_corpus[k])]
        for k, v in not_used_tokens.items()
    }
    not_used_tokens_docs = {
        k: np.array([
            [t in d for d in peer_docs[k]]
            for t in v
        ])
        for k, v in not_used_tokens.items()
    }
    not_used_tokens_cnt = {
        k: v.sum(axis=1)
        for k, v in not_used_tokens_docs.items()
    }
    not_used_tokens_idx = {
        k: [np.where(filter_corpus[k] == t)[0][0] for t in v]
        for k, v in not_used_tokens.items()
    }
    not_used_chi2 = {
        k: chi2[k][v]
        for k, v in not_used_tokens_idx.items()
    }
    not_used_odds = {
        k: odds[k][v]
        for k, v in not_used_tokens_idx.items()
    }
    not_used_mult = {
        k: v > 1
        for k, v in not_used_tokens_cnt.items()
    }
    not_used_positive = {
        k: v > 1
        for k, v in not_used_odds.items()
    }
    not_used_selected = {
        k: v & not_used_positive[k]
        for k, v in not_used_mult.items()
    }
    not_used_chi2_positive_rank = {
        k: v[not_used_selected[k]].argsort()
        for k, v in not_used_chi2.items()
    }
    recommend_tokens = {
        k: pd.DataFrame(zip(
            v[not_used_selected[k]][not_used_chi2_positive_rank[k]],
            not_used_tokens_cnt[k][not_used_selected[k]][not_used_chi2_positive_rank[k]],
            not_used_chi2[k][not_used_selected[k]][not_used_chi2_positive_rank[k]]
        ), columns=['token', 'df', 'pvals'])
        for k, v in not_used_tokens.items()
    }
    peer_cols = ['title', 'link']
    peer_props = {
        c: dataset.iloc[sim_proj, :][c].to_numpy()
        for c in peer_cols
    }
    cols = ['title', 'description', 'content']
    for col in cols:
        for peer_col in peer_cols:
            recommend_tokens[col][f'peer_{peer_col}'] = [
                peer_props[peer_col][d].tolist()
                for d in not_used_tokens_docs[col][
                    not_used_selected[col]][not_used_chi2_positive_rank[col]].tolist()
            ]
    result = {
        'recommend_tokens': {
            k: v.to_dict('records')[:20]
            for k, v in recommend_tokens.items()
        }
    }
    return result

def get_meta_suggestion(sim_proj, project) -> dict:
    """Generate metadata suggestion"""
    cols = ['goal', 'content_length', 'duration_days', 'max_set_prices',
            'description_length', 'min_set_prices']
    indexes = ['min', '25%', '50%', '75%', 'max']
    df_peer = dataset[cols + ['success']].iloc[sim_proj, :]
    box = df_peer[cols].describe().loc[indexes, :].astype(float).rename(index={
        ind: f'box_{ind.replace("%", "")}'
        for ind in indexes
    }).to_dict('dict')
    success_median = df_peer[df_peer['success']][cols].median().astype(float).to_dict()
    failure_median = df_peer[~df_peer['success']][cols].median().astype(float).to_dict()
    result = {
        'metadata': {
            c: {
                'success_median': success_median[c],
                'failure_median': failure_median[c],
                'success_greater': int(np.sum(df_peer[df_peer['success']][c] > project[c])),
                'success_less': int(np.sum(df_peer[df_peer['success']][c] < project[c])),
                'project_value': project[c],
                **box[c]
            }
            for c in cols
        }
    }
    return result

def get_suggestion(project: dict, vector: dict, tokens: dict) -> dict:
    """Generates suggestion for project"""
    start_time = time.time()
    sim_proj = get_similar_project(vector)
    logger.info('Cosine Similarity Time: %f', time.time() - start_time)
    if len(sim_proj) > 0:
        start_time = time.time()
        cols = ['title', 'domain', 'type', 'success', 'cos', 'link']
        peers = dataset[cols].iloc[sim_proj, :].to_dict('records')
        cate = {}
        for col in ['domain', 'type']:
            cnt = dataset.iloc[sim_proj,:][col].value_counts()
            cate[col] = {}
            cate[col]['same_rate'] = float((dataset.iloc[sim_proj,:][col] == project[col]).mean())
            cate[col]['most'] = {
                'name': str(cnt.index[0]),
                'rate': float(cnt[0] / sim_proj.shape[0])
            }
        logger.info('Category Suggestion Time: %f', time.time() - start_time)
        start_time = time.time()
        text_suggestion = get_text_suggestion(sim_proj, tokens)
        logger.info('Text Suggestion Time: %f', time.time() - start_time)
        start_time = time.time()
        meta_suggestion = get_meta_suggestion(sim_proj, project)
        logger.info('Metadata Suggestion Time: %f', time.time() - start_time)
        start_time = time.time()
    else:
        peers = []
        cate = {}
        text_suggestion = {'recommend_tokens': {}}
        meta_suggestion = {'metadata': {}}
    result = {
        'peer_cnt': int(sim_proj.shape[0]),
        'peer_success_cnt': int(dataset.iloc[sim_proj,:]['success'].sum()),
        'peers': peers,
        'categories': cate,
        **text_suggestion,
        **meta_suggestion
    }
    return result
