# yellow-api-client
A client library for accessing Yellow Python API.

## [DEPRECATED]

### Notice of Deprecation

This project is no longer maintained as of July 2024. It may no longer work with newer versions of the Yellow API, and no further updates or fixes will be provided.

## Modules:

### YellowSculpt

#### Overview

Our text-to-3D character generation model is designed to generate naked human meshes in an A-pose. We support the generating of realistic adult males and females based on a given short textual description.

Currently, only the human mesh is generated - anything else will not be reflected in the output (e.g., clothes, swords, etc.).

Limitations and specification:
- Generating can take up to ~5 minutes.
- You need to specify if you are expecting female or male.
- The maximum length of the input prompt is 300 characters.

#### Best Practices

DOs:
- Describe body proportions and anatomy (be as specific as you like, limit is ~300 characters)
- Describe facial features
- Use famous people as reference
- Describe hair or hats
- Describe also non-anatomical features, like the context, history, and characterization of the character and its environment
- Describe style
- Describe fantasy figures that have human-like anatomy (e.g., orcs, trolls, vampires, elves, etc.)

DON’Ts:
- Describe multiple objects
- Describe non-humanoid figures
- Describe specific poses or facial expressions
- Describe clothes and accessories
- Describe fantasy figures that have non-human anatomical features (e.g., mermaids, fairies, centaurs, cyclopes, etc.)
- Exceed 300 characters

### YellowRetopo (experimental)

...

## Installation

Install using `pip`:
```python
pip install git+https://github.com/yellow3d/yellow-client.git
```

To visualize meshes using `trimesh`, install `yellow-client` with additional dependencies:
```python
pip install "yellow-client[vis] @ git+https://github.com/yellow3d/yellow-client.git"
```

## Accessing Yellow GenAI using high-level wrappers

### Authentication

Authenticate using username and password:
```python
from yellow.client.advanced.auth import YellowAuthenticator

USERNAME="<username>"
PASSWORD="<password>"
auth = YellowAuthenticator.auth_with_account(username=USERNAME, password=PASSWORD)
```

or authenticate using token:
```python
from yellow.client.advanced.auth import YellowAuthenticator
TOKEN = "<token>"
auth = YellowAuthenticator.auth_with_token(token=TOKEN)
```

or authentiacate using token stored under OS env variable YELLOW_TOKEN:
```bash
# BASH
export YELLOW_TOKEN="<token>"
```
```python
# Python
os.environ["YELLOW_TOKEN"] = "<token>"
```

then:
```python
from yellow.client.advanced.auth import YellowAuthenticator
auth = YellowAuthenticator()
```

### Access the historical list of prompts and generations
```python
from yellow.client.advanced.sculpt import YellowSculpt

sculpt = YellowSculpt(auth=auth)
sculpt.print_assets_list()
```

### Submit a new asset generation job
```python
from yellow.client.advanced.sculpt import YellowSculpt

sculpt = YellowSculpt(auth=auth)

# example 
prompt = "a muscular young man"
gender = 'male' # or female, neutral
uuid = sculpt.generate_asset(prompt, gender)

sculpt.track_asset_generation(uuid)

zip_path = sculpt.fetch_asset(uuid, "demo_output")
sculpt.show_asset(zip_path)
```

### Fetch a generated asset

```python
from yellow.client.advanced.sculpt import YellowSculpt

sculpt = YellowSculpt(auth=auth)

uuid = "<uuid>"

zip_path = sculpt.fetch_asset(uuid, "demo_output")
sculpt.show_asset(zip_path)
```

## Accessing Yellow GenAI using primitive methods 

### Usage
First, create a client:

```python
from yellow.client import Client

client = Client(base_url="https://yellow3d.com")
```

If the endpoints you are going to hit require authentication, use `AuthenticatedClient` instead:

```python
from yellow.client import AuthenticatedClient

client = AuthenticatedClient(base_url="https://yellow3d.com", token="<token>")
```

Call your endpoint and use your models:

```python
from yellow.client.api.sculpt import sculpt_characters_list
from yellow.client.models import CharacterGeneration
from yellow.client.types import Response

with client as client:
    my_data: List["CharacterGeneration"] = sculpt_characters_list.sync(client=client)
    # or if you need more info (e.g. status_code)
    response: Response = sculpt_characters_list.sync_detailed(client=client)
```

Or do the same thing with an async version:

```python
from yellow.client.api.sculpt import sculpt_characters_list
from yellow.client.models import CharacterGeneration
from yellow.client.types import Response

with client as client:
    my_data: List["CharacterGeneration"] = await sculpt_characters_list.asyncio(client=client)
    response: Response = await sculpt_characters_list.asyncio_detailed(client=client)
```

By default, when you're calling an HTTPS API, it will attempt to verify that SSL is working correctly. Using certificate verification is highly recommended most of the time; however,  you may need to authenticate to a server (especially an internal server) using a custom certificate bundle.

```python
client = AuthenticatedClient(
    base_url="https://internal_api.example.com", 
    token="SuperSecretToken",
    verify_ssl="/path/to/certificate_bundle.pem",
)
```

You can also disable certificate validation altogether, but beware that **this is a security risk**.

```python
client = AuthenticatedClient(
    base_url="https://internal_api.example.com", 
    token="SuperSecretToken", 
    verify_ssl=False
)
```

Things to know:
1. Every path/method combo becomes a Python module with four functions:
    1. `sync`: Blocking request that returns parsed data (if successful) or `None`.
    1. `sync_detailed`: Blocking request that always returns a `Request`, optionally with `parsed` set if the request was successful.
    1. `asyncio`: Like `sync` but async instead of blocking.
    1. `asyncio_detailed`: Like `sync_detailed` but async instead of blocking.

1. All path/query parameters and bodies become method arguments.
1. If your endpoint had any tags on it, the first tag will be used as a module name for the function (my_tag above).
1. Any endpoint which did not have a tag will be in `yellow.client.api.default`.

### Advanced customizations

There are more settings on the generated `Client` class which let you control runtime behavior (refer to the docstring on that class for more information). You can also customize the underlying `httpx.Client` or `httpx.AsyncClient` (depending on your use case):

```python
from yellow.client import Client

def log_request(request):
    print(f"Request event hook: {request.method} {request.url} - Waiting for response")

def log_response(response):
    request = response.request
    print(f"Response event hook: {request.method} {request.url} - Status {response.status_code}")

client = Client(
    base_url="https://api.example.com",
    httpx_args={"event_hooks": {"request": [log_request], "response": [log_response]}},
)

# Or get the underlying httpx client to modify directly with client.get_httpx_client()
# or client.get_async_httpx_client()
```

You can even set the `httpx` client directly; however, beware that this will override any existing settings (e.g. base_url):

```python
import httpx
from yellow.client import Client

client = Client(
    base_url="https://api.example.com",
)
# Note that base_url needs to be reset, as any shared cookies, headers, etc.
client.set_httpx_client(httpx.Client(base_url="https://api.example.com", proxies="http://localhost:8030"))
```

### Building / publishing this package
This project uses [Hatch](https://hatch.pypa.io/) to manage dependencies and packaging. Here are the basics if you want to install this client into another project without publishing it (e.g. for development):
1. Build a wheel with `hatch build`
2. Install that wheel from the other project `pip install <path-to-wheel>`
