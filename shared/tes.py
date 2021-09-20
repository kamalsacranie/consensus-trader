import praw
from praw.models.reddit.subreddit import SubredditStream
from threading import Lock, Thread


def stream_sub(lk: Lock, subreddit: str, sub_stream: SubredditStream):
    lk.acquire()
    try:
        for comment in sub_stream.comments():
            print(f"{subreddit}: {comment.body[:20]}")
    finally:
        lk.release()


lock = Lock()

subs_to_scrape = ["wallstreetbets", "stocks", "investing"]
reddit = praw.Reddit(site_name="sentimentbot", config_interpolation="basic")

praw_streams = {i: reddit.subreddit(i).stream for i in subs_to_scrape}
thread_streams = dict()

for sub in praw_streams:
    thread_streams[sub] = Thread(
        target=stream_sub, args=(lock, sub, praw_streams[sub])
    )

for thread in thread_streams:
    thread_streams[thread].start()
