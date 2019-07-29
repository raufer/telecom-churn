import os
import kfp

project = os.environ['ORG'] + '-' + os.environ['APP_NAME']
version = os.environ['VERSION']

client = kfp.Client(host='127.0.0.1:8080/pipeline')


def pipeline_parameters(client, pipeline_id):
    """
    Returns the default arguments of for a given `pipeline_id`
    e.g. [{'name': 'key', 'value': 'val'}]
    """
    pipeline = client.pipelines.get_pipeline(pipeline_id)
    return pipeline.parameters


def create_scheduled_job(client, name, description, pipeline_id, experiment_id, period):
    """
    Creates a recurring run of a kubeflow pipeline.
    Associates the run with `experiment`.

    `period` should be given in second
    e.g. 1 week -> 604800
    """
    body = {
       "description": description,
       "name": name,
       "pipeline_spec": {
          "parameters": pipeline_parameters(client, pipeline_id),
          "pipeline_id": pipeline_id
       },
       "resource_references": [
          {
             "key":{
                "id": experiment_id,
                "type": "EXPERIMENT"
             },
             "relationship": "OWNER"
          }
       ],
       "enabled": True,
       "max_concurrency": "10",
       "trigger":{
          "periodic_schedule": {
             "interval_second": str(period)
          }
       }
    }

    response = client.jobs.create_job(body)
    return response

pipelines = client.pipelines.list_pipelines()
ids = {p.name: p.id for p in pipelines.pipelines}
project_pipeline_id = ids.get(project)

if project_pipeline_id:
    print("Pipeline '{} ({})' already exists. Deleting".format(project, project_pipeline_id))
    client.pipelines.delete_pipeline(project_pipeline_id, async_req=True)

body = {
    'name': "{}-v{}".format(project, version),
    'description': 'Manticore Experiment'
}
response = client.experiments.create_experiment(body)
experiment_id = response.id
print("Experiment ID: '{}'".format(experiment_id))

response = client.upload_pipeline('pipeline.tar.gz', project)
pipeline_id = response.id
print("Pipeline ID: '{}'".format(pipeline_id))

job = create_scheduled_job(
    client=client,
    name="retraining-job",
    description="Retraining job to mitigate model performance degradation",
    pipeline_id=pipeline_id,
    experiment_id=experiment_id,
    period=604800
)
print("Recurring Job ID: '{}'".format(job.id))

response = client.run_pipeline(
    experiment_id=experiment_id,
    job_name="{}-job-run".format(project),
    pipeline_id=pipeline_id,
    params={},
    pipeline_package_path=None,
)
run_id = response.id
print("Run ID: '{}'".format(pipeline_id))

response = client.wait_for_run_completion(run_id, timeout=1000)
status = response.run.status
print("Job run completed. Status: '{}'".format(status))

if status == 'Failed':
    raise ValueError

