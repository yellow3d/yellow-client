# Copyright (c) 2024 Yellow Technologies Inc. All rights reserved.
import os
import logging

from yellow.client.advanced.auth import YellowAuthenticator
from yellow.client.advanced.sculpt import YellowSculpt
from yellow.client.models.sculpt_characters_fetch_retrieve_file_format import SculptCharactersFetchRetrieveFileFormat
from yellow.client.models.sculpt_characters_fetch_retrieve_rig_type import SculptCharactersFetchRetrieveRigType
from yellow.client.models.sculpt_characters_list_state_item import SculptCharactersListStateItem


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
assets_list = sculpt.get_latest_k_assets(
    k=10,
    state=[SculptCharactersListStateItem.COMPLETED]
)

if len(assets_list) == 0:
    raise ValueError("Not found asset")

print("Listing assets:")
for asset in assets_list:
    print(asset)

# get the newest asset from the list
uuid = assets_list[0]["uuid"]
    
# fetch the asset in fbx format
sculpt.fetch_asset(
    uuid=uuid, 
    output_dir="output_to_fbx", 
    file_format=SculptCharactersFetchRetrieveFileFormat.FBX,
    rig_type=SculptCharactersFetchRetrieveRigType.BLENDER_BASIC_HUMAN_METARIG
)


# fetch the asset in obj format
zip_path = sculpt.fetch_asset(
    uuid=uuid, 
    output_dir="output_to_obj", 
    file_format=SculptCharactersFetchRetrieveFileFormat.OBJ,
    rig_type=SculptCharactersFetchRetrieveRigType.NO_RIG
)

# show the asset (only .obj is supported)
sculpt.show_asset(zip_path)
