"""Thresholder

This module contains main models to predict project success rate.

    Typical usage example:

    from app.utils.thresholder import Thresholder

    thresholder = Thresholder().load('path/to/model.pickle')
    thresholder.predict_prob(dataframe)
    thresholder.predict(dataframe)

"""
import pickle

import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin

class Thresholder(BaseEstimator, ClassifierMixin):
    """Model to predict project success rate

    Attributes:
        estimator: Model contains function `fit` and `predict_proba`
        threshold (float): Threshold to predict sucess

    """
    def __init__(self, estimator= None, threshold: float=.5) -> None:
        self.estimator = estimator
        self.threshold = threshold

    def fit(self, *kwargs) -> 'Thresholder':
        """Training with dataset"""
        self.estimator.fit(*kwargs)
        return self

    def predict_prob(self, *kwargs) -> np.ndarray:
        """Predict the success probability of projects"""
        return self.estimator.predict_proba(*kwargs)[:, 1]

    def predict(self, *kwargs) -> np.ndarray:
        """Predict whether the projects will success or not"""
        prob = self.predict_prob(*kwargs)
        pred = (prob > self.threshold).astype(int)
        return pred

    def save(self, filename: str) -> None:
        """Save the thresholder itself"""
        data = {
            'estimator': self.estimator,
            'threshold': self.threshold
        }
        with open(filename, 'wb') as file:
            pickle.dump(data, file)

    def load(self, filename: str) -> 'Thresholder':
        """Load thresholder from file"""
        with open(filename, 'rb') as file:
            data = pickle.load(file)
        if not isinstance(data, dict):
            raise TypeError('The file should contain a dictionary')
        if 'estimator' not in data or 'threshold' not in data:
            raise KeyError('The data should contain estimator and threshold')
        self.estimator = data['estimator']
        self.threshold = data['threshold']
        return self
