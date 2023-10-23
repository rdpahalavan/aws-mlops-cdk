from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_s3 as s3,
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_events as events,
    aws_events_targets as targets,
    aws_s3_notifications as s3_notifications,
)


class MLOpsProjectStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket(self, 
            'MLOpsBucket',
            bucket_name='mlops-cdk-project-1',
            versioned=True,
        )

        lambda_role = iam.Role.from_role_arn(
            self, 
            'ExistingRole', 
            role_arn='arn:aws:iam::648057559257:role/service-role/MLOpsTrainModel-role-k8zj5kgm'
        )

        lambda_train_function = _lambda.Function(
            self, 'MLOpsCDKModelTrain',
            function_name='MLOpsCDKModelTrain',
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler='train_model.lambda_handler',
            code=_lambda.Code.from_asset('lambda_code'),
            role=lambda_role,
            timeout=Duration.minutes(5),
            memory_size=1024
        )

        bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED_PUT,
            s3_notifications.LambdaDestination(lambda_train_function),
            s3.NotificationKeyFilter(prefix='MLOps-Project/Input/Dataset/train/', suffix='.arrow')
        )

        lambda_deploy_function = _lambda.Function(
            self,
            'MLOpsCDKModelDeploy',
            function_name='MLOpsCDKModelDeploy',
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler='deploy_model.lambda_handler', 
            code=_lambda.Code.from_asset('lambda_code'),
            role=lambda_role,
            timeout=Duration.minutes(5),
            memory_size=1024
        )

        bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3_notifications.LambdaDestination(lambda_deploy_function),
            s3.NotificationKeyFilter(prefix='MLOps-Project/Models/', suffix='model.tar.gz')
        )