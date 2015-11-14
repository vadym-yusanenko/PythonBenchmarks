"""
Created on Nov 12, 2015

@author: vadimyusanenko
"""

# Standard imports
from timeit import Timer

# TODO: ask for forgiveness
# TODO: point to tests that only valid for CPython


def benchmark_performance(benchmark_title, timer_instructions, cycles=1000000, omit_spacing=False):
    """
    Print test title and benchmark all available options, printing their performance results.
    """
    if not omit_spacing:
        print ""

    print "=> %s" % benchmark_title

    for timer_instruction in timer_instructions:
        print "    => %s: %s" % (
            timer_instruction[0],
            Timer(
                setup=timer_instruction[1],
                stmt=timer_instruction[2]
            ).timeit(cycles)
        )


benchmark_performance(
    "Appending characters to string",
    (
        (
            "append operator",
            'string_object = ""',
            "for substring in ('1','2','3','4','5'): string_object += substring"
        ),
        (
            "join method",
            "",
            "string_object = ''.join(('1','2','3','4','5'))"
        )
    ),
    omit_spacing=True
)


benchmark_performance(
    "Forming string",
    (
        (
            "Using add operator",
            "",
            'out = "<html>" + "head" + "prologue" + "query" + "tail" + "</html>"'
        ),
        (
            "Using string substitution",
            "",
            'out = "<html>%s%s%s%s</html>" % ("head", "prologue", "query", "tail")'
        )
    )
)


benchmark_performance(
    "Processing string",
    (
        (
            "Loop with append() after processing",
            'newlist = []; oldlist = [ str(item) for item in xrange(1000000) ]',
            'for word in oldlist: newlist.append(word.upper())'
        ),
        (
            "Functional processing via map()",
            'newlist = []; oldlist = [ str(item) for item in xrange(1000000) ]',
            'newlist = map(str.upper, oldlist)'
        ),
        (
            "List comprehension",
            'newlist = []; oldlist = [ str(item) for item in xrange(1000000) ]',
            'newlist = [s.upper() for s in oldlist]'
        )
    ),
    1
)


benchmark_performance(
    "Working with object references",
    (
        (
            "Full callable reference reevaluation",
            'newlist = []; oldlist = [ str(item) for item in range(1000000) ]',
            'for word in oldlist: newlist.append(str.upper(word))'
        ),
        (
            "Using direct reference to callable after first evaluation",
            (
                'newlist = []; oldlist = [ str(item) for item in range(1000000) ];'
                'append = newlist.append; upper = str.upper'
            ),
            'for word in oldlist: append(upper(word))'
        )
    ),
    1
)

benchmark_performance(
    "Global vs local variables",
    (
        (
            "Loop accessing global variables",
            (
                'global newlist; newlist = [];'
                'global oldlist; oldlist = [ str(item) for item in range(1000) ];'
                'global append; append = newlist.append; global upper; upper = str.upper;'
            ),
            'for word in oldlist: append(upper(word))'
        ),
        (
            "Loop accessing local variables via function scope",
            (
                'oldlist = [ str(item) for item in range(1000) ];\n'
                'def test_function():\n'
                '    newlist = []; append = newlist.append; upper = str.upper;\n'
                '    for word in oldlist: append(upper(word));'
            ),
            'test_function()'
        )
    ),
    1000
)


benchmark_performance(
    "Garbage collection impact",
    (
        (
            "Garbage collection enabled",
            'gc.enable()',
            'for _ in xrange(10): pass'
        ),
        (
            "Garbage collection disabled",
            "",
            'for _ in xrange(10): pass'
        )
    )
)


benchmark_performance(
    "Garbage collection impact",
    (
        (
            "Garbage collection enabled",
            'gc.enable()',
            'for _ in xrange(10): pass'
        ),
        (
            "Garbage collection disabled",
            "",
            'for _ in xrange(10): pass'
        )
    )
)


benchmark_performance(
    "Import statement overhead",
    (
        (
            "Import is declared outside of loop scope (global scope overhead acquired)",
            'import datetime',
            'for _ in xrange(1000): datetime.datetime.utcnow()'
        ),
        (
            "Import is declared inside loop scope (gains local variable speedup)",
            "",
            'for _ in xrange(1000):\n    import datetime\n    datetime.datetime.utcnow()'
        )
    ),
    100
)


# NOTE: if else does not suffer performance penalty
benchmark_performance(
    "Positioning of if blocks",
    (
        (
            "Rare conditions appear at the top",
            '',
            'for i in xrange(1000):\n    if i < 1: pass\n    elif i >= 1: pass\n    else: pass'
        ),
        (
            "Most frequent conditions appear at the top",
            "",
            'for i in xrange(1000):\n    if i >= 1: pass\n    elif i < 1: pass\n    else: pass'
        )
    ),
    10000
)


benchmark_performance(
    "Function call overhead",
    (
        (
            "Using inline logic with loop",
            '',
            'for i in xrange(1000): a = i + 1'
        ),
        (
            "Calling function with logic inside loop",
            "def test_function(argument): return argument + 1",
            'for i in xrange(1000):\n    a = test_function(i)'
        )
    ),
    1000
)


benchmark_performance(
    "CPython interpreter configuration",
    (
        (
            "Default configuration",
            '',
            'for _ in xrange(1000): pass'
        ),
        (
            "Tuning to check for signals and thread order less often",
            (
                "import sys;\n"
                "sys.setcheckinterval(1000)"
            ),
            'for _ in xrange(1000): pass'
        )
    ),
    10000
)


benchmark_performance(
    "Multiplying number by two",
    (
        (
            "Using multiply operator",
            'x = 1',
            'x = x * 2'
        ),
        (
            "Using shift operator",
            'x = 1',
            'x = x << 1'
        ),
        (
            "Adding number to itself",
            'x = 1',
            'x = x + x'
        )
    ),
    10000
)


benchmark_performance(
    "Generating an iteration range",
    (
        (
            "Using range()",
            '',
            'for _ in range(1000): pass'
        ),
        (
            "Using xrange()",
            '',
            'for _ in xrange(1000): pass'
        )
    ),
    10000
)


benchmark_performance(
    "Using while statement for loop",
    (
        (
            "Using while True",
            'x = 0',
            'while True:\n    if x != 10000: x += 1\n    else: break'
        ),
        (
            "Using while 1",
            'x = 0',
            'while 1:\n    if x != 10000: x += 1\n    else: break'
        )
    )
)


benchmark_performance(
    "Iterating over dict using .items() and .viewitems()",
    (
        (
            "Using .items()",
            'test_dict = { str(i): i for i in xrange(1000) }',
            'for _ in test_dict.items(): pass'
        ),
        (
            "Using .viewitems()",
            'test_dict = { str(i): i for i in xrange(1000) }',
            'for _ in test_dict.viewitems(): pass'
        )
    ),
    10000
)


benchmark_performance(
    "Use C extensions where applicable",
    (
        (
            "Using pickle",
            (
                'import pickle\n'
                'test_dict = { str(i): i for i in xrange(1000) }'
            ),
            'pickle.dumps(test_dict)'
        ),
        (
            "Using cPickle",
            (
                'import cPickle\n'
                'test_dict = { str(i): i for i in xrange(1000) }'
            ),
            'cPickle.dumps(test_dict)'
        )
    ),
    1000
)
