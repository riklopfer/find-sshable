#!/usr/bin/env python3
"""
This script is for convenience and testing. 
"""
import sys

from find_sshable._command import main

try:
    sys.exit(main())
except KeyboardInterrupt:
    sys.exit(1)
