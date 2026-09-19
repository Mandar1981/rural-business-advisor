# Rural Business Advisor - Backend

## 1) Place datasets in `backend/data/datasets/`
## 2) Install

python -m venv venv
venv\Scripts\activate     # Windows
pip install -r requirements.txt

## 3) Train

python train.py

## 4) Run

uvicorn main:app --reload

API: http://localhost:8000
