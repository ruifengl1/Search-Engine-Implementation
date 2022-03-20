from collections import defaultdict  # https://docs.python.org/2/library/collections.html

from words import get_text, words


def create_index(files):
    """
    Given a list of fully-qualified filenames, build an index from word
    to set of document IDs. A document ID is just the index into the
    files parameter (indexed from 0) to get the file name. Make sure that
    you are mapping a word to a set of doc IDs, not a list.
    For each word w in file i, add i to the set of document IDs containing w
    Return a dict object mapping a word to a set of doc IDs.
    """
    file_index = defaultdict(set)
    for idx in range(len(files)):
        word_list = words(get_text(files[idx]))
        for word in word_list:
            file_index[word].add(idx)
    return(file_index)


def index_search(files, index, terms):
    """
    Given an index and a list of fully-qualified filenames, return a list of
    filenames whose file contents has all words in terms parameter as normalized
    by your words() function.  Parameter terms is a list of strings.
    You can only use the index to find matching files; you cannot open the files
    and look inside.
    """
    tmp_list = list()
    for elem in terms:
        tmp_list.append(index[elem])
    if tmp_list:
        return([files[idx] for idx in set.intersection(*tmp_list)])
    else:
        return([])
