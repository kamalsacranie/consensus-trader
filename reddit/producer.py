import re
from typing import List
from .core import RedditScraper
from .comment_parser import ParsedComment


SUBS_TO_SCRAPE = ["wallstreetbets"]
DF_LENGTH = 1000

def comment_df_producer(subs: List[str], debug: bool=False) -> None:
    """
    Main function which has options for debugging

    :debug: Enable debug or not
    """

    reddit = RedditScraper(
        subs=subs,
        site_name='sentimentbot',
        conf_interp='basic'
    )

    if debug:
        reddit.enable_debug()

    assert reddit.read_only, "Not in read only mode"

    # Opening the stream for our subreddits
    subreddit = reddit.subreddit(SUBS_TO_SCRAPE[0])
    sub_stream = subreddit.stream
    # Regex we want to use when parsing our comment
    regex = r"(?<![A-Z])(\$?)([A-Z]{2,5})(\s|$|\.)"

    while True:

        try:
            for comment in sub_stream.comments(skip_existing=True):
                parsed_comment = ParsedComment(
                    comment,
                    regex,
                    reg_group=1,
                )

                # filtering for when someone types in all caps
                if not parsed_comment.body.isupper():
                    likely_tickers = parsed_comment.likely_tickers
                    if bool(likely_tickers):
                        reddit.append_data(parsed_comment)

                # Cropping to be 1000 or length
                reddit.sentiment_data = reddit.sentiment_data.tail(
                    min(DF_LENGTH, len(reddit.sentiment_data.index))
                )
                print(reddit.sentiment_data)
        
        except (re.error or AttributeError) as e:
            print(e)
