import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk.cdk_stack import HelloCdkStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk/cdk_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = HelloCdkStack(app, "cdk")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::EC2::Instance", {
#         "InstanceType": "t2.micro"
#     })
