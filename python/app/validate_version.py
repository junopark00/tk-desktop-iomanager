# -*- coding: utf-8 -*-

"""
This script will parse the checked data.
Then, get the version of 'Version' enitity's 'code' field.
After compare the version, it will return the new version.
If the version is not found, it will return 1.
"""

__author__ = "Juno Park"
__github__ = "https://github.com/junopark00"


class ValidateVersion:
    def __init__(
        self, 
        shotgrid_data: list, 
        checked_data: dict, 
        colorspace: str
        ):
        self._shotgrid_data = shotgrid_data
        self._checked_data = checked_data
        self._selected_colorspace = colorspace
        self._validated_version = None
        
    def validate_version(self) -> dict:
        """
        Parse the sg data and checked data.
        Then, compare the version.
        If the version is not found, return 1.
        
        Returns:
            dict: validated data {'row': version}
        """
        validated_data = {}
        # parse shotgrid data
        exist_version = {}
        for data in self._shotgrid_data:
            version_name = data['code']  # seq001_shot001_sRGB_org_v001
            version_num = int(version_name.split('_')[-1][1:]) # 1
            seq_shot_name = (
                f"{version_name.split('_')[0]}_"
                f"{version_name.split('_')[1]}"
                )
            print("seq_shot_name: ", seq_shot_name)
            colorspace = version_name.split("_")[2] # sRGB
            _type = version_name.split("_")[3]
            
            if seq_shot_name not in exist_version:
                exist_version[seq_shot_name] = {}
            if colorspace not in exist_version[seq_shot_name]:
                exist_version[seq_shot_name][colorspace] = {}
            if _type not in exist_version[seq_shot_name][colorspace]:
                exist_version[seq_shot_name][colorspace][_type] = []
            
            exist_version[seq_shot_name][colorspace][_type].append(version_num)
            print("exist_version: ", exist_version)
            # exist_version = {'seq001_shot001': {'sRGB': {'org': [1, 2, 3]}}}

        # parse checked data
        for row, column in self._checked_data.items():
            seq_shot_name = column["shot_name"]
            colorspace = self._selected_colorspace
            _type = column["type"]
            file_name = f"{seq_shot_name}_{colorspace}_{_type}"
            print("file_name: ", file_name)
            
            # compare the version
            if (seq_shot_name in exist_version and 
                colorspace in exist_version[seq_shot_name] and 
                _type in exist_version[seq_shot_name][colorspace]):
                
                latest_version = max(exist_version[seq_shot_name][colorspace][_type])
                print("latest_version: ", latest_version)
                new_version = latest_version + 1
            else:
                new_version = 1
                
            validated_data[row] = new_version
        
        return validated_data
    
    @property
    def validated_version(self) -> dict:
        if self._validated_version is None:
            self._validated_version = self.validate_version()
        return self._validated_version