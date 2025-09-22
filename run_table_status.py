#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RACOON Status-Monitoring
Wrapper für src/tools/table_status.py
"""

import sys
from pathlib import Path

# Füge src-Verzeichnis zu Python Path hinzu
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

# Importiere und starte das Tool
from tools.table_status import main

if __name__ == "__main__":
    main()