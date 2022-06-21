#!/usr/bin/env python3
import os

import aws_cdk as cdk
from cdk.cdk_stack import Ec2InstanceStack

# Starts the Python CDK Application
app = cdk.App()

"""
The described stack. Notice that this creates an object of
the class with the values
app -> The scope
"HelloStack" -> Logical ID of the Stack
env -> A describing variable which creates a CDK environment
with the account number that is already configured in the
AWS CLI and the region.
"""
Ec2InstanceStack(app, "HelloStack", env=cdk.Environment(account='566066428641',region='ap-south-1'),)

# Synthesises the app
app.synth()
