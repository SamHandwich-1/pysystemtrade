"""
Mongo smoke: connect via pysystemtrade mongoDb, write/read a probe doc, exit.

Usage:
    python -m local.mongo_smoke
"""

from datetime import datetime, timezone

from sysdata.mongodb.mongo_connection import mongoDb


def main():
    db = mongoDb()
    print(db)

    collection = db.db["harness_smoke"]
    probe = {
        "_id": "mongo_smoke",
        "ok": True,
        "ts": datetime.now(timezone.utc).isoformat(),
        "note": "local first_system mongo slice",
    }
    collection.replace_one({"_id": probe["_id"]}, probe, upsert=True)
    got = collection.find_one({"_id": "mongo_smoke"})

    if not got or got.get("ok") is not True:
        print("FAIL: probe document missing or invalid:", got)
        return 1

    print("probe_ok=", got["ok"], "ts=", got.get("ts"))
    print("mongo_verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
