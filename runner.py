from threading import Lock, Thread

from praw.models import Subreddit
from core import RedditScraper, DfHandler
from comment_parser import ParsedComment
from constants import SUBS_TO_SCRAPE, COMMENT_DF_LENGTH


regex = r"(?<![A-Z])(\$?)([A-Z]{2,5})(\s|$|\.)"


class Stream_Thread:
    lock = Lock()

    def __init__(self, subreddit: str, sub_instance: Subreddit) -> None:
        self.subreddit = subreddit
        self.stream = sub_instance.stream
        self.handler = DfHandler()

    def _comment_df_append(self):
        self.lock.acquire()
        try:
            for comment in self.stream.comments(skip_existing=True):
                parsed_comment = ParsedComment(comment, regex, reg_group=1)

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

                print(self.handler.sentiment_data)
                self.handler.pickle_df(dir=f"./shared/{self.subreddit}")

        finally:
            self.lock.release()

    def thread_comment_df_append(self):
        Thread(target=self._comment_df_append).start()


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

    while True:
        stream_threads = [
            Stream_Thread(sub, subreddits[sub]) for sub in subreddits
        ]
        for thread in stream_threads:
            thread.thread_comment_df_append()


if __name__ == "__main__":
    comment_df_producer(SUBS_TO_SCRAPE)
