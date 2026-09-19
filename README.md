# Rural Business Advisor

A data-driven rural business decision-support platform for Maharashtra
(initial districts: Nagpur, Pune, Latur).

## 1) Place datasets

Copy the 8 CSV files into `backend/data/datasets/`:
- pca_villages.csv
- village_clustering_dataset (1).csv
- b04_processed.csv
- b24_processed.csv
- crop_area_processed.csv
- crop_production_processed.csv
- dairy_development_2010_11 (1).csv
- village_amenities_processed (1).csv

## 2) Backend

cd backend
python -m venv venv
venv\Scripts\activate           # Windows
pip install -r requirements.txt
python train.py
uvicorn main:app --reload

## 3) Frontend

cd frontend
npm install
npm run dev

Open http://localhost:5173

---

## License & Copyright

© 2026 **Code Ninjas** (Team ID 056)
SIH 2026 · Problem Statement ID 26091

All Rights Reserved.

This project is submitted to Smart India Hackathon 2026.
Unauthorized copying, distribution, or commercial use of this
project without written permission from the team is prohibited.

**Contact:** [your-email@example.com]
