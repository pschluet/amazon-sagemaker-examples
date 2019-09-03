import json
import uuid
import boto3

class DeploymentClient:
    def __init__(self):
        self.sm_client = boto3.client('sagemaker')
    
    def create_model(self, training_job_name, execution_role_arn):
        if self._model_exists(training_job_name):
            print('Model already exists for training job {}'.format(training_job_name))
            return None
        else:
            training_job_info = self.sm_client.describe_training_job(TrainingJobName=training_job_name)
            primary_container = {
                'Image': training_job_info['AlgorithmSpecification']['TrainingImage'],
                'ModelDataUrl': training_job_info['ModelArtifacts']['S3ModelArtifacts']
            }
            response = self.sm_client.create_model(
                ModelName = training_job_name,
                ExecutionRoleArn = execution_role_arn,
                PrimaryContainer = primary_container
            )
            print('Created model: {}'.format(response['ModelArn']))
            return response

    def create_endpoint_config(self, training_job_name, instance_type):
        endpoint_config_name = self._generate_endpoint_config_name(training_job_name)
        response = self.sm_client.create_endpoint_config(
            EndpointConfigName = endpoint_config_name,
            ProductionVariants=[{
                'InstanceType':instance_type,
                'InitialVariantWeight':1,
                'InitialInstanceCount':1,
                'ModelName':training_job_name,
                'VariantName':'AllTraffic'}]
        )
        print('Created endpoint config: {}'.format(response['EndpointConfigArn']))
        return (response, endpoint_config_name)

    def _endpoint_exists(self, endpoint_name):
        return bool(self.sm_client.list_endpoints(NameContains=endpoint_name).get('Endpoints', None))

    def _model_exists(self, model_name):
        return bool(self.sm_client.list_models(NameContains=model_name).get('Models', None))

    def _generate_endpoint_config_name(self, training_job_name):
        return '{}-{}'.format(training_job_name, uuid.uuid4().hex[:7])

    def create_endpoint(self, endpoint_name, endpoint_config_name):
        
        if self._endpoint_exists(endpoint_name):
            # update
            endpoint_response = self.sm_client.update_endpoint(
                EndpointName=endpoint_name,
                EndpointConfigName=endpoint_config_name
            )
            print('Updated endpoint: {}'.format(endpoint_response['EndpointArn']))
        else:
            # create
            endpoint_response = self.sm_client.create_endpoint(
                EndpointName=endpoint_name,
                EndpointConfigName=endpoint_config_name
            )
            print('Created endpoint: {}'.format(endpoint_response['EndpointArn']))
        return endpoint_response

def main():
    client = DeploymentClient()
    config = json.load(open('sagemaker_deployment_config.json'))

    create_model_response = client.create_model(
        training_job_name=config['TrainingJobName'],
        execution_role_arn=config['ExecutionRoleArn']
    )

    create_endpoint_config_response, endpoint_config_name = client.create_endpoint_config(
        training_job_name=config['TrainingJobName'],
        instance_type=config['InstanceType']
    )

    create_endpoint_response = client.create_endpoint(
        endpoint_name=config['EndpointName'],
        endpoint_config_name=endpoint_config_name
    )


if __name__=='__main__':
    main()