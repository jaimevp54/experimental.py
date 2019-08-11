# experimental.py

Safe transition into new implementations.

`experimental' is a python package that provides safety measures when implementing changes to a codebase throughout the use of `experiments`.

Within the context of this package, experiments are pieces of functionality which haven't been successfully tested on a production environment.

## Experiments
Experiments are pieces of functionality identified by a tag that can be enabled by simply including them within the `experimental_config.py` file. By default, experiments not included in `experimental_config.py` will raise a `DisabledExperiment` exception.

### Hello World
The simplest expression to define a experiment is by the use of a `experimental_block`:

`experimental_config.py`
```python
ENABLED_EXPERIMENTS = ["feature123"] # Enable all
````

`main.py`
```python
from experimental import experimental_block, DisabledExperiment

try:
    with experimental_block('feature123'):
        print("do stuff")

except DisabledExperiment:                                       
    print("fallback")
```

### @experiment and @volatile

While `experimental_block`s' are usefull when defining new functionalities, they fall behind when updating already existing code. For these cases the `@experiment` and `@volatile` decorators are provided.

`@experiment





Experiments are *not*:
- Feature flags: even thou there is resemblance between these concepts, contrary to feature flags, experiments are expected to be short-lived and to be removed as soon as they are proven to be successful.
