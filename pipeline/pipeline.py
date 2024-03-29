import os
import kfp.dsl as dsl
import kfp.compiler as compiler
from kubernetes import client as k8s_client

os.environ['VERSION'] = os.environ.get('VERSION', '0.0.33')

IMAGE_BASE_NAME = "/".join([os.environ['DOCKER_REGISTRY'], os.environ['DOCKER_REGISTRY_ORG']])
VERSION = os.environ['VERSION']


def image(step_name):
    return "{}/{}:{}".format(IMAGE_BASE_NAME, step_name, VERSION)


def preprocess_op(raw_data_location, prepared_data_location):
    return dsl.ContainerOp(
        name='data-transformations',
        image=image('preprocess'),
        command=['python'],
        arguments=[
            '/app/preprocess.py',
            '--raw-data-location', raw_data_location,
            '--prepared-data-location', prepared_data_location
        ]
    )


def data_versioning_op(prepared_data_location, data_repository):
    return dsl.ContainerOp(
        name='data-versioning',
        image=image('data-versioning'),
        command=['python'],
        arguments=[
            '/app/data_versioning.py',
            '--prepared-data-location', prepared_data_location,
            '--data-repository', data_repository,
        ]
    )


def upload_model_op(model_repository):
    return dsl.ContainerOp(
        name='upload-model',
        image=image('upload-model'),
        command=['python'],
        arguments=[
            '/app/upload_model.py',
            '--model-repository', model_repository
        ]
    )


def analysis_op(prepared_data_location):
    return dsl.ContainerOp(
        name='analysis',
        image=image('analysis'),
        command=['python'],
        arguments=[
            '/app/analysis.py',
            '--prepared-data-location', prepared_data_location
        ]
    )


def train_op(prepared_data_location, model_repo_location):
    return dsl.ContainerOp(
        name='train',
        image=image('training'),
        command=['python'],
        arguments=[
            '/app/train.py',
            '--prepared-data-location', prepared_data_location,
            '--model-repo-location', model_repo_location
        ]
    )


def evaluate_op(prepared_data_location, model_repo_location):
    return dsl.ContainerOp(
        name='evaluate',
        image=image('evaluate'),
        command=['python'],
        arguments=[
            '/app/evaluate.py',
            '--prepared-data-location', prepared_data_location,
            '--model-repo-location', model_repo_location
        ]
    )


@dsl.pipeline(
    name='Telecom Customer Churn Prediction',
    description='Customer attrition, also known as customer churn, customer turnover, or customer defection, is the loss of clients or customers.'
)
def pipeline(
        raw_data_location="s3://manticore-data/churn/raw",
        prepared_data_location="s3://manticore-data/churn/prepared",
        model_repo_location="s3://manticore-model-repository/churn",
        data_repository='product-recommendation',
        model_repository='product-recommendation'
):
    steps = {}

    steps['preprocess'] = preprocess_op(
        raw_data_location=raw_data_location,
        prepared_data_location=prepared_data_location
    )

    steps['data-versioning'] = data_versioning_op(
        prepared_data_location=prepared_data_location,
        data_repository=data_repository
    )

    steps['upload-model'] = upload_model_op(
        model_repository=model_repository
    )

    steps['analysis'] = analysis_op(
        prepared_data_location=prepared_data_location
    )

    steps['train'] = train_op(
        prepared_data_location=prepared_data_location,
        model_repo_location=model_repo_location
    )

    steps['evaluate'] = evaluate_op(
        prepared_data_location=prepared_data_location,
        model_repo_location=model_repo_location
    )

    steps['data-versioning'].after(steps['preprocess'])
    steps['train'].after(steps['preprocess'])
    steps['analysis'].after(steps['preprocess'])
    steps['evaluate'].after(steps['train'])
    steps['upload-model'].after(steps['evaluate'])


if __name__ == '__main__':
    compiler.Compiler().compile(pipeline, 'pipeline' + '.tar.gz')
