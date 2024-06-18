"""
The meat of the machine, the redaction processes
"""
import os
import mmap
from results import Results


def get_out_filename(fnm):
    """ prepend 'redacted' to a file name string """
    fname = str(fnm)
    now = 0
    while now >= 0:
        last = now
        now = str(fname).find('/', last+1)

    if last >= 0:
        # if we have previously generated it, leave it alone
        if fname[last+1:last+10] == 'redacted-':
            return None
        return fname[:last+1]+'redacted-'+fname[last+1:]

    return 'redacted-'+fname


def redact_file(localfile, *opts):
    """ redact a single file """
    redactips, redactmacs, redactmachines, redactlogins = opts

    res = Results()
    new_file = None

    with open(localfile, 'r', encoding='utf-8') as in_file:
        new_file = get_out_filename(localfile)
        if new_file is None:
            return None
        file_stat = os.stat(localfile)
        mm_size = 0
        # use a memory mapped file, only write it to disk if redactions are performed
        # we over-estimate the amount of memory required, just to be safe!
        with mmap.mmap(-1, file_stat.st_size*2) as mm:
            for pre in in_file:
                post = redact_line(
                    pre, res, redactips, redactmacs, redactmachines, redactlogins)
                mm.write(post.encode('utf-8'))
                # remember the count written to memory for saving
                mm_size += len(post)

            if not res.is_empty():
                mm.flush()
                mm.seek(0)
                with open(new_file, 'w+b') as out_file:
                    out_file.write(mm.read(mm_size))
                    # add our tag!
                    out_file.write(
                        b'\n\nRedacted by Redacted v1.0 from PyDaveM\n')

                res.add_file(new_file)
                return res

    return None


def redact_line(text, res: Results, *opts):
    """ redact a single line """
    redactips, redactmacs, redactmachines, redactlogins = opts
    ret = text

    if redactips:
        # redact IPs (n.n.n.n converted to x.x.x.x)
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
                    ret += text[last:start]
                    ret += 'x.x.x.x'
                    last = idx
                    res.add_ip()

                start = -1
                maybe = 0
                count = 0
            idx += 1

        if maybe:
            # strip from start to here
            print(f'Found one at {start}')
            ret += text[last:start]
            ret += 'x.x.x.x'
            res.add_ip()
        elif last < idx:
            # add any remaining characters to the string
            ret += text[last:]

    if redactlogins:
        idx = 0
        for c in ret:
            if c.isspace():
                break
            if c == '@':
                if idx:
                    ret = 'username'+ret[idx:]
                    res.add_login()
                break
            idx += 1

    if redactmachines:
        start = 0
        idx = 0
        for c in ret:
            if c.isspace():
                break
            if c == '@' and not start:
                start = idx
            if start and c == '>' or c == '$':
                ret = ret[:start+1]+'machine'+ret[idx:]
                res.add_machine()
                break
            idx += 1

    if redactmacs:
        found = 1
        while found:
            digit = 0   # 2 digits between ':'s
            found = 0   # check more than once per line, recursive because i'm lazy!
            start = -1
            count = 0
            idx = 0
            for c in ret:
                if (c >= '0' and c <= '9') or (c >= 'A' and c <= 'F') or (c >= 'a' and c <= 'f'):
                    digit += 1
                    if digit > 2:
                        start = -1
                        count = 0
                        digit = 0
                    else:
                        if start == -1:
                            start = idx
                        count += 1
                        if count == 12:
                            ret = ret[:start]+'--:--:--:--:--:--'+ret[idx+1:]
                            found = 1
                            res.add_mac()
                            break
                elif not c == ':':
                    start = -1
                    count = 0
                else:
                    digit = 0
                idx += 1

    return ret
