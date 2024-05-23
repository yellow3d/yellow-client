# Copyright (c) 2024 Yellow Technologies Inc. All rights reserved.

# We recommend to use conda to create an isolated environemt
conda create -n yellow-client python=3.12
conda activate yellow-client

# install latest version of yellow-client from GitHub repository
git clone https://github.com/yellow3d/yellow-client.git
cd yellow-client
pip install .
