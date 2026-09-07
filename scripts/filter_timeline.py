#!/usr/bin/env python3
"""
CLI filter tool for the AI Fellowships Timeline dataset.
Usage:
    python3 filter_timeline.py
    python3 filter_timeline.py --country UK
    python3 filter_timeline.py --country USA
    python3 filter_timeline.py --category "Industry PhD"
    python3 filter_timeline.py --upcoming
"""
import argparse
import json
import os
from datetime import datetime

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "fellowships.json")

def load_data():
    with open(DATA_PATH, "r") as f:
        return json.load(f)

def display_fellowships(fellowships):
    print(f"\nFound {len(fellowships)} matching fellowship(s):\n")
    print(f"{'Deadline':<25} | {'Country':<12} | {'Fellowship Name':<45} | {'Category'}")
    print("-" * 115)
    for f in fellowships:
        dl = f.get("deadline", "")[:24]
        country = f.get("country", "")[:11]
        name = f.get("name", "")[:44]
        cat = f.get("category", "")
        print(f"{dl:<25} | {country:<12} | {name:<45} | {cat}")
    print()

def main():
    parser = argparse.ArgumentParser(description="Query and filter AI Fellowships in UK & USA.")
    parser.add_argument("--country", choices=["UK", "USA", "Global", "all"], default="all", help="Filter by country/region")
    parser.add_argument("--category", type=str, default="", help="Filter by category substring (e.g. 'Industry', 'Safety', 'Academic')")
    parser.add_argument("--upcoming", action="store_true", help="Sort by soonest deadline first")
    args = parser.parse_args()

    fellowships = load_data()

    if args.country != "all":
        fellowships = [f for f in fellowships if args.country.lower() in f["country"].lower()]

    if args.category:
        fellowships = [f for f in fellowships if args.category.lower() in f["category"].lower()]

    if args.upcoming:
        fellowships = sorted(fellowships, key=lambda x: x.get("deadline_iso", "9999-12-31"))

    display_fellowships(fellowships)

if __name__ == "__main__":
    main()
