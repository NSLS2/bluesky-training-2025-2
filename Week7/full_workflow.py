from prefect import flow

from fun_flow import fun_fact
from my_export import export


@flow(log_prints=True)
def my_workflow(ref):
    print("Getting fun fact...")
    fun_fact()
    print("Now exporting a file...")
    export(ref)
    print("Done!")
