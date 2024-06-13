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

# list assets
sculpt.print_assets_list()
