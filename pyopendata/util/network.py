# pylint: disable-msg=E1101,W0613,W0603

from __future__ import unicode_literals
from __future__ import division

import os
import sys


class ProgressBar:

    """Display Progress Bar

    Parameters
    ----------
    total : int
        Total size to be processed
    length:
        Number of progress bar characters"""

    def __init__(self, total=None, length=20):
        if total is None:
            raise ValueError('Provide total number to be prosessed')

        self.total = total
        self.length = length
        self.current = 0

    def update(self, current):
        self.current += current

        done = int(self.length * self.current / self.total)
        if done > self.length:
            # not to exceed total length
            done = self.length

        sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (self.length - done)) )
        sys.stdout.flush()

        if self.current >= self.total:
            sys.stdout.write(os.linesep)
