import boto3
import time

def lambda_handler(event, context):
    
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    model_data_url = f"s3://{bucket_name}/{object_key}"
    
    # Initialize a SageMaker client
    sagemaker = boto3.client('sagemaker')
    parts = model_data_url.split('/')
    identifier_part = parts[-3]  # This gets the part 'MLOps-Project-1696691123'
    time_name = identifier_part.split('-')[-1]  # This splits on '-' and gets the last part '1696691123'

    # Specify the model name and S3 location of the model artifacts
    model_name = f"MLOps-Project-Model-{time_name}"
    role_arn = "arn:aws:iam::648057559257:role/service-role/AmazonSageMaker-ExecutionRole-20230507T193773"  # replace with your SageMaker role ARN
    
    # Create a model in SageMaker
    create_model_response = sagemaker.create_model(
        ModelName=model_name,
        PrimaryContainer={
            'Image': '763104351884.dkr.ecr.us-east-1.amazonaws.com/huggingface-pytorch-inference:1.13.1-transformers4.26.0-gpu-py39-cu117-ubuntu20.04',  # update the region and versions as necessary
            'ModelDataUrl': model_data_url,
            'Environment': {
                'SAGEMAKER_CONTAINER_LOG_LEVEL': '20',
                'SAGEMAKER_REGION': 'us-east-1',
            }
        },
        ExecutionRoleArn=role_arn
    )
    
    # Specify the endpoint configuration
    endpoint_config_name = f"MLOps-Project-Endpoint-Config-{time_name}"
    create_endpoint_config_response = sagemaker.create_endpoint_config(
        EndpointConfigName=endpoint_config_name,
        ProductionVariants=[
            {
                'VariantName': 'AllTraffic',
                'ModelName': model_name,
                'InitialInstanceCount': 1,
                'InstanceType': 'ml.g4dn.2xlarge',
            }
        ]
    )
    
    # Create the endpoint
    endpoint_name = f"MLOps-Project-Endpoint-{time_name}"
    create_endpoint_response = sagemaker.create_endpoint(
        EndpointName=endpoint_name,
        EndpointConfigName=endpoint_config_name
    )
    
    return {
        'statusCode': 200,
        'endpointArn': create_endpoint_response['EndpointArn']
    }