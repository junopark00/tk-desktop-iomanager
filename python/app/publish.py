"""
If this script is executed, it will call "generate_converter.py".

If the conversion is successfully completed,
this script will publish converted video and data to the ShotGrid.

Finally, it will call "cleanup.py" to clean up the temporary files.
"""

__author__ = "Juno Park"
__github__ = "https://github.com/junopark00"

import os
import sgtk


# Set standard sgtk logger
logger = sgtk.platform.get_logger(__name__)


class Publish:
    def __init__(self, data: list, colorspace: str):
        self.data = data
        self.colorspace = colorspace
        
        self._app = sgtk.platform.current_bundle()
        self._sg = self._app.shotgun
    
    def publish_to_shotgrid(self) -> None:
        """
        Publishes the version data to ShotGrid.
        """
        version_data = {}
        for row, data in enumerate(self.data):
            version_entry = {}
            version_entry["project"] = self._app.context.project
            version_entry["sg_roll"] = data["roll"]
            version_entry["sg_version_1"] = data["version"]
            version_entry["sg_type"] = data["type"]
            version_entry["sg_scan_path_1"] = data["scan_path"]
            version_entry["sg_scan_name"] = data["scan_name"]
            version_entry["sg_clip_name"] = "\n".join(data["clip_name"]) if isinstance(data["clip_name"], list) else data["clip_name"]
            version_entry["sg_pad"] = data["pad"]
            version_entry["sg_ext"] = data["ext"]
            version_entry["sg_resolution"] = data["resolution"]
            version_entry["sg_start_frame"] = str(data["start_frame"])
            version_entry["sg_end_frame"] = str(data["end_frame"])
            version_entry["sg_duration"] = str(data["duration"])
            version_entry["sg_retime_duration"] = "\n".join(data["retime_duration"]) if isinstance(data["retime_duration"], list) else data["retime_duration"]
            version_entry["sg_retime_percent"] = "\n".join(data["retime_percent"]) if isinstance(data["retime_percent"], list) else data["retime_percent"]
            version_entry["sg_retime_start_frame"] = "\n".join(data["retime_start_frame"]) if isinstance(data["retime_start_frame"], list) else data["retime_start_frame"]
            version_entry["sg_timecode_in"] = str(data["timecode_in"])
            version_entry["sg_timecode_out"] = str(data["timecode_out"])
            version_entry["sg_just_in"] = str(data["just_in"])
            version_entry["sg_just_out"] = str(data["just_out"])
            version_entry["sg_framerate"] = data["framerate"]
            version_entry["sg_date"] = "\n".join(data["date"]) if isinstance(data["date"], list) else data["date"]
            version_entry["sg_clip_tag"] = "\n".join(data["clip_tag"]) if isinstance(data["clip_tag"], list) else data["clip_tag"]

            output_path = os.path.dirname(data['scan_path'])
            colorspace = self.colorspace
            
            uploaded_movie_path = (f"{output_path}/"
                                   "mov/"
                                   f"{data['shot_name']}_"
                                   f"{colorspace}_"
                                   f"{data['type']}_v"
                                   f"{int(data['version']):03d}"
                                   ".mov"
                                   )
            
            edited_movie_path = (f"{output_path}/"
                                 f"{data['shot_name']}_"
                                 f"{data['type']}_v"
                                 f"{int(data['version']):03d}"
                                 ".mov"
                                 )
            
            dpx_frames_path = (f"{output_path}/"
                               "dpx/"
                               f"{data['shot_name']}_"
                               f"{colorspace}_"
                               f"{data['type']}_v"
                               f"{int(data['version']):03d}"
                               "_%04d.dpx"
                               )
            
            version_entry["code"] = os.path.splitext(
                os.path.basename(
                    uploaded_movie_path
                    )
                )[0]
            version_entry["sg_path_to_frames"] = dpx_frames_path
            version_entry["sg_path_to_movie"] = edited_movie_path
            
            version_data[row] = version_entry
        
        for row, data in version_data.items():
            output_path = (
                os.path.dirname(self.data[row]["scan_path"])
                )
            
            uploaded_movie_name = (
                f"{self.data[row]['shot_name']}_"
                f"{colorspace}_"
                f"{self.data[row]['type']}_v"
                f"{int(self.data[row]['version']):03d}"
                ".mov"
                )
            
            uploaded_movie = f"{output_path}/{uploaded_movie_name}"
            
            if not os.path.exists(uploaded_movie):
                logger.error(f"MOV not found: {uploaded_movie}")
                continue
            
            version = self._sg.create("Version", data)
            logger.debug(f"Version created: {version}")
            
            self._sg.upload(
                "Version",
                version["id"],
                uploaded_movie,
                "sg_uploaded_movie"
                )
            logger.debug(f"Uploaded movie: {uploaded_movie}")
