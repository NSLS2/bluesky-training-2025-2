#!/usr/bin/env python3
"""Starting point for Crow's Nest"""

import argparse


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description="Crow's Nest -- choose the correct article",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("word", metavar="word", help="A word")

    return parser.parse_args()


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()
    word = args.word

    ## TO DO: Determine a condition to make the article 'a' or 'an'
    ## HINT: update condition to check if the word starts with a consonant
    article = "an" if word[0].lower() in "something" else "a"

    ## TO DO: Update the print statement to use f-string formatting for word and article
    ## HINT: word is {word} and article is {article}
    print(f"Hello World")


# --------------------------------------------------
if __name__ == "__main__":
    main()
