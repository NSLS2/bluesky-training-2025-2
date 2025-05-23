# Prefect

**Presenter**: Abby Giles

**Materials**:

- [Slides](https://brookhavenlab-my.sharepoint.com/:p:/g/personal/agiles_bnl_gov/EVkVBRSUZ8JFj6FGgpuS_ykB90FDfuuUKlPAWZ-FgG0PrA?e=qJFRvs)

## Setup

1. Log into VDI and open a terminal.

2. Activate a collection environment:
```
conda activate 2025-2.1-py310-tiled
```

3. Change to the `bluesky-training-2025-2` git directory:
```
cd <path to your fork>/bluesky-training-2025-2
```

4. Pull the upstream changes by syncing your fork on GitHub or by fetching upstream and merging.
Documentation on how to do this is located [here](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/syncing-a-fork).

5. Change to the `Week7` directory
```
cd Week7
```

Optional: Open the repo in VSCode
```
# from the directory you want to open in VSCode
code .
```

## Converting Python Workflows to Prefect

We will be converting `my_export.py` from a set of Python functions to a Prefect flow.

There are two decorators we will use: the `@flow` decorator to identify the primary function
for the flow, and the `@task` decorator to identify the helper functions for the flow.

Taking this simple example:
```python
def my_helper_function():
    ...

def my_pipeline_function():
    print("This should appear in the logs")
    my_helper_function()
    ...
```

We can convert it to Prefect by making the following changes:
```python
from prefect import flow, task

@task
def my_helper_function():
    ...

@flow(log_prints=True)
def my_pipeline_function():
    print("This should appear in the logs")
    my_helper_function()
    ...
```

We will walk through converting `my_export.py` together.

## Running flows locally in IPython

In your terminal, start up IPython and run the following:
`%run -i my_export.py`

This will run `my_export.py` in an interactive mode, so global variables (e.g. `simple_local_server`,
`tiled_client`, etc.) and all the functions defined in this file are available.

Next let's run the export function, passing in a reference to a Tiled entry (e.g. `scan_id`, `uid`, index):
```python
export(ref=-2)
```

We should see Prefect logs that look something like this:
```
09:42:00.683 | INFO    | prefect.engine - Created flow run 'devious-catfish' for flow 'export'
09:42:01.050 | INFO    | Flow run 'devious-catfish' - Created task run 'get_weather-0' for task 'get_weather'
09:42:01.052 | INFO    | Flow run 'devious-catfish' - Executing 'get_weather-0' immediately...
09:42:01.373 | INFO    | Task run 'get_weather-0' - Getting weather for date 2025-05-20
09:42:02.023 | INFO    | Task run 'get_weather-0' - Finished in state Completed()
...
```

If you make any changes to the code and want to re-run the file, you **must** close the local tiled
server first by running `simple_local_server.close()`.
This is something you only need to worry about with the `SimpleTiledServer` that we are using
in this example.

## Subflows in Prefect

The `end-of-run-workflow` works by running other flow functions as subflows.
The equivalent flow for this training is in the `full_workflow.py` file.

In the `my_workflow` function, we call `fun_fact` and `export`: the `fun_fact` flow returns a fact about cats, and the `export` flow is what we worked on before.

When we run `my_workflow`, we can see in the Prefect logs that subflows are created with different names:
```
09:58:23.384 | INFO    | prefect.engine - Created flow run 'benevolent-hawk' for flow 'my-workflow'
09:58:23.737 | INFO    | Flow run 'benevolent-hawk' - Getting fun fact...
09:58:24.045 | INFO    | Flow run 'benevolent-hawk' - Created subflow run 'active-eel' for flow 'fun-fact'
09:58:24.272 | INFO    | Flow run 'active-eel' - Want to hear a fun fact about cats?
09:58:24.361 | INFO    | Flow run 'active-eel' - Created task run 'get_cat_fact-0' for task 'get_cat_fact'
09:58:24.362 | INFO    | Flow run 'active-eel' - Executing 'get_cat_fact-0' immediately...
09:58:24.809 | INFO    | Task run 'get_cat_fact-0' - Finished in state Completed()
09:58:24.821 | INFO    | Flow run 'active-eel' - A cats field of vision is about 185 degrees.
09:58:24.821 | INFO    | Flow run 'active-eel' - Isn't that neat?
09:58:24.920 | INFO    | Flow run 'active-eel' - Finished in state Completed('All states completed.')
```
