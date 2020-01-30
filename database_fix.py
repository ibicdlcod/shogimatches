from datetime import date

from metastruct import match_data
from importdata import match_auto


def fix_database():
    print("Fixing database...")
    matches = []
    match_auto.match_to_sql(matches)