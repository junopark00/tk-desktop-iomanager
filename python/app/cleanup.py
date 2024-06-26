# -*- coding: utf-8 -*-

"""
When publishing was done, this file will be clean up the temporary files.
"""

__author__ = "Juno Park"
__github__ = "https://github.com/junopark00"


import sgtk

# set standard sgtk logger
logger = sgtk.platform.get_logger(__name__)


def cleanup_temp_files(completed_converters: list, cliplib: bool) -> None:
    """
    Clean up temporary script files.
    
    Args:
        completed_converters (list): List of completed converters
    """
    import os
    for completed_converter in completed_converters:
        if not os.path.exists(completed_converter):
            continue
        
        os.remove(completed_converter)
        
    if cliplib:
        print("This function is not implemented yet.")
        logger.info("This function is not implemented yet.")