# Copyright (c) 2024 Yellow Technologies Inc. All rights reserved.
import os
import logging

from yellow.client.advanced.auth import YellowAuthenticator
from yellow.client.advanced.sculpt import YellowSculpt
from yellow.client.models.file_format_enum import FileFormatEnum
from yellow.client.models.rig_type_enum import RigTypeEnum


# configure logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger('yellow-client').setLevel(logging.INFO)  

# authentiacate using username and password
# USERNAME="<username>"
# PASSWORD="<password>"
# auth = YellowAuthenticator.auth_with_account(username=USERNAME, password=PASSWORD)

# or authentiacate using token
# TOKEN = "<token>"
# auth = YellowAuthenticator.auth_with_token(token=TOKEN)

# or authentiacate using token stored under OS env variable YELLOW_TOKEN
# os.environ["YELLOW_TOKEN"] = "<token>"
auth = YellowAuthenticator()

sculpt = YellowSculpt(auth=auth)

# get a list of assets assigned to the account
assets_list = sculpt.get_assets_list()

if len(assets_list) == 0:
    raise ValueError("Not found asset")

# filter only assets with status "completed"
assets_list = [a for a in assets_list if a["state"] == "completed"]

print("Listing assets:")
for asset in assets_list:
    print(asset)

# get the last asset from the list
uuid = assets_list[-1]["uuid"]
    
# fetch the asset in fbx format
sculpt.fetch_asset(
    uuid=uuid, 
    output_dir="output_to_fbx", 
    file_format=FileFormatEnum.FBX, 
    rig_type=RigTypeEnum.BLENDER_BASIC_HUMAN_METARIG
)


# fetch the asset in obj format
zip_path = sculpt.fetch_asset(
    uuid=uuid, 
    output_dir="output_to_obj", 
    file_format=FileFormatEnum.OBJ, 
    rig_type=RigTypeEnum.NO_RIG
)

# show the asset (only .obj is supported)
sculpt.show_asset(zip_path)
