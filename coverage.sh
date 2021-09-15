#!bin/sh

python -m coverage run --branch -m unittest discover -v -s tests/ -p test_*.py
python -m coverage report --omit=*site-packages*,*tests* --skip-empty --fail-under=100
python -m coverage html --omit=*site-packages*,*tests* --skip-empty
