from multiprocessing import Process
from reddit import runner
from constants import SUBS_TO_SCRAPE


def start_reddit_scraper(debug: bool = False) -> Process:
    scraper = Process(
        target=runner.comment_df_producer,
        args=(SUBS_TO_SCRAPE, debug),
    )
    scraper.start()
    return scraper


def main():
    # 1. Scrape,
    # 2. use NLTK or Vader to use a dictionary to rank
    _ = start_reddit_scraper()


if __name__ == "__main__":
    main()
