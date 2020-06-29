from pyparsing import *

itemlist = delimitedList(oneOf("alpha beta gamma"), '|')
def verify(toks):
    print(toks)
    return len(set(toks)) == len(toks)
itemlist.addCondition(verify, "duplicate list entries found")

s = """alpha|beta
alpha|gamma
gamma
beta|beta|beta|alpha|beta|alpha
"""

print(itemlist.searchString("alpha|beta"))
