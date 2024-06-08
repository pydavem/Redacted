"""
The meat of the machine, the redaction processes
"""


def get_out_filename(fnm):
    """ prepend 'redacted' to a file name string """
    fname = str(fnm)
    now = 0
    while now >= 0:
        last = now
        now = str(fname).find('/', last+1)

    if last >= 0:
        return fname[:last+1]+'redacted-'+fname[last+1:]

    return 'redacted-'+fname


def redact_file(localfile, redactips, redactlogins, redactmachines):
    """ redact a single file """

    new_file = None

    with open(localfile, 'r', encoding='utf-8') as in_file:
        new_file = get_out_filename(localfile)
        with open(new_file, 'w', encoding='utf-8') as out_file:
            for pre in in_file:
                post = redact_line(
                    pre, redactips, redactlogins, redactmachines)
                out_file.writelines(post)

    return new_file


def redact_line(text, redactips, redactlogins, redactmachines):
    """ redact a single line """

    ret = text

    if redactips:
        last = 0
        idx = 0
        count = 0
        start = -1
        maybe = 0

        ret = ''

        for c in text:
            # no need to check for hex! or (c >= 'a' and c <= 'f') or (c >= 'A' and c <= 'F'):
            if (c >= '0' and c <= '9'):
                if start == -1:
                    start = idx
                if count == 3:
                    maybe = 1
            elif c == '.':
                count += 1
            else:
                if maybe:
                    # strip from start to here
                    print(f'Found one at {start}')
                    ret += text[last:start]
                    ret += 'x.x.x.x'
                    last = idx

                start = -1
                maybe = 0
                count = 0
            idx += 1

        if maybe:
            # strip from start to here
            print(f'Found one at {start}')
            ret += text[last:start]
            ret += 'x.x.x.x'
        elif last < idx:
            # add any remaining characters to the string
            ret += text[last:]

    return ret
