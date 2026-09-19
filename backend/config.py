"""
Central configuration.

© 2026 Code Ninjas (SIH 2026, PS26091)
All Rights Reserved.
"""

from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "datasets"
MODEL_DIR = BASE_DIR / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

FILES = {
    "pca_villages": "pca_villages.csv",
    "village_clustering": "village_clustering_dataset (1).csv",
    "village_amenities_district": "village_amenities_processed (1).csv",
    "b04": "b04_processed.csv",
    "b24": "b24_processed.csv",
    "crop_area": "crop_area_processed.csv",
    "crop_production": "crop_production_processed.csv",
    "dairy": "dairy_development_2010_11 (1).csv",
}

SUPPORTED_DISTRICTS = ["Nagpur", "Pune", "Latur"]

AMENITY_FEATURES = [
    "Govt Primary School (Numbers)",
    "Private  Primary School (Numbers)",
    "Govt Vocational Training School/ITI (Numbers)",
    "Private Vocational Training School/ITI (Numbers)",
    "Community Health Centre (Numbers)",
    "Primary Health Centre (Numbers)",
    "Veterinary Hospital (Numbers)",
    "Public Bus Service (Status A(1)/NA(2))",
    "Private Bus Service (Status A(1)/NA(2))",
    "Commercial Bank (Status A(1)/NA(2))",
    "Cooperative Bank (Status A(1)/NA(2))",
    "Mandis/Regular Market (Status A(1)/NA(2))",
]

AMENITY_LABELS = {
    "Govt Primary School (Numbers)": "Government Primary Schools",
    "Private  Primary School (Numbers)": "Private Primary Schools",
    "Govt Vocational Training School/ITI (Numbers)": "Govt ITI / Vocational",
    "Private Vocational Training School/ITI (Numbers)": "Private ITI / Vocational",
    "Community Health Centre (Numbers)": "Community Health Centre",
    "Primary Health Centre (Numbers)": "Primary Health Centre",
    "Veterinary Hospital (Numbers)": "Veterinary Hospital",
    "Public Bus Service (Status A(1)/NA(2))": "Public Bus Service",
    "Private Bus Service (Status A(1)/NA(2))": "Private Bus Service",
    "Commercial Bank (Status A(1)/NA(2))": "Commercial Bank",
    "Cooperative Bank (Status A(1)/NA(2))": "Cooperative Bank",
    "Mandis/Regular Market (Status A(1)/NA(2))": "Mandi / Regular Market",
}

RANDOM_STATE = 42

BUSINESS_CATALOG = {
    "Dairy / Milk-related Business": {
        "sub_businesses": [
            {"name": "Milk Collection Centre", "startup_cost": 150000},
            {"name": "Small Dairy Products Unit (paneer/curd)", "startup_cost": 250000},
            {"name": "Cattle-related Service (feed, AI)", "startup_cost": 120000},
        ],
        "note": "Prototype/domain estimate - not an official cost.",
    },
    "Agri Processing": {
        "sub_businesses": [
            {"name": "Flour Mill (Atta Chakki)", "startup_cost": 200000},
            {"name": "Dal / Pulse Processing", "startup_cost": 350000},
            {"name": "Grain Processing Unit", "startup_cost": 300000},
            {"name": "Small Food Processing Unit", "startup_cost": 400000},
        ],
        "note": "Prototype/domain estimate - not an official cost.",
    },
    "Retail & Trading": {
        "sub_businesses": [
            {"name": "Kirana / General Store", "startup_cost": 100000},
            {"name": "Agricultural Input Store (seeds/fertilizer)", "startup_cost": 180000},
            {"name": "Local Trading Business", "startup_cost": 150000},
        ],
        "note": "Prototype/domain estimate - not an official cost.",
    },
    "Skill & Repair Services": {
        "sub_businesses": [
            {"name": "Mobile Repair Shop", "startup_cost": 60000},
            {"name": "Electrical Repair Shop", "startup_cost": 80000},
            {"name": "Two-Wheeler Repair Shop", "startup_cost": 100000},
            {"name": "Welding Workshop", "startup_cost": 120000},
        ],
        "note": "Prototype/domain estimate - not an official cost.",
    },
    "Rural Services": {
        "sub_businesses": [
            {"name": "Digital Service Centre (CSC)", "startup_cost": 80000},
            {"name": "Printing / Photocopy", "startup_cost": 70000},
            {"name": "Online Government Services Kiosk", "startup_cost": 90000},
            {"name": "Banking Assistance / BC Point", "startup_cost": 60000},
            {"name": "Local Logistics / Courier", "startup_cost": 120000},
        ],
        "note": "Prototype/domain estimate - not an official cost.",
    },
}

OPPORTUNITY_WEIGHTS = {
    "Dairy / Milk-related Business": {"veterinary": 0.22, "agri_activity": 0.20, "transport": 0.15, "market": 0.13, "dairy_district": 0.30},
    "Agri Processing": {"cultivators": 0.20, "agri_labour": 0.20, "crop_production": 0.15, "cultivated_area": 0.10, "irrigation": 0.10, "market": 0.15, "transport": 0.10},
    "Retail & Trading": {"population": 0.20, "market": 0.20, "commercial_bank": 0.10, "coop_bank": 0.10, "transport": 0.20, "workers": 0.20},
    "Skill & Repair Services": {"govt_iti": 0.20, "private_iti": 0.20, "workers": 0.25, "population": 0.20, "transport": 0.15},
    "Rural Services": {"population": 0.20, "banks": 0.20, "transport": 0.15, "market": 0.15, "schools": 0.15, "healthcare": 0.15},
}

PMEGP = {
    "scheme_name": "PMEGP (Prime Minister's Employment Generation Programme)",
    "potential_relevance_note": ("PMEGP may be relevant for micro-enterprise setup. Current eligibility, "
        "subsidy and loan limits vary - verify with official PMEGP/KVIC sources."),
    "checklist": [
        "Applicant age 18+",
        "Project cost within scheme ceiling (varies)",
        "Own contribution requirement met (varies)",
        "Business category eligible under PMEGP",
        "Not a defaulter of any nationalized bank / financial institution",
    ],
    "verification_warning": ("Verify current eligibility, subsidy and financing conditions through "
        "official PMEGP / KVIC sources before making any decision."),
}
GROQ_MODEL = "openai/gpt-oss-120b"
GROQ_MAX_TOKENS = 2000
GROQ_TEMPERATURE = 0.6

# ==================== MONGODB CONFIG ====================
MONGODB_DB = "ausekarmandar60_db_user"
MONGODB_REPORTS_COLLECTION = "reports"
MONGODB_ANALYTICS_COLLECTION = "analytics"
FINANCIAL_DEFAULTS = {
    "initial_investment": 200000,
    "selling_price_per_unit": 50,
    "units_per_month": 1000,
    "monthly_fixed_cost": 15000,
    "variable_cost_per_unit": 20,
}
