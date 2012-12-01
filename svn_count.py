from collections import defaultdict
from pprint import pprint
import re
from subprocess import Popen, PIPE

class SvnCounter:
    def __init__(self, path_to_project=None, url=None):
        ' Init state. '

        self.normal_lines = defaultdict(int)
        self.counting_monsters = defaultdict(int)
        self.path_to_project = path_to_project
        self.url = url

    def svn_cmd(self, inner_cmd, line_regex):
        ' Run svn command.  Return output lines matching line_regex. '

        url = self.url
        full_cmd = 'svn {0} {1}'.format(inner_cmd, url if url else '')
        print 'full_cmd:', full_cmd
        p = Popen(full_cmd.split(), cwd=self.path_to_project, stdout=PIPE)
        log_lines = p.communicate()[0].splitlines()
        return [line for line in log_lines if re.search(line_regex, line)]

    def svn_diff(self, rev, name):
        ' Run svn diff.  Pull out the + and - lines.  Ignore if too many. '

        print '-------------------------'
        print 'rev:', rev
        print 'name:', name
        diff_lines = self.svn_cmd(
            'diff -c {0} --diff-cmd diff'.format(rev), 
            line_regex='^[\+|\-][^\+|\-]')
        num_lines = len(diff_lines)
        self.counting_monsters[name] += num_lines
        if num_lines < 100:
            pprint(diff_lines)
            self.normal_lines[name] += num_lines

    def go(self):
        ' example line:  r545 | jesse.aldridge | 2012-02-03 19:43:41 -0600 (Fri, 03 Feb 2012) | 1 line'

        log_lines = self.svn_cmd('log --limit 100', line_regex='^r[0-9]+')
        for line in log_lines:
            rev, name, date, lines_committed = [
                s.strip() for s in line.split('|')]
            rev = int(rev[1:])

            self.svn_diff(rev, name)

            print 'just counting normal commits:'
            pprint(dict(self.normal_lines))
            print 'counting monster commits:'
            pprint(dict(self.counting_monsters))

if __name__ == '__main__':
    SvnCounter(url='http://dev.zenoss.com/svnint/').go()
