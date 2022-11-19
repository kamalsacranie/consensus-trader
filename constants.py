TICKER_BLACKLIST = [
    "DD",
    "YOLO",
    "LOL",
    "LMAO",
    "USD",
    "LED",
    "TV",
    "US",
    "MD",
    "IPO",
    "LMFAO",
    "SPY",
    "QQQ",
    "USA",
    "WSB",
    "GTFO",
    "ETF",
    "FED",
]

SUBS_TO_SCRAPE = ["wallstreetbets", "investing", "stocks"]
# SUBS_TO_SCRAPE = ["investing"]

COMMENT_DF_LENGTH = 1000

REGEX = r"(?<![A-Z])(\$?)([A-Z]{2,5})(\s|$|\.)"
