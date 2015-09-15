from __future__ import print_function

import json
import os
import sys

from IPython.kernel.kernelspec import install_kernel_spec
from IPython.utils.tempdir import TemporaryDirectory

kernel_json = {
 "argv":[sys.executable, "-m", "stata_kernel", "-f", "{connection_file}"],
 "display_name": "Stata",
 "language": "stata"
}


def install_my_kernel_spec(user=True):
    with TemporaryDirectory() as td:
        os.chmod(td, 0o755) # Starts off as 700, not user readable
        with open(os.path.join(td, 'kernel.json'), 'w') as f:
            json.dump(kernel_json, f, sort_keys=True)

        print('Installing IPython kernel spec')
        install_kernel_spec(td, 'stata', user=user, replace=True)
    

if __name__ == '__main__':
    install_my_kernel_spec()
