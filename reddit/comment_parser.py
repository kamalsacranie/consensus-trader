import re
from typing import List
from dataclasses import dataclass


TICKER_BLACKLIST = ['DD', 'YOLO', 'LOL', 'LMAO', 'USD', 'LED', 'TV', 'US']

@dataclass
class ParsedComment(object):

    """
    ParsedComment object for our redding comment and its methods if it so
    requires. We use a dataclass to pass in a praw comment object and a regex
    of our choice so that we can parse the comment for something specific
    """

    comment: str
    regex: str
    reg_group: int
    str_len: int = 1000

    def __post_init__(self):
        self.body = self.comment.body
        if len(self.body) <= self.str_len:
            self.likely_tickers = self._parse_tickers()

    def _parse_tickers(self) -> List[str]:
        """
        Returns a list of desired regex substrings/tickers
        """
        
        # finding all the 2-5 length all caps words in the comment body
        raw_tickers = re.findall(self.regex, self.body)

        # parsing through our list of raw tickers. our raw ticker is located in
        # the group of our regex. We get back a list of tickers which we
        # convert to a set to get rid of duplitcates
        likely_tickers = set([ticker[self.reg_group] for ticker in raw_tickers])

        # Filtering for tickers in our blacklist
        likely_tickers = [ticker for ticker in likely_tickers 
                if ticker not in TICKER_BLACKLIST]
        print(f'{__name__}: {likely_tickers = }')

        return likely_tickers
