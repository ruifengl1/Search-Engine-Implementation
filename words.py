import os
import re
import string
from jinja2 import Template

def filelist(root):
    """Return a fully-qualified list of filenames under root directory"""
    files_list = list()
    directory = os.path.expanduser(root)
    for subdir, dirs, files in os.walk(directory):
        for filename in files:
            filepath = subdir + os.sep + filename
            if filepath.endswith(".txt"):
                files_list.append(filepath)
    return(files_list)


def get_text(fileName):
    f = open(fileName, encoding='latin-1')
    s = f.read()
    f.close()
    return s


def words(text):
    """
    Given a string, return a list of words normalized as follows.
    Split the string to make words first by using regex compile() function
    and string.punctuation + '0-9\\r\\t\\n]' to replace all those
    char with a space character.
    Split on space to get word list.
    Ignore words < 3 char long.
    Lowercase all words
    """
    regex = re.compile('[' + re.escape(string.punctuation) + '0-9\\r\\t\\n]')
    nopunct = regex.sub(" ", text)  # delete stuff but leave at least a space to avoid clumping together
    words = nopunct.split(" ")
    words = [w for w in words if len(w) > 2]  # ignore a, an, to, at, be, ...
    words = [w.lower() for w in words]
    # print words
    return words


def results(docs, terms):
    """
    Given a list of fully-qualifed filenames, return an HTML file
    that displays the results and up to 2 lines from the file
    that have at least one of the search terms.
    Return at most 100 results.  Arg terms is a list of string terms.
    """
    results = dict()
    for filepath in docs:
        lines = get_text(filepath).splitlines()
        new_lines = []
        line_count = 0
        for line in lines:
            pattern = re.compile('|'.join(terms), re.IGNORECASE)
            if pattern.findall(line):
                norm_words = words(line)
                new_words = [ f"<b>{word}</b>" if word in terms else word for word in norm_words]
                new_line = ' '.join(new_words)
                new_lines.append(new_line)
                line_count +=1
            if line_count >= 2:
                break
        if new_lines:
            results[filepath] = (new_lines)
    return Template(open('template.html').read()).render(terms = ' '.join(terms), total_results = len(results), results = list(results.items())[:100])


def filenames(docs):
    """Return just the filenames from list of fully-qualified filenames"""
    if docs is None:
        return []
    return [os.path.basename(d) for d in docs]