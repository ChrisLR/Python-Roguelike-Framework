#!/usr/bin/env python
"""
The main entry point for the designer
"""

from designer.main import DesignerManager

if __name__ == '__main__':
    design_manager = DesignerManager()
    design_manager.start()
