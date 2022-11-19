from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Lock

from praw.models import Subreddit
from reddit.core import RedditScraper, DfHandler
from reddit.comment_parser import ParsedComment
from constants import SUBS_TO_SCRAPE, COMMENT_DF_LENGTH, REGEX


class StreamThread:
    def __init__(self, subreddit: str, sub_instance: Subreddit) -> None:
        self.subreddit = subreddit
        self.stream = sub_instance.stream
        self.handler = DfHandler()
        # Just temp to debug what error types we get
        self._lock = Lock()

    def comment_df_append(self):
        try:
            for comment in self.stream.comments(skip_existing=True):
                parsed_comment = ParsedComment(comment, REGEX, reg_group=1)

                # filtering for when someone types in all caps
                if not parsed_comment.body.isupper():
                    likely_tickers = parsed_comment.likely_tickers
                    if bool(likely_tickers):
                        self.handler.append_data(parsed_comment)

                # Cropping to be 1000 or length
                self.handler.sentiment_data = self.handler.sentiment_data.tail(
                    min(
                        COMMENT_DF_LENGTH,
                        len(self.handler.sentiment_data.index),
                    )
                )

                self.handler.pickle_df(dir=f"./shared/{self.subreddit}")
        except AttributeError:
            print(
                "This attribute error happens where Parsed comment has no atrribute likey_tickers"
            )
        # Just to find the errors we get
        except Exception as e:
            with self._lock:
                while True:
                    print(e)

    def __str__(self) -> str:
        return f"{self.subreddit}"


def comment_df_producer(subs: list[str], debug: bool = False) -> None:
    """
    Main function which has options for debugging

    :debug: Enable debug or not
    """

    # site name is the name of your config
    reddit = RedditScraper(site_name="sentimentbot", conf_interp="basic")

    if debug:
        reddit.enable_debug()

    assert reddit.read_only, "Not in read only mode"

    # Opening the stream for our subreddits.
    subreddits = {sub: reddit.subreddit(sub) for sub in subs}

    with ThreadPoolExecutor(len(SUBS_TO_SCRAPE)) as executor:
        executor.map(
            lambda i: StreamThread(i[0], i[1]).comment_df_append(),
            subreddits.items(),
        )


if __name__ == "__main__":
    comment_df_producer(SUBS_TO_SCRAPE)
