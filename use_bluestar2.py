import bluestar
import use_bluestar_lib

def is_target_ok(s):
    try:
        parse(s)
    except:
        return False
    return True

# iter 1
def parse(s):
    raise NotImplementedError

e_plus = ['a', '||', '|a|']
e_minus = ['|']
chars = 'a|'

# iter2
def parse(s):
    in_quote = False
    for c in s:
        if c == '|':
            in_quote = not in_quote

    if in_quote: raise AssertionError

e_plus = ['a', '||', '|a|', 'aa']
e_minus = ['|']

# iter3
chars = 'a|b'

def parse(s):
    in_quote = False
    to_escape = False
    for c in s:
        if c == '|':
            in_quote = not in_quote
        elif c == 'b':
            to_escape = True

    if in_quote: raise AssertionError
    if to_escape: raise AssertionError

# iter4
e_plus = ['a', '||', '|a|', 'aa', 'ab|a']
e_minus = ['|']

e_plus = ['a', '||', '|a|', 'aa', 'ab|a']
e_minus = ['|', 'a|', 'ab']

# iter5

def parse(s):
    in_quote = False
    to_escape = False
    for c in s:
        if to_escape:
            to_escape = False
            continue

        if c == '|':
            in_quote = not in_quote
        elif c == 'b':
            to_escape = True

    if in_quote: raise AssertionError
    if to_escape: raise AssertionError

e_plus = ['a', '||', '|a|', 'aa', 'ab|a', 'aba', 'ab|', 'abb']
e_minus = ['|', 'a|', 'ab']

# iter6: value testing

def parse(s):
    """
    >>> parse('a')
    ['a']
    """
    in_quote = False
    to_escape = False
    result = []
    buf = []
    for c in s:
        if to_escape:
            to_escape = False
            continue

        if c == '|':
            in_quote = not in_quote
        elif c == 'b':
            to_escape = True
        else:
            buf.append(c)

    if in_quote: raise AssertionError
    if to_escape: raise AssertionError
    result.append(''.join(buf))
    return result

# iter7: value testing

def parse(s):
    """
    >>> parse('a')
    ['a']
    >>> parse('||')
    ['']
    >>> parse('|a|')
    ['a']
    >>> parse('ab|a')
    ['a|a']
    >>> parse('aba')
    ['aa']
    >>> parse('ab|')
    ['a|']
    >>> parse('abb')
    ['ab']
    """
    in_quote = False
    to_escape = False
    result = []
    buf = []
    for c in s:
        if to_escape:
            buf.append(c)
            to_escape = False
            continue

        if c == '|':
            in_quote = not in_quote
        elif c == 'b':
            to_escape = True
        else:
            buf.append(c)

    if in_quote: raise AssertionError
    if to_escape: raise AssertionError
    result.append(''.join(buf))
    return result

# iter8: add comma
chars = 'a|b,'
e_plus = ['a', '||', '|a|', 'aa', 'ab|a', 'aba', 'ab|', 'abb',
          ',', 'a,', 'ab,']
e_minus = ['|', 'a|', 'ab']

#iter9: value testing with comma

def parse(s):
    """
    >>> parse('a')
    ['a']
    >>> parse('||')
    ['']
    >>> parse('|a|')
    ['a']
    >>> parse('ab|a')
    ['a|a']
    >>> parse('aba')
    ['aa']
    >>> parse('ab|')
    ['a|']
    >>> parse('abb')
    ['ab']
    >>> parse(',')
    ['', '']
    >>> parse('a,')
    ['a', '']
    >>> parse('ab,')
    ['a,']
    """
    in_quote = False
    to_escape = False
    result = []
    buf = []
    for c in s:
        if to_escape:
            buf.append(c)
            to_escape = False
            continue

        if c == '|':
            in_quote = not in_quote
        elif c == 'b':
            to_escape = True
        elif c == ',':
            result.append(''.join(buf))
            buf = []
        else:
            buf.append(c)

    if in_quote: raise AssertionError
    if to_escape: raise AssertionError
    result.append(''.join(buf))
    return result

# iter10 change predicate
def is_target_ok(s):
    try:
        assert len(parse(s)) == 1
    except:
        return False
    return True

e_plus = ['a', '||', '|a|', 'aa', 'ab|a', 'aba', 'ab|', 'abb',
          'ab,', 'ba', '|ba|', '|b||', '|bb|', '|b,|']
e_minus = ['|', 'a|', 'ab', ',', 'a,', 'b', '|b|', '|baa', 'a||']


#iter11

def parse(s):
    """
    >>> parse('a')
    ['a']
    >>> parse('||')
    ['']
    >>> parse('|a|')
    ['a']
    >>> parse('ab|a')
    ['a|a']
    >>> parse('aba')
    ['aa']
    >>> parse('ab|')
    ['a|']
    >>> parse('abb')
    ['ab']
    >>> parse(',')
    ['', '']
    >>> parse('a,')
    ['a', '']
    >>> parse('ab,')
    ['a,']
    >>> parse('ba')
    ['a']
    >>> parse('|ba|')
    ['a']
    >>> parse('|b||')
    ['|']
    >>> parse('|bb|')
    ['b']
    >>> parse('|b,|')
    [',']
    """
    in_quote = False
    to_escape = False
    result = []
    buf = []
    for c in s:
        if to_escape:
            buf.append(c)
            to_escape = False
            continue

        if c == '|':
            if not in_quote:
                if buf:
                    raise AssertionError
            in_quote = not in_quote
        elif c == 'b':
            to_escape = True
        elif c == ',':
            result.append(''.join(buf))
            buf = []
        else:
            buf.append(c)

    if in_quote: raise AssertionError
    if to_escape: raise AssertionError
    result.append(''.join(buf))
    return result

e_plus = ['a', '||', '|a|', 'aa', 'ab|a', 'aba', 'ab|', 'abb',
          'ab,', 'ba', '|ba|', '|b||', '|bb|', '|b,|', '||||', '||a', '|aa|', '||ba', 'bb||',
          'b|', 'bb', 'b,', 'bba']
e_minus = ['|', 'a|', 'ab', ',', 'a,', 'b', '|b|', '|baa', 'a||', '|b', '||b', 'bb||', '|b|a', '|bba', 'bb||', '|||', '|b,', 'bb|', 'b|||', '|a|||']

## auto testing
dfa = bluestar.bluestar(e_plus, e_minus)
use_bluestar_lib.write_dfa(dfa)



def find_mismatch(dfa, limit=10, bluteforce=False):
    cur = [[c] for c in chars]
    next = []
    count = 0
    while cur:
        for s in cur:
            if len(s) > limit:
                print 'no mismatch found in len <= %d (%d tests)' % (limit, count)
                return
            #print s
            count += 1
            d = dfa.is_ok(s)
            f = is_target_ok(s)
            if bool(d) != f:
                print '%d: for input \'%s\': dfa said %s, but target said %s' % (
                    count, ''.join(s), bool(d), f)
                return s
            if d != None or bluteforce:
                for c in chars:
                    next.append(s + [c])
        cur = next

def _test():
    import doctest
    doctest.testmod()
    find_mismatch(dfa)

_test()
