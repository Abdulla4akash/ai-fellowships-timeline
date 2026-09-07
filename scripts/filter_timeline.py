#!/usr/bin/env python3
"""
CLI filter tool for the AI Fellowships Timeline dataset.
Usage:
    python3 filter_timeline.py
    python3 filter_timeline.py --urgent
    python3 filter_timeline.py --country UK
    python3 filter_timeline.py --country USA
    python3 filter_timeline.py --category "8-12"
    python3 filter_timeline.py --category "Industry PhD"
    python3 filter_timeline.py --upcoming
"""
import argparse
import json
import os
from datetime import datetime, timedelta

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "fellowships.json")

def load_data():
    with open(DATA_PATH, "r") as f:
        return json.load(f)

def display_fellowships(fellowships):
    print(f"\nFound {len(fellowships)} matching fellowship(s):\n")
    print(f"{'Deadline':<26} | {'Country':<12} | {'Fellowship Name':<42} | {'Category'}")
    print("-" * 115)
    for f in fellowships:
        dl = f.get("deadline", "")[:25]
        country = f.get("country", "")[:11]
        name = f.get("name", "")[:41]
        cat = f.get("category", "")
        print(f"{dl:<26} | {country:<12} | {name:<42} | {cat}")
    print()

def main():
    parser = argparse.ArgumentParser(description="Query and filter AI Fellowships in UK & USA.")
    parser.add_argument("--country", choices=["UK", "USA", "Global", "all"], default="all", help="Filter by country/region")
    parser.add_argument("--category", type=str, default="", help="Filter by category substring (e.g. '8-12', 'Industry', 'Safety', 'Academic')")
    parser.add_argument("--upcoming", action="store_true", help="Sort by soonest deadline first")
    parser.add_argument("--urgent", action="store_true", help="Show only programs closing within the next 14 days (Sept 8 - Sept 20)")
    args = parser.parse_args()

    fellowships = load_data()

    if args.urgent:
        today = datetime(2026, 9, 7)
        two_weeks = today + timedelta(days=14)
        urgent = []
        for f in fellowships:
            dl_str = f.get("deadline_iso", "")
            if dl_str:
                try:
                    dl_date = datetime.strptime(dl_str, "%Y-%m-%d")
                    if today <= dl_date <= two_weeks:
                        urgent.append(f)
                except Exception:
                    pass
        fellowships = sorted(urgent, key=lambda x: x.get("deadline_iso", ""))
        print(f"\n🚨 URGENT: Showing {len(fellowships)} program(s) closing within 2 weeks:")
        display_fellowships(fellowships)
        return

    if args.country != "all":
        fellowships = [f for f in fellowships if args.country.lower() in f["country"].lower()]

    if args.category:
        fellowships = [f for f in fellowships if args.category.lower() in f["category"].lower()]

    if args.upcoming:
        fellowships = sorted(fellowships, key=lambda x: x.get("deadline_iso", "9999-12-31"))

    display_fellowships(fellowships)

if __name__ == "__main__":
    main()
