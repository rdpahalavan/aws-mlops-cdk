#!/usr/bin/env python3

import aws_cdk as cdk

from mlops_project.mlops_project_stack import MLOpsProjectStack


app = cdk.App()
MLOpsProjectStack(app, "MLOpsProjectStack")

app.synth()
