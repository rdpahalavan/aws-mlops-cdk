import boto3
import time

def lambda_handler(event, context):
    # Initialize a SageMaker client
    sagemaker = boto3.client('sagemaker')
    
    time_now = int(time.time())

    # Specify the training job parameters
    training_params = {
        "TrainingJobName": f"MLOps-Project-{time_now}",  # unique training job name
        "AlgorithmSpecification": {
            "TrainingImage": "763104351884.dkr.ecr.us-east-1.amazonaws.com/huggingface-pytorch-training:1.13.1-transformers4.26.0-gpu-py39-cu117-ubuntu20.04",  # update the region and versions as necessary
            "TrainingInputMode": "File"
        },
        "RoleArn": "arn:aws:iam::648057559257:role/service-role/AmazonSageMaker-ExecutionRole-20230507T193773",  # replace with your SageMaker role ARN
        "OutputDataConfig": {
            "S3OutputPath": "s3://mlops-cdk-project-1/MLOps-Project/Models/"
        },
        "ResourceConfig": {
            "InstanceCount": 1,
            "InstanceType": "ml.p3.8xlarge",
            "VolumeSizeInGB": 30
        },
        "InputDataConfig": [
            {
                "ChannelName": "train",
                "DataSource": {
                    "S3DataSource": {
                        "S3DataType": "S3Prefix",
                        "S3Uri": "s3://mlops-cdk-project-1/MLOps-Project/Input/Dataset/train",
                        "S3DataDistributionType": "FullyReplicated"
                    }
                },
                "InputMode": "File",
                "ContentType": "application/x-arrow"
            },
            {
                "ChannelName": "test",
                "DataSource": {
                    "S3DataSource": {
                        "S3DataType": "S3Prefix",
                        "S3Uri": "s3://mlops-cdk-project-1/MLOps-Project/Input/Dataset/test",
                        "S3DataDistributionType": "FullyReplicated"
                    }
                },
                "InputMode": "File",
                "ContentType": "application/x-arrow"
            }
        ],
        "HyperParameters": {
            "sagemaker_container_log_level": "20",
            "sagemaker_job_name": f'"MLOps-Project-{time_now}"',
            "sagemaker_program": '"train.py"',
            "sagemaker_region": '"us-east-1"',
            "sagemaker_submit_directory": '"s3://sagemaker-bucket-store/MLOps-Project/Source/sourcedir.tar.gz"'
        },
        "StoppingCondition": {
            "MaxRuntimeInSeconds": 1000
        }
    }

    # Create the training job
    response = sagemaker.create_training_job(**training_params)
    
    return {
        'statusCode': 200,
        'trainingJobArn': response['TrainingJobArn']
    }