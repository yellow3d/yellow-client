# Copyright (c) 2024 Yellow Technologies Inc. All rights reserved.

# authorize using username and password 
# USERNAME="<username>"
# PASSWORD="<password>"

# auth_token=$(yellow-cli auth --username $USERNAME --password $PASSWORD)
# export YELLOW_TOKEN=$auth_token

# or authorize by providing token directly as an env variable
# export YELLOW_TOKEN=<token>

echo "Your Yellow Token: $YELLOW_TOKEN"

UUID="<uuid>"

echo "UUID of an asset: $UUID"

# ------ CHECK GENERATION JOB STATUS -------
generation_status=$(yellow-cli sculpt status "$UUID")
state=$(echo "$generation_status" | jq -r '.state')


if [ "$state" = "completed" ]; then
    # ------ FETCH ASSET -------
    echo "Fetching of $UUID"
    yellow-cli sculpt fetch --output ./ $UUID
else
    echo "Generation not completed"
    echo "Status: $generation_status"
fi
