#!/usr/bin/env python
import os
from os.path import join as ojoin
import subprocess
SCRIPTDIR = os.path.abspath(os.path.dirname(__file__))

if __name__ == '__main__':
    psl_jar_file = ojoin(SCRIPTDIR, '..', '..', 'engines', 'psl-cli-CANARY.jar')
    output_dir = ojoin(SCRIPTDIR, 'output', 'psl_jar')

    cmd = ['java', '-jar', psl_jar_file, '-infer', 
        '-model', 'review.psl',
        '-data', 'review.data',
        '--output', output_dir]
    subprocess.check_call(cmd, cwd=SCRIPTDIR)
