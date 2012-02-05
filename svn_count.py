from collections import defaultdict
from pprint import pprint
import re
from subprocess import Popen, PIPE

# Call svn log on the repo.  Parse the lines that look like this:
# r545 | jesse.aldridge | 2012-02-03 19:43:41 -0600 (Fri, 03 Feb 2012) | 1 line

path_to_project = '/path/to/my/project'
print 'checking log...'
p = Popen('svn log'.split(), cwd=path_to_project, stdout=PIPE)
log_lines = p.communicate()[0].splitlines()
log_lines = [line for line in log_lines if re.search('^r[0-9]+', line)]

normal_lines = defaultdict(int)
counting_monsters = defaultdict(int)

for line in log_lines:
    rev, name, date, lines_committed = [s.strip() for s in line.split('|')]
    rev = int(rev[1:])

    # Run svn diff.  Pull out the + and - lines.  Ignore if too many.

    print '-------------------------'
    print 'rev:', rev
    print 'name:', name

    p = Popen('svn diff -c {0}'.format(rev).split(),
              cwd=path_to_project, stdout=PIPE)
    diff_lines = p.communicate()[0].splitlines()
    diff_lines = [line for line in diff_lines
                  if re.search('^[\+|\-][^\+|\-]', line)]
    num_lines = len(diff_lines)
    counting_monsters[name] += num_lines
    if len(diff_lines) < 100:
        pprint(diff_lines)
        normal_lines[name] += num_lines

    # Print as we go.

    print 'just counting normal commits:'
    pprint(dict(normal_lines))
    print 'counting monster commits:'
    pprint(dict(counting_monsters))