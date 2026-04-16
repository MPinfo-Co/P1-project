"""
SSB log 擷取腳本。

從 SSB 拉取指定時間區間的 log，預彙總後 POST 至 P1-code /api/ingest。

用法：
    python fetch_logs.py                          # 拉取過去 20 分鐘
    python fetch_logs.py --from 2024-01-15T00:00 --to 2024-01-15T06:00
    python fetch_logs.py --dry-run                # 僅顯示筆數，不送 ingest
"""

import argparse
import json
import logging
import sys
from datetime import datetime, timedelta, timezone

import httpx

from config import settings
from log_preaggregator import preaggregate
from ssb_client import SSBClient

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)


def _parse_dt(s: str) -> datetime:
    """解析 ISO 8601 字串為 UTC datetime。"""
    dt = datetime.fromisoformat(s)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def _build_payload(
    time_from: datetime,
    time_to: datetime,
    logs: list[dict],
    analysis_mode: str,
) -> dict:
    """組裝 ingest payload。"""
    if analysis_mode == "full":
        forti_summaries, windows_logs = preaggregate(logs)
        records = forti_summaries + windows_logs
    else:
        records = logs

    return {
        "time_from": time_from.isoformat(),
        "time_to": time_to.isoformat(),
        "records_fetched": len(logs),
        "analysis_mode": analysis_mode,
        "logs": records,
    }


def _post_ingest(payload: dict) -> None:
    """POST payload 至 P1-code /api/ingest。"""
    url = f"{settings.P1_CODE_URL}/api/ingest"
    headers = {"X-Ingest-Key": settings.INGEST_SECRET}

    with httpx.Client(timeout=300.0) as client:
        resp = client.post(url, json=payload, headers=headers)

    if resp.status_code == 200:
        result = resp.json()
        logger.info(f"Ingest success: {result}")
    else:
        logger.error(f"Ingest failed: HTTP {resp.status_code} — {resp.text}")
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch logs from SSB and send to P1-code ingest")
    parser.add_argument(
        "--from",
        dest="time_from",
        metavar="DATETIME",
        help="Start time (ISO 8601). Default: now - FLASH_INTERVAL_MINUTES",
    )
    parser.add_argument(
        "--to",
        dest="time_to",
        metavar="DATETIME",
        help="End time (ISO 8601). Default: now",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Fetch and preaggregate only, do not POST to ingest",
    )
    args = parser.parse_args()

    now = datetime.now(timezone.utc)
    time_to = _parse_dt(args.time_to) if args.time_to else now
    time_from = (
        _parse_dt(args.time_from)
        if args.time_from
        else now - timedelta(minutes=20)
    )

    logger.info(f"Fetching logs: {time_from.isoformat()} ~ {time_to.isoformat()}")
    logger.info(f"Analysis mode: {settings.ANALYSIS_MODE}")

    ssb = SSBClient()
    try:
        logs = ssb.fetch_logs(
            time_from,
            time_to,
            settings.effective_search_expression,
        )
    finally:
        ssb.close()

    logger.info(f"Fetched {len(logs)} raw logs from SSB")

    payload = _build_payload(time_from, time_to, logs, settings.ANALYSIS_MODE)

    if args.dry_run:
        logger.info(
            f"[dry-run] Would send {len(payload['logs'])} records to {settings.P1_CODE_URL}/api/ingest"
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False, default=str))
        return

    _post_ingest(payload)


if __name__ == "__main__":
    main()
