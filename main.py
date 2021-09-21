from time import sleep
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
    _ = start_reddit_scraper()
    while True:
        print("Hello look I'm running while the other thingy is running")
        sleep(3)


if __name__ == "__main__":
    main()
