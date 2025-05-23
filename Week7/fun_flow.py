import httpx
from prefect import flow, task


@task
def get_cat_fact():
    """Get a fun cat fact."""
    return httpx.get("https://catfact.ninja/fact").json()["fact"]


@flow(log_prints=True)
def fun_fact():
    print("Want to hear a fun fact about cats?")
    print(get_cat_fact())
    print("Isn't that neat?")
