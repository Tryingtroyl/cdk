import aws_cdk as cdk # Import aws_cdk package which contains all the constructs
import aws_cdk.aws_s3 as s3 # Import a specific S3 construct for ease
            
# A class representing a single stack which inherits from the stack construct
class HelloCdkStack(cdk.Stack): 

    """
    A Python Constructor

    Every Construct takes 3 arguments, a scope, a logical construct ID and
    a trailing list of construct arguments (such as Bucket name, versioning, etc.)
    Here, the constructor takes self, the scope which is this particular app, a 
    logical id of type str which will be defined later, and zero or more parameters
    describing the construct.
    """
    def __init__(self, scope: cdk.App, construct_id: str, **kwargs) -> None:

        # A function call executing the base class Constructor of the Construct
        # and providing the three arguments mentioned above.
        super().__init__(scope, construct_id, **kwargs)
        
        """
        This is how we deploy resources.

        self -> The scope of the Construct, i.e. this particular Stack construct
        "MyFirstBucket" -> The logical id of the construct i.e. the bucket
        versioned=True -> An argument describing the construct
        """
        bucket = s3.Bucket(self, "MyFirstBucket", versioned=True)

class AnotherOne(cdk.Stack): 

    def __init__(self, scope: cdk.App, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket(self, "MySecondBucket", versioned=True)