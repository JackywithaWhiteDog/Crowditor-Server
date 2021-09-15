"""This module provides abstract class for test cases"""
from abc import ABC, abstractmethod
import pathlib
import sys

FILE_PATH = pathlib.Path(__file__).parent.resolve()
sys.path.insert(1, str(FILE_PATH / '../../main'))

class TestAbstractClass(ABC):
    """Abstract class for test cases"""

    def create_app(self):
        """Create application instance"""
        from app import app # pylint: disable=import-error,import-outside-toplevel
        app.config['TESTING'] = True
        return app
