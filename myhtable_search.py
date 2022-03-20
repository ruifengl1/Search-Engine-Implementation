# Got slate magazine data from http://www.anc.org/data/oanc/contents/
# rm'd .xml, .anc files, leaving just .txt
# 4534 files in like 55 subdirs

from htable import *
from words import get_text, words


def myhtable_create_index(files):
    """
    Build an index from word to set of document indexes
    This does the exact same thing as create_index() except that it uses
    your htable.  As a number of htable buckets, use 4011.
    Returns a list-of-buckets hashtable representation.
    """
    table = htable(4011)
    for file_index in range(len(files)):
        word_list = words(get_text(files[file_index]))
        for word in word_list:
            get_tuple = htable_get(table, word)
            if get_tuple:
                get_tuple.add(file_index)
            else:
                htable_put(table, word, {file_index})
    return(table)



def myhtable_index_search(files, index, terms): ## index is a table from above
    """
    This does the exact same thing as index_search() except that it uses your htable.
    I.e., use htable_get(index, w) not index[w].
    """
    tmp_list = list()
    for elem in terms:
        result = htable_get(index, elem)
        tmp_list.append(result if result else set())
    if tmp_list:
        return([files[idx] for idx in set.intersection(*tmp_list)])
    else:
        return([])