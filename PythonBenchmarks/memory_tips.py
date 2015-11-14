'''
Created on Nov 13, 2015

@author: vadimyusanenko
'''

datetime = None

def detect_current_datetime():
    global datetime
    if datetime is None:
        import datetime
    for _ in xrange(1000):
        datetime.datetime.now()

# slots
# generators
# iterators
# items and viewitems
# dicts and namedtuples