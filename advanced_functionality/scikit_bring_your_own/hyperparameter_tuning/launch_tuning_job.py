import json
from time import gmtime, strftime
import boto3
import os

JOB_NAME_MAX_LENGTH = 32

def generate_job_name():
    # Make sure the training job name doesn't exceed the maximum limit
    user = os.getenv('USER', 'user')
    date_str = strftime("%Y-%m-%dT%H-%M-%S", gmtime())
    return '{}-{}'.format(user[:(JOB_NAME_MAX_LENGTH - len(date_str) - 1)], date_str)

def main():
    smclient = boto3.client('sagemaker')

    tuning_job_name = generate_job_name()
    print('Tuning job name: {}'.format(tuning_job_name))

    # Load job definitons
    tuning_job_config = json.load(open('tuning_job_config.json'))
    training_job_definition = json.load(open('training_job_definition.json'))

    print('Training artifacts will be uploaded to: {}'.format(training_job_definition["OutputDataConfig"]["S3OutputPath"]))

    # Launch hyperparameter tuning job
    smclient.create_hyper_parameter_tuning_job(
        HyperParameterTuningJobName = tuning_job_name,
        HyperParameterTuningJobConfig = tuning_job_config,
        TrainingJobDefinition = training_job_definition
    )

if __name__=='__main__':
    main()