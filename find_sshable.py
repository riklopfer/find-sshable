#!/usr/bin/env python3
"""
This script is for convenience and testing. 
"""
import sys

from find_sshable.command import main_no_args

try:
    sys.exit(main_no_args())
except KeyboardInterrupt:
    sys.exit(1)
