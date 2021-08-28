import pandas as pd
import logging
import praw
from typing import List
from datetime import datetime
from .comment_parser import ParsedComment


class RedditScraper(praw.Reddit):

    def __init__(self, subs: List[str], site_name: str, conf_interp: str):
        super(self.__class__, self).__init__(
            site_name=site_name,
            config_interpolation=conf_interp,
        )
        self.subreddits = '+'.join(subs)
        # Any capital letter string of lengh two to 5 which is not preceeded by other
        # capital letters and may have an optional $ sign in front and is succeeded by
        # a space or end of line or full stop
        # Outline cases would be when someone goes all caps mid sentece, type a whole
        # sentece caps which could happen quite often actually. Also doesn't capture
        # one letter tickers
        self.sentiment_cols = ['comment', 'tickers']
        self.sentiment_data = pd.DataFrame(columns=self.sentiment_cols)

    def enable_debug(self) -> None:
        """
        Enables debugging using the loggin module and praw built in settings
        """
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        for logger_name in ("praw", "prawcore"):
            logger = logging.getLogger(logger_name)
            logger.setLevel(logging.DEBUG)
            logger.addHandler(handler)

    def append_data(self, parsed_comment: ParsedComment) -> None:
        """
        Appends a string to the comment column of our dataframe and
        a list of possible tickers from the comment to our ticker column
        """
        assert type(parsed_comment == ParsedComment), "Method RedditScraper.append_data() takes a ParsedComment object"

        df_entry = pd.DataFrame(
            {
                self.sentiment_cols[0]: parsed_comment.body,
                self.sentiment_cols[1]: [parsed_comment.likely_tickers], 
            }, 
            index=[datetime.now()]
        )
        self.sentiment_data = self.sentiment_data.append(df_entry)
