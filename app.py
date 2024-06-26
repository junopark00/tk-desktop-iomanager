# Copyright (c) 2024 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

__author__ = "Juno Park"
__github__ = "https://github.com/junopark00"

import os
import sys
import traceback
from sgtk.platform import Application

# Append rez_path to Get variables from rez-env
sys.path.append('/RAPA/rez/src')

try:
    from rez.resolved_context import ResolvedContext
    use_rez = True
except ImportError:
    print("Rez not found. Run without Rez.")
    use_rez = False
    pass

class IO_Manager(Application):
    """
    The app entry point. This class is responsible for initializing and tearing down
    the application, handle menu registration etc.
    """

    def init_app(self):
        """
        Called as the application is being initialized
        """ 
        try:
            if use_rez:
                self.append_rez_env(
                    ["openpyxl", "openpyxl_image_loader", "ocio2"]
                    )
            tk_desktop_iomanager = self.import_module("app")

            menu_callback = lambda: tk_desktop_iomanager.dialog.show_dialog(self)
            menu_caption = "IO Manager"

            self.engine.register_command(menu_caption, menu_callback)
        except Exception:
            traceback.print_exc()
            
    def append_rez_env(self, rez_packages: list) -> None:
        """
        Get packages env from rez-env and append to variables.

        Args:
            rez_packages (list): List of packages to rez-env
        """
        context = ResolvedContext(rez_packages)
        env = context.get_environ()
        
        # Get env from rez_packages name
        openpyxl_path = env["REZ_OPENPYXL_ROOT"]
        openpyxl_image_loader_path = env["REZ_OPENPYXL_IMAGE_LOADER_ROOT"]
        ocio_path = env["OCIO"]
        
        # Check if rez_packages are found
        if not openpyxl_path:
            raise ValueError("Rez Package 'openpyxl' not found")
        
        if not openpyxl_image_loader_path:
            raise ValueError("Rez Package 'openpyxl_image_loader' not found")
        
        if not ocio_path:
            raise ValueError("Rez Package 'ocio2' not found")
        
        # append PYTHONPATH
        sys.path.append(openpyxl_path)
        sys.path.append(openpyxl_image_loader_path)
        
        # set OCIO
        os.environ["OCIO"] = ocio_path
            
    def destroy_app(self):
        """
        Tear down the app
        """
        self.log_debug("Destroying tk-desktop-iomanager")
