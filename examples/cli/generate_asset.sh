# Copyright (c) 2024 Yellow Technologies Inc. All rights reserved.

# authorize using username and password 
# USERNAME="<username>"
# PASSWORD="<password>"

# auth_token=$(yellow-cli auth --username $USERNAME --password $PASSWORD)
# export YELLOW_TOKEN=$auth_token

# or authorize by providing token directly as an env variable
# export YELLOW_TOKEN=<token>

echo "Your Yellow Token: $YELLOW_TOKEN"

# ------ GENERATE ASSET -------
# sumbit a new generation request
# use your prompt
PROMPT="a muscular young man"
# define gender 'male' or 'female', or use 'neutral' category
GENDER="male"

generation_status=$(yellow-cli sculpt create --prompt "$PROMPT" --gender "$GENDER")
uuid=$(echo "$generation_status" | jq -r '.uuid')
echo "UUID of a submitted job: $uuid"

# ------ CHECK GENERATION JOB STATUS -------
generation_status=$(yellow-cli sculpt status "$uuid")
echo "$generation_status"
