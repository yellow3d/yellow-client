# Copyright (c) 2024 Yellow Technologies Inc. All rights reserved.
# authorize using username and password 
# USERNAME="<username>"
# PASSWORD="<password>"

# auth_token=$(yellow-cli auth --username $USERNAME --password $PASSWORD)
# export YELLOW_TOKEN=$auth_token

# or authorize by providing token directly as an env variable
# export YELLOW_TOKEN=<token>

echo "Yellow API Token: $YELLOW_TOKEN"

# ------ LISTING ASSETS -------
assets_list=$(yellow-cli sculpt list)

echo "Listing assets assigned to your account:"
# Parse JSON array and iterate over assets
echo "$assets_list" | jq -c '.[]' | while read -r asset; do
    echo "$asset"
    # if you want parsed json, you can use
    # echo "$asset" | python -m json.tool
done
