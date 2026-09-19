"""
MongoDB integration for saving reports and analytics.
Graceful fallback: if MongoDB not configured, returns None/empty.
"""

from __future__ import annotations

import os
from datetime import datetime
from typing import Dict, List, Optional

try:
    from pymongo import MongoClient
except ImportError:
    MongoClient = None

from config import MONGODB_ANALYTICS_COLLECTION, MONGODB_DB, MONGODB_REPORTS_COLLECTION


_client = None


def _get_db():
    global _client
    if _client is not None:
        return _client[MONGODB_DB]
    if MongoClient is None:
        return None
    uri = os.getenv("MONGODB_URI", "").strip()
    if not uri or "YOUR_" in uri or "xxxxx" in uri.lower():
        return None
    try:
        _client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        _client.admin.command("ping")
        return _client[MONGODB_DB]
    except Exception as e:
        print(f"[db_service] MongoDB connection failed: {e}")
        _client = None
        return None


def is_db_available() -> bool:
    return _get_db() is not None


def save_report(report: Dict) -> Optional[str]:
    db = _get_db()
    if db is None:
        return None
    try:
        report = dict(report)
        report["created_at"] = datetime.utcnow()
        result = db[MONGODB_REPORTS_COLLECTION].insert_one(report)
        _update_analytics(db, report)
        return str(result.inserted_id)
    except Exception as e:
        print(f"[db_service] save_report failed: {e}")
        return None


def _update_analytics(db, report: Dict):
    try:
        district = report.get("district") or "unknown"
        category = report.get("category") or "unknown"
        db[MONGODB_ANALYTICS_COLLECTION].update_one(
            {"_id": "global"},
            {
                "$inc": {
                    f"districts.{district}": 1,
                    f"categories.{category}": 1,
                    "total_reports": 1,
                },
                "$set": {"last_updated": datetime.utcnow()},
            },
            upsert=True,
        )
    except Exception as e:
        print(f"[db_service] analytics update failed: {e}")


def get_history(limit: int = 20) -> List[Dict]:
    db = _get_db()
    if db is None:
        return []
    try:
        cursor = db[MONGODB_REPORTS_COLLECTION].find(
            {},
            {
                "_id": 1, "name": 1, "village": 1, "taluka": 1, "district": 1,
                "category": 1, "capital": 1, "created_at": 1,
            },
        ).sort("created_at", -1).limit(limit)
        out = []
        for doc in cursor:
            doc["_id"] = str(doc["_id"])
            if "created_at" in doc and hasattr(doc["created_at"], "isoformat"):
                doc["created_at"] = doc["created_at"].isoformat()
            out.append(doc)
        return out
    except Exception as e:
        print(f"[db_service] get_history failed: {e}")
        return []


def get_analytics() -> Dict:
    db = _get_db()
    if db is None:
        return {}
    try:
        doc = db[MONGODB_ANALYTICS_COLLECTION].find_one({"_id": "global"}) or {}
        doc.pop("_id", None)
        if "last_updated" in doc and hasattr(doc["last_updated"], "isoformat"):
            doc["last_updated"] = doc["last_updated"].isoformat()
        return doc
    except Exception as e:
        print(f"[db_service] get_analytics failed: {e}")
        return {}