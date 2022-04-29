# Robo-AI - NLU Service Python SDK

This package offers a bundle of classes and methods that allow to interact easily with a running NLU Service API.

### Basic Usage:

To access the SDK code you must first import the package by adding the following line of code:

```python
from robo_sdk import RoboNLU 
```

You need first to instantiate and configure an object that holds the url to the base endpoint odf the API that will serve this SDK, and also the username and password to authenticate and grant access to it:

```python
client = RoboNLU(base_endpoint="http://127.0.0.1:8000", username="user", password="password")
```

after this, you can get a model object that will allow to reach the several API endpoints, by

```python
model = client.model()
```

The instantiation above implies that you want to create a new nlu model instance. If a model instance already exists and you need to access it, you simply pass the model UUID, as an argument to the previous method:

```python
model=client.model('ad6602c0-96e1-4eb6-a953-196ed7cb10e7')
``` 

The model object will then have all the methods needed to access the API, in a one-to-one relationship:

* create
* train
* status
* predict
* delete

Additionally the model object has a property *get_model*, which allow to retrieve and/or confirm the current model UUID. All of this methods are documented by docstrings, which offer aid by calling the native help info on the method, e.g.:

```python
model.create?
``` 

### Workflow example of endpoints usage:

Once a model object is available, if a no uuid was provided, you can create a model within the API, by:

```python
model.create(language='en')
``` 

and then train and deploy a model by:

```python
model.train(json_data)
``` 
where json_data is a dictionary formatted as the example below:

```json
{
    "nlu": [
        {"intent": "Greeting", "examples": ["Hi","Hello","Howdy","Bonjour","Ça va bien?"]},
        {"intent": "Bye", "examples": ["Good bye","Bye bye", "Au revoir","C U"]},
        {"lookup": "Language", "examples":["PT","ENG"]},
        {"regex": "door_number", "examples":["(\W|^)po[#\-]{0,1}\s{0,1}\d{2}[\s-]{0,1}\d{4}(\W|$)"]}

        ]
}
```

or a string reference to a yaml filepath in nlu.yaml Rasa3 format.

> **NOTE:** The train method also permits to change optional endpoint parameters, allowing for model evaluation, or to change the Entity Recognition fuzzy matching parameters. The optional arguments and respective defaults are:
>
>    - model_eval: bool = False
>    - max_allowed_error_number: int = 3;
>    - min_word_length: int = 3.
>
>For more info please read the API swagger documentation, or access the method's docstring.

To confirm the model is ready and in serving condition, you can access the status endpoint by:


```python
model.status()
```

to which, upon receiving a READY status, the predict method allows to call upon the model for intent and entities predictions:

```python
model.predict({"text": "Hello world!"})
```

If something goes terribly wrong, you can delete a model instance within the API by calling the delete method:

```python
model.delete()
```

> **NOTE:** In all of the above methods they return a enriched object based on pydantic's BaseModel, which allows for ease of parsing the returned data. [Here](https://pydantic-docs.helpmanual.io/usage/models/#model-properties) you can find more information on pydantic models. 

For more examples, please check the [example notebook](https://github.com/robo-ai/roboai-python-sdk/tree/robo_nlu/robo_sdk/robo_nlu/docs/usage_example/NLU_SDK_usage_example.ipynb).
