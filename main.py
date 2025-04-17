from scrape_ebay import get_ebay_listings
from langchain_flows import parse_listing
from matchmaker import match_listing, buyers
from logger import open_csv


def run_flipbot():
    listings = get_ebay_listings()

    for listing in listings:
        print(f"\n🛒 {l['title']}")
        parsed = parse_listing(l["title"])
        print(f"🧠 Parsed → {parsed}")
        result = match_listing(parsed, buyers)
        print(result)


if __name__ == "__main__":
    run_flipbot()

open_csv()
