# Copyright (c) 2024 Yellow Technologies Inc. All rights reserved.
import os
import logging

from yellow.client.advanced.auth import YellowAuthenticator
from yellow.client.advanced.sculpt import YellowSculpt


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
    
# fetch the asset
zip_path = sculpt.fetch_asset(uuid, "demo_output")

# show the asset
sculpt.show_asset(zip_path)