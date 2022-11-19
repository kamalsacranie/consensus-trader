import pandas as pd
import logging
import praw
import pickle
from datetime import datetime
from reddit.comment_parser import ParsedComment


class RedditScraper(praw.Reddit):
    # Wrapper around the classic praw api
    def __init__(self, site_name: str, conf_interp: str):
        super(self.__class__, self).__init__(
            site_name=site_name,
            config_interpolation=conf_interp,
        )

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


class DfHandler:
    # Any capital letter string of lengh two to 5 which is not preceeded by
    # other capital letters and may have an optional $ sign in front and is
    # succeeded by a space or end of line or full stop Outline cases would
    # be when someone goes all caps mid sentece, type a whole sentece caps
    # which could happen quite often actually. Also doesn't capture one
    # letter tickers

    def __init__(self) -> None:
        self.df_cols = ["comment", "tickers"]
        self.sentiment_data = pd.DataFrame(columns=self.df_cols)

    def append_data(self, parsed_comment: ParsedComment) -> None:
        """
        Appends a string to the comment column of our dataframe and
        a list of possible tickers from the comment to our ticker column
        """
        assert type(
            parsed_comment == ParsedComment
        ), "Method RedditScraper.append_data() takes a ParsedComment object"

        df_entry = pd.DataFrame(
            {
                self.df_cols[0]: parsed_comment.body,
                self.df_cols[1]: [parsed_comment.likely_tickers],
            },
            index=[datetime.now()],
        )
        self.sentiment_data = self.sentiment_data.append(df_entry)

    def pickle_df(self, dir: str):
        """
        Pickles our dataframe

        :param dir: a string of the file path and name without an extension
        """
        pickle.dump(self.sentiment_data, open(f"{dir}.p", "wb"))
