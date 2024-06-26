# -*- coding: utf-8 -*-

"""
This script generates a converter script for the conversion process.
Then, it will execute the conversion process.
Finally, it will return the list of completed converters.

If you want to modify the generated script, please modify this script.
"""

__author__ = "Juno Park"
__github__ = "https://github.com/junopark00"


import os
import subprocess

from .constants import CODECS, COLORSPACE, NUKE_PATH

class GenerateConverter:
    def __init__(
        self, 
        data: dict,
        mov_to_dpx: bool, 
        apply_retime: bool, 
        colorspace: str,
        codec: str
        ):
        self.data = data
        self.mov_to_dpx = mov_to_dpx
        self.apply_retime = apply_retime
        self.colorspace_key = colorspace
        self.codec = codec
        self.current_dir = os.path.dirname(__file__)
        
    def set_data(self) -> None:
        """
        Set the data for the converter.
        """
        self.codec = CODECS[self.codec]
        self.seq_name = self.data["seq_name"]
        self.shot_name = self.data["shot_name"]
        self.version = self.data["version"]
        self.type = self.data["type"]
        self.scan_path = self.data["scan_path"]
        self.scan_name = self.data["scan_name"]
        self.pad = self.data["pad"]
        self.ext = self.data["ext"]
        self.resolution = self.data["resolution"]
        self.start_frame = int(self.data["start_frame"])
        self.end_frame = int(self.data["end_frame"])
        self.retime_duration = self.data["retime_duration"]
        self.retime_percent = self.data["retime_percent"]
        self.retime_start_frame = self.data["retime_start_frame"]
        self.framerate = self.data["framerate"]
        self.__set_name()
        self.__set_path()
        
        if self.apply_retime:
            self.retime_info = []
            # Check if multiple items selected
            if (isinstance(self.retime_start_frame, list) and
                isinstance(self.retime_duration, list) and
                isinstance(self.retime_percent, list)
            ):
                for start_frame, retime_duration, retime_percent in zip(
                    self.retime_start_frame, 
                    self.retime_duration, 
                    self.retime_percent
                    ):
                    self.retime_info.append(
                        (start_frame, retime_duration, retime_percent)
                        )
            else:
                self.retime_info.append(
                    (
                        self.retime_start_frame, 
                        self.retime_duration, 
                        self.retime_percent
                    )
                )
            
        else:
            self.retime_info = []
        
    def __set_name(self) -> None:
        """
        Set the name of the files.
        """
        self.edit_mov_name = f"{self.shot_name}_{self.type}_v{int(self.version):03d}.mov"
        self.dpx_name = f"{self.shot_name}_{self.colorspace_key}_{self.type}_v{int(self.version):03d}.%04d.dpx"
        self.jpg_name = f"{self.shot_name}_{self.colorspace_key}_{self.type}_v{int(self.version):03d}.%04d.jpg"
        self.colored_mov_name = f"{self.shot_name}_{self.colorspace_key}_{self.type}_v{int(self.version):03d}.mov"
        
    def __set_path(self) -> None:
        """
        Set the path of the files.
        """
        if self.pad == "":
            self.original_path = os.path.join(self.scan_path, self.scan_name)
        else:
            self.original_path = os.path.join(
                self.scan_path, f"{self.scan_name}{self.pad}.{self.ext}"
                )
        self.output_dir = os.path.dirname(self.scan_path)
        self.mov_input_dir = os.path.join(self.output_dir, "mov")
        self.dpx_output_dir = os.path.join(self.output_dir, "dpx")
        self.jpg_output_dir = os.path.join(self.output_dir, "jpg")
        
        self.converted_mov_path = os.path.join(
            self.mov_input_dir, 
            os.path.basename(self.original_path).split(".")[0] + ".mov"
        )
        
        self.edited_mov_path = os.path.join(
            self.output_dir, self.edit_mov_name
        )
        
        self.dpx_output_path = os.path.join(
            self.dpx_output_dir, self.dpx_name
        )
        
        self.jpg_output_path = os.path.join(
            self.jpg_output_dir, self.jpg_name
        )
        
        self.colored_mov_output_path = os.path.join(
            self.output_dir, self.colored_mov_name
        )
        
    def execute(self, converters: list) -> list:
        """
        Execute the conversion process.
        
        Returns:
            list: The list of completed converters.
        """
        # list of processes
        processes = []
        # list of completed converters
        completed_converter = []
        
        for converter in converters:
            cmd = f"{NUKE_PATH} -t {converter}"
            process = subprocess.Popen(cmd, shell=True)
            processes.append((process, converter))
        
        for process, converter in processes:
            try:
                return_code = process.wait()
                # if return code is 0, the process is successfully completed
                if return_code == 0:
                    completed_converter.append(converter)
                else:
                    print(f"Process for {converter} failed with return code {return_code}.")
            except Exception as e:
                print(f"An Error occured during process for {converter}.\n", e)
        
        return completed_converter
        
    def generate(self) -> str:
        """
        Generate the converter script.
        
        Returns:
            str: The path of the generated script.
        """
        if self.mov_to_dpx:
            if self.apply_retime:
                script = f"""# -*- coding: utf-8 -*-
# WHEN YOU WANT TO MODIFY THIS SCRIPT, PLEASE MODIFY "generate_converter.py".

# IF THIS SCRIPT STILL EXISTS, 
# IT IS LIKELY THAT AN ERROR OCCURRED DURING THE CONVERSION PROCESS.

__author__ = "Juno Park"
__github__ = "https://github.com/junopark00"

import os
import sys
import nuke

codec = "{self.codec}"
colorspace_key = "{self.colorspace_key}"
colorspace_value = "{COLORSPACE[self.colorspace_key]}"
retime_info = {self.retime_info}
start_frame = {self.start_frame}
end_frame = {self.end_frame}

original_path = "{self.original_path}"
output_dir = "{self.output_dir}"
mov_input_dir = "{self.mov_input_dir}"
converted_mov_path = "{self.converted_mov_path}"
edited_mov_path = "{self.edited_mov_path}"
dpx_output_dir = "{self.dpx_output_dir}"
dpx_output_path = "{self.dpx_output_path}"
jpg_output_dir = "{self.jpg_output_dir}"
jpg_output_path = "{self.jpg_output_path}"
colored_mov_output_path = "{self.colored_mov_output_path}"

# set_ocio_color_management
ocio_config_path = os.environ["OCIO"]
if not ocio_config_path:
    sys.exit(1)

root = nuke.root()
root["colorManagement"].setValue("OCIO")
root["OCIO_config"].setValue("custom")
root["customOCIOConfigPath"].setValue('')
root["customOCIOConfigPath"].setValue(ocio_config_path)

# check original media type, if it's not mov, convert it to mov
if original_path.lower().endswith(".mov"):
    pass
else:
    read_node = nuke.createNode("Read")
    read_node["file"].setValue(original_path)
    read_node["last"].setValue(end_frame)
    read_node["origlast"].setValue(end_frame)
    
    if not os.path.exists(mov_input_dir):
        os.makedirs(mov_input_dir)
    
    write_node = nuke.createNode("Write")
    write_node["file"].setValue(converted_mov_path)
    write_node["file_type"].setValue("mov")
    write_node["mov64_codec"].setValue(codec)
    nuke.execute(write_node, start_frame, end_frame)
    end_frame = end_frame - start_frame + 1
    start_frame = 1
    
# edit original mov
read_node = nuke.createNode("Read")
read_node["file"].setValue(converted_mov_path)
read_node["last"].setValue(end_frame)
read_node["origlast"].setValue(end_frame)
read_node["colorspace"].setValue(colorspace_key)

write_node = nuke.createNode("Write")
write_node["file"].setValue(edited_mov_path)
write_node["file_type"].setValue("mov")
write_node["mov64_codec"].setValue(codec)
write_node["colorspace"].setValue(colorspace_key)

nuke.execute(write_node, start_frame, end_frame)

# convert original mov to dpx
read_node = nuke.createNode("Read")
read_node["file"].setValue(converted_mov_path)
read_node["last"].setValue(end_frame)
read_node["origlast"].setValue(end_frame)

retime_nodes = []
for retime in retime_info:
    first_frame, retime_duration, retime_percent = retime
    if first_frame == "" or retime_duration == "" or retime_percent == "":
        raise ValueError("Please fill in the retime information.")
    
    last_frame = int(first_frame) + int(retime_duration) - 1
    retime_ratio = int(retime_percent) / 100

    retime_node = nuke.createNode("Retime")
    retime_node.setInput(0, read_node)
    retime_node["input.first_lock"].setValue("enable")
    retime_node["input.last_lock"].setValue("enable")
    retime_node["output.first_lock"].setValue("enable")
    retime_node["input.first"].setValue(int(first_frame))
    retime_node["input.last"].setValue(int(last_frame))
    retime_node["output.first"].setValue(1)
    output_last = (int(last_frame) - int(first_frame)) / retime_ratio + 1
    retime_node["output.last"].setValue(output_last)
    retime_node["speed"].setValue(retime_ratio)
    retime_nodes.append(retime_node)

append_clip_node = nuke.createNode("AppendClip")
for idx, retime_node in enumerate(retime_nodes):
    append_clip_node.setInput(idx, retime_node)
    
ac_first_frame = int(append_clip_node["firstFrame"].value())
ac_last_frame = int(append_clip_node["lastFrame"].value())

if not os.path.exists(dpx_output_dir):
    os.makedirs(dpx_output_dir)

write_node = nuke.createNode("Write")
write_node.setInput(0, append_clip_node)
write_node["file"].setValue(dpx_output_path)
write_node["file_type"].setValue("dpx")
nuke.execute(write_node, ac_first_frame, ac_last_frame)

# convert dpx to colored jpg
read_node = nuke.createNode("Read")
read_node["file"].setValue(dpx_output_path)
read_node["colorspace"].setValue(colorspace_key)
read_node["last"].setValue(ac_last_frame)
read_node["origlast"].setValue(ac_last_frame)

if not os.path.exists(jpg_output_dir):
    os.makedirs(jpg_output_dir)

write_node = nuke.createNode("Write")
write_node["file"].setValue(jpg_output_path)
write_node["file_type"].setValue("jpeg")
write_node["colorspace"].setValue(colorspace_value)
nuke.execute(write_node, ac_first_frame, ac_last_frame)

# convert colored jpg to mov
read_node = nuke.createNode("Read")
read_node["file"].setValue(jpg_output_path)
read_node["last"].setValue(ac_last_frame)
read_node["origlast"].setValue(ac_last_frame)

write_node = nuke.createNode("Write")
write_node["file"].setValue(colored_mov_output_path)
write_node["file_type"].setValue("mov")
write_node["mov64_codec"].setValue(codec)
nuke.execute(write_node, ac_first_frame, ac_last_frame)
                """
                script_path = os.path.join(
                    self.current_dir, 
                    f"converter_mov_to_dpx_retime_{self.shot_name}_v{int(self.version):03d}.py"
                )
                
                with open(script_path, "w") as f:
                    f.write(script)
            else:
                script = f"""# -*- coding: utf-8 -*-
# WHEN YOU WANT TO MODIFY THIS SCRIPT, PLEASE MODIFY "generate_converter.py".

# IF THIS SCRIPT STILL EXISTS, 
# IT IS LIKELY THAT AN ERROR OCCURRED DURING THE CONVERSION PROCESS.

__author__ = "Juno Park"
__github__ = "https://github.com/junopark00"

import os
import sys
import nuke

codec = "{self.codec}"
colorspace_key = "{self.colorspace_key}"
colorspace_value = "{COLORSPACE[self.colorspace_key]}"
start_frame = {self.start_frame}
end_frame = {self.end_frame}

original_path = "{self.original_path}"
output_dir = "{self.output_dir}"
mov_input_dir = "{self.mov_input_dir}"
converted_mov_path = "{self.converted_mov_path}"
edited_mov_path = "{self.edited_mov_path}"
dpx_output_dir = "{self.dpx_output_dir}"
dpx_output_path = "{self.dpx_output_path}"
jpg_output_dir = "{self.jpg_output_dir}"
jpg_output_path = "{self.jpg_output_path}"
colored_mov_output_path = "{self.colored_mov_output_path}"

# set_ocio_color_management
ocio_config_path = os.environ["OCIO"]
if not ocio_config_path:
    sys.exit(1)

root = nuke.root()
root["colorManagement"].setValue("OCIO")
root["OCIO_config"].setValue("custom")
root["customOCIOConfigPath"].setValue('')
root["customOCIOConfigPath"].setValue(ocio_config_path)

# check original media type, if it's not mov, convert it to mov
if original_path.lower().endswith(".mov"):
    pass
else:
    read_node = nuke.createNode("Read")
    read_node["file"].setValue(original_path)
    read_node["first"].setValue(start_frame)
    read_node["origfirst"].setValue(start_frame)
    read_node["last"].setValue(end_frame)
    read_node["origlast"].setValue(end_frame)
    
    if not os.path.exists(mov_input_dir):
        os.makedirs(mov_input_dir)
    
    write_node = nuke.createNode("Write")
    write_node["file"].setValue(converted_mov_path)
    write_node["file_type"].setValue("mov")
    write_node["mov64_codec"].setValue(codec)
    nuke.execute(write_node, start_frame, end_frame)
    end_frame = end_frame - start_frame + 1
    start_frame = 1
    
# edit original mov
read_node = nuke.createNode("Read")
read_node["file"].setValue(converted_mov_path)
read_node["first"].setValue(start_frame)
read_node["origfirst"].setValue(start_frame)
read_node["last"].setValue(end_frame)
read_node["origlast"].setValue(end_frame)
read_node["colorspace"].setValue(colorspace_key)

write_node = nuke.createNode("Write")
write_node["file"].setValue(edited_mov_path)
write_node["file_type"].setValue("mov")
write_node["mov64_codec"].setValue(codec)
write_node["colorspace"].setValue(colorspace_key)

nuke.execute(write_node, start_frame, end_frame)

# convert original mov to dpx
read_node = nuke.createNode("Read")
read_node["file"].setValue(converted_mov_path)
read_node["first"].setValue(start_frame)
read_node["origfirst"].setValue(start_frame)
read_node["last"].setValue(end_frame)
read_node["origlast"].setValue(end_frame)

if not os.path.exists(dpx_output_dir):
    os.makedirs(dpx_output_dir)

write_node = nuke.createNode("Write")
write_node["file"].setValue(dpx_output_path)
write_node["file_type"].setValue("dpx")
nuke.execute(write_node, start_frame, end_frame)
    
# convert dpx to colored jpg
read_node = nuke.createNode("Read")
read_node["file"].setValue(dpx_output_path)
read_node["first"].setValue(start_frame)
read_node["origfirst"].setValue(start_frame)
read_node["last"].setValue(end_frame)
read_node["origlast"].setValue(end_frame)
read_node["colorspace"].setValue(colorspace_key)

if not os.path.exists(jpg_output_dir):
    os.makedirs(jpg_output_dir)

write_node = nuke.createNode("Write")
write_node["file"].setValue(jpg_output_path)
write_node["file_type"].setValue("jpeg")
write_node["colorspace"].setValue(colorspace_value)
nuke.execute(write_node, start_frame, end_frame)

# convert colored jpg to mov
read_node = nuke.createNode("Read")
read_node["file"].setValue(jpg_output_path)
read_node["first"].setValue(start_frame)
read_node["origfirst"].setValue(start_frame)
read_node["last"].setValue(end_frame)
read_node["origlast"].setValue(end_frame)

write_node = nuke.createNode("Write")
write_node["file"].setValue(colored_mov_output_path)
write_node["file_type"].setValue("mov")
write_node["mov64_codec"].setValue(codec)
nuke.execute(write_node, start_frame, end_frame)
                """
                script_path = os.path.join(
                    self.current_dir, 
                    f"converter_mov_to_dpx_{self.shot_name}_v{int(self.version):03d}.py"
                )
                
                with open(script_path, "w") as f:
                    f.write(script)
        else:
            if self.apply_retime:
                script = f"""# -*- coding: utf-8 -*-
# WHEN YOU WANT TO MODIFY THIS SCRIPT, PLEASE MODIFY "generate_converter.py".

# IF THIS SCRIPT STILL EXISTS, 
# IT IS LIKELY THAT AN ERROR OCCURRED DURING THE CONVERSION PROCESS.

__author__ = "Juno Park"
__github__ = "https://github.com/junopark00"

import os
import sys
import nuke

codec = "{self.codec}"
colorspace_key = "{self.colorspace_key}"
colorspace_value = "{COLORSPACE[self.colorspace_key]}"
retime_info = {self.retime_info}
start_frame = {self.start_frame}
end_frame = {self.end_frame}

original_path = "{self.original_path}"
output_dir = "{self.output_dir}"
mov_input_dir = "{self.mov_input_dir}"
converted_mov_path = "{self.converted_mov_path}"
edited_mov_path = "{self.edited_mov_path}"
dpx_output_dir = "{self.dpx_output_dir}"
dpx_output_path = "{self.dpx_output_path}"
jpg_output_dir = "{self.jpg_output_dir}"
jpg_output_path = "{self.jpg_output_path}"
colored_mov_output_path = "{self.colored_mov_output_path}"

# set_ocio_color_management
ocio_config_path = os.environ["OCIO"]
if not ocio_config_path:
    sys.exit(1)

root = nuke.root()
root["colorManagement"].setValue("OCIO")
root["OCIO_config"].setValue("custom")
root["customOCIOConfigPath"].setValue('')
root["customOCIOConfigPath"].setValue(ocio_config_path)

# check original media type, if it's not mov, convert it to mov
if original_path.lower().endswith(".mov"):
    pass
else:
    read_node = nuke.createNode("Read")
    read_node["file"].setValue(original_path)
    read_node["first"].setValue(start_frame)
    read_node["origfirst"].setValue(start_frame)
    read_node["last"].setValue(end_frame)
    read_node["origlast"].setValue(end_frame)
    
    if not os.path.exists(mov_input_dir):
        os.makedirs(mov_input_dir)
    
    write_node = nuke.createNode("Write")
    write_node["file"].setValue(converted_mov_path)
    write_node["file_type"].setValue("mov")
    write_node["mov64_codec"].setValue(codec)
    nuke.execute(write_node, start_frame, end_frame)
    end_frame = end_frame - start_frame + 1
    start_frame = 1
    
# edit original mov
read_node = nuke.createNode("Read")
read_node["file"].setValue(converted_mov_path)
read_node["first"].setValue(start_frame)
read_node["origfirst"].setValue(start_frame)
read_node["last"].setValue(end_frame)
read_node["origlast"].setValue(end_frame)
read_node["colorspace"].setValue(colorspace_key)

retime_nodes = []
for retime in retime_info:
    first_frame, retime_duration, retime_percent = retime
    if first_frame == "" or retime_duration == "" or retime_percent == "":
        raise ValueError("Please fill in the retime information.")
    
    last_frame = int(first_frame) + int(retime_duration) - 1
    retime_ratio = int(retime_percent) / 100
    
    retime_node = nuke.createNode("Retime")
    retime_node.setInput(0, read_node)
    retime_node["input.first_lock"].setValue("enable")
    retime_node["input.last_lock"].setValue("enable")
    retime_node["output.first_lock"].setValue("enable")
    retime_node["input.first"].setValue(int(first_frame))
    retime_node["input.last"].setValue(int(last_frame))
    retime_node["output.first"].setValue(1)
    output_last = (int(last_frame) - int(first_frame)) / retime_ratio + 1
    retime_node["output.last"].setValue(output_last)
    retime_node["speed"].setValue(retime_ratio)
    retime_nodes.append(retime_node)
    
append_clip_node = nuke.createNode("AppendClip")
for idx, retime_node in enumerate(retime_nodes):
    append_clip_node.setInput(idx, retime_node)
    
ac_first_frame = int(append_clip_node["firstFrame"].value())
ac_last_frame = int(append_clip_node["lastFrame"].value())

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

write_node = nuke.createNode("Write")
write_node.setInput(0, append_clip_node)
write_node["file"].setValue(edited_mov_path)
write_node["file_type"].setValue("mov")
write_node["mov64_codec"].setValue(codec)
write_node["colorspace"].setValue(colorspace_key)

nuke.execute(write_node, ac_first_frame, ac_last_frame)

# apply colorspace and export mov
read_node = nuke.createNode("Read")
read_node["file"].setValue(edited_mov_path)
read_node["colorspace"].setValue(colorspace_key)
read_node["first"].setValue(ac_first_frame)
read_node["origfirst"].setValue(ac_first_frame)
read_node["last"].setValue(ac_last_frame)
read_node["origlast"].setValue(ac_last_frame)

write_node = nuke.createNode("Write")
write_node["file"].setValue(colored_mov_output_path)
write_node["file_type"].setValue("mov")
write_node["mov64_codec"].setValue(codec)
write_node["colorspace"].setValue(colorspace_value)

nuke.execute(write_node, ac_first_frame, ac_last_frame)
                """
                script_path = os.path.join(
                    self.current_dir, 
                    f"converter_original_retime_{self.shot_name}_v{int(self.version):03d}.py"
                )
                
                with open(script_path, "w") as f:
                    f.write(script)
            else:
                script = f"""# -*- coding: utf-8 -*-
# WHEN YOU WANT TO MODIFY THIS SCRIPT, PLEASE MODIFY "generate_converter.py".

# IF THIS SCRIPT STILL EXISTS, 
# IT IS LIKELY THAT AN ERROR OCCURRED DURING THE CONVERSION PROCESS.

__author__ = "Juno Park"
__github__ = "https://github.com/junopark00"

import os
import sys
import nuke

codec = "{self.codec}"
colorspace_key = "{self.colorspace_key}"
colorspace_value = "{COLORSPACE[self.colorspace_key]}"
start_frame = {self.start_frame}
end_frame = {self.end_frame}

original_path = "{self.original_path}"
output_dir = "{self.output_dir}"
mov_input_dir = "{self.mov_input_dir}"
converted_mov_path = "{self.converted_mov_path}"
edited_mov_path = "{self.edited_mov_path}"
dpx_output_dir = "{self.dpx_output_dir}"
dpx_output_path = "{self.dpx_output_path}"
jpg_output_dir = "{self.jpg_output_dir}"
jpg_output_path = "{self.jpg_output_path}"
colored_mov_output_path = "{self.colored_mov_output_path}"

# set_ocio_color_management
ocio_config_path = os.environ["OCIO"]
if not ocio_config_path:
    sys.exit(1)

root = nuke.root()
root["colorManagement"].setValue("OCIO")
root["OCIO_config"].setValue("custom")
root["customOCIOConfigPath"].setValue('')
root["customOCIOConfigPath"].setValue(ocio_config_path)

# check original media type, if it's not mov, convert it to mov
if original_path.lower().endswith(".mov"):
    pass
else:
    read_node = nuke.createNode("Read")
    read_node["file"].setValue(original_path)
    read_node["first"].setValue(start_frame)
    read_node["origfirst"].setValue(start_frame)
    read_node["last"].setValue(end_frame)
    read_node["origlast"].setValue(end_frame)
    
    if not os.path.exists(mov_input_dir):
        os.makedirs(mov_input_dir)
    
    write_node = nuke.createNode("Write")
    write_node["file"].setValue(converted_mov_path)
    write_node["file_type"].setValue("mov")
    write_node["mov64_codec"].setValue(codec)
    nuke.execute(write_node, start_frame, end_frame)
    end_frame = end_frame - start_frame + 1
    start_frame = 1
    
# edit original mov
read_node = nuke.createNode("Read")
read_node["file"].setValue(converted_mov_path)
read_node["first"].setValue(start_frame)
read_node["origfirst"].setValue(start_frame)
read_node["last"].setValue(end_frame)
read_node["origlast"].setValue(end_frame)
read_node["colorspace"].setValue(colorspace_key)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

write_node = nuke.createNode("Write")
write_node["file"].setValue(edited_mov_path)
write_node["file_type"].setValue("mov")
write_node["colorspace"].setValue(colorspace_key)
nuke.execute(write_node, start_frame, end_frame)

# apply colorspace and export mov
mov_end = end_frame - start_frame + 1
read_node = nuke.createNode("Read")
read_node["file"].setValue(edited_mov_path)
read_node["colorspace"].setValue(colorspace_key)
read_node["first"].setValue(1)
read_node["origfirst"].setValue(1)
read_node["last"].setValue(mov_end)
read_node["origlast"].setValue(mov_end)

write_node = nuke.createNode("Write")
write_node["file"].setValue(colored_mov_output_path)
write_node["file_type"].setValue("mov")
write_node["mov64_codec"].setValue(codec)
write_node["colorspace"].setValue(colorspace_value)

nuke.execute(write_node, 1, mov_end)
                """
                script_path = os.path.join(
                    self.current_dir, 
                    f"converter_original_{self.shot_name}_v{int(self.version):03d}.py"
                )
                
                with open(script_path, "w") as f:
                    f.write(script)
                    
        return script_path