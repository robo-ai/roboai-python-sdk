# ROBO.AI SDK for Python

A Python library for the ROBO.AI API which allows you to manage assistants' runtimes.

## Installation

The latest stable version is available on PyPI. You can install it with pip: 

    pip install robo-ai

## Usage

Initializing a new RoboAI instance:  

```python
from robo_ai.model.config import Config
from robo_ai.robo_ai import RoboAi

base_endpoint = "<BACKEND_URL>"
http_username = "<BASIC_AUTH_USERNAME>"
http_password = "<BASIC_AUTH_PASSWORD>"
config = Config(
    base_endpoint,
    http_auth={
        "username": http_username,
        "password": http_password
    }
)

robo = RoboAi(config)
```

## Available methods

Below we provide instructions on how to use each method.  

**Login** - allows you to authenticate with an API key:
```python
api_key = "<API_KEY>"
robo.oauth.authenticate(api_key)
```

To use the following methods one needs to define some variables like this:
```python
bot_uuid = "<BOT_UUID>"
package_file_path = "<PATH_OF_PACKAGE_FILE_TO_BE_DEPLOYED>"
base_version = "<RUNTIME_BASE_VERSION>"
```

**List assistants** - provides a list of the existing assistants for a given page:  
```python
page = 0
assistants = robo.assistants.get_list(page)

assistants_list = assistants.content
for assistant in assistants_list:
    print(assistant.uuid)
```

**Get assistant** - provides you with information about a specific assistant:  
```python
assistant = robo.assistants.get(bot_uuid)

assistant_content = assistant.content
print(assistant_content.uuid)
print(assistant_content.status)
```

**Create an assistant** - allows you to create an assistant runtime:  
```python
robo.assistants.runtimes.create(bot_uuid, package_file_path, base_version)
```

**Update an assistant** - allows you to update an assistant runtime:  
```python
# Before being updated, the bot runtime needs to be stopped
robo.assistants.runtimes.stop(bot_uuid)

robo.assistants.runtimes.update(bot_uuid, package_file_path, base_version)
```

**Stop an assistant** - allows you to stop an assistant runtime:  
```python
robo.assistants.runtimes.stop(bot_uuid)
```

**Start an assistant** - allows you to start an assistant runtime:  
```python
robo.assistants.runtimes.start(bot_uuid)
```

**Remove an assistant** - allows you to remove an assistant runtime:  
```python
robo.assistants.runtimes.remove(bot_uuid)
```

**Get an assistant runtime** - allows you to fetch information for a specific assistant runtime:  
```python
runtime = robo.assistants.runtimes.get(bot_uuid)

# You can then get info on the assistant's UUID
assistant_uuid = runtime.content.assistantUuid
print(assistant_uuid)
# Or the status
status = runtime.content.status
print(status)
# Or the engine for instance
engine = runtime.content.engine
print(engine)
```

**Get logs for an assistant** - allows you to get logs for a specific assistant runtime:  
```python
logs = robo.assistants.runtimes.get_logs(bot_uuid)
lines = logs.content.lines
print(*lines, sep="\n")
```

## Code Style

We use [Google Style Python Docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings). 