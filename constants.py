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
]

SUBS_TO_SCRAPE = ["wallstreetbets", "investing", "stocks"]

COMMENT_DF_LENGTH = 1000

REGEX = r"(?<![A-Z])(\$?)([A-Z]{2,5})(\s|$|\.)"
