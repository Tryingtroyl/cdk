import aws_cdk as core
import aws_cdk.aws_ec2 as ec2
import base64


with open("cdk/data/userdata.sh") as f:
    user_data = f.read()
user_data_bytes=user_data.encode('ascii')
base64_bytes=base64.b64encode(user_data_bytes)
base64_user_data=base64_bytes.decode('ascii')

class Ec2InstanceStack(core.Stack):

    def __init__(self, scope: core.App, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        InstanceType = core.CfnParameter(self, "InstanceType", type="String", default="t2.micro",
        description="The type of the instance.")
        InstanceName = core.CfnParameter(self, "InstanceName", type="String", default="webserver-7",
        description="The name of the instance.")
        AmiId = core.CfnParameter(self, "AmiId", type="String",
        description="The id of the AMI.")
        VpcCidr = core.CfnParameter(self, "VpcCidr", type="String",
        description="The cidr of the VPC.")
        PublicSubCidr = core.CfnParameter(self, "PublicSubCidr", type="String",
        description="The cidr of the public subnet.")
        PrivateSubCidr = core.CfnParameter(self, "PrivateSubCidr", type="String",
        description="The cidr of the private subnet.")
        KeyPair = core.CfnParameter(self, "KeyPair", type="String",
        description="The keypair for the instance")

        self.vpc = ec2.CfnVPC(self, 'CDKVPC',
            cidr_block = VpcCidr.value_as_string,
            enable_dns_hostnames=True,
            enable_dns_support=True
        )

        internet_gateway = ec2.CfnInternetGateway(self,
        "CDKInternetGateway",
        tags=[core.CfnTag(
        key="name",
        value="DemoIGforCDK")]
        )

        gateway_attach = ec2.CfnVPCGatewayAttachment(self,
        "CDKVPCGatewayAttachment",
        vpc_id=self.vpc.attr_vpc_id,
        internet_gateway_id=internet_gateway.attr_internet_gateway_id
        )

        route_table = ec2.CfnRouteTable(self,
        "CDKRouteTable",
        vpc_id=self.vpc.attr_vpc_id
        )

        route = ec2.CfnRoute(self,
        "CDKRoute",
        route_table_id=route_table.attr_route_table_id,
        gateway_id=internet_gateway.attr_internet_gateway_id,
        destination_cidr_block="0.0.0.0/0"
        )
       

        security_group = ec2.CfnSecurityGroup(self, "CDKSecurityGroup",
            group_description="groupDescription",

            security_group_ingress=[ec2.CfnSecurityGroup.IngressProperty(
                ip_protocol="tcp",

                # the properties below are optional
                cidr_ip="0.0.0.0/0",
                from_port=80,
                to_port=80
            ),
            ec2.CfnSecurityGroup.IngressProperty(
                ip_protocol="tcp",

                # the properties below are optional
                cidr_ip="0.0.0.0/0",
                from_port=22,
                to_port=22
            )],
            vpc_id=self.vpc.attr_vpc_id
        )
            
        public_subnet = ec2.CfnSubnet(self,
         "CDKPublicSubnet",
         vpc_id = self.vpc.attr_vpc_id,
         map_public_ip_on_launch=True,
         cidr_block=PublicSubCidr.value_as_string,
         availability_zone='ap-south-1a'
         )

        private_subnet = ec2.CfnSubnet(self,
        "CDKPrivateSubnet",
        vpc_id=self.vpc.attr_vpc_id,
        cidr_block=PrivateSubCidr.value_as_string,
        availability_zone='ap-south-1a'
        )

        public_subnet_route_table_association = ec2.CfnSubnetRouteTableAssociation(self,
        "CDKPublicSubnetRouteTableAssociation",
        route_table_id=route_table.attr_route_table_id,
        subnet_id=public_subnet.attr_subnet_id)

        
        # Defining a new ec2 instance
        ec2_instance = ec2.CfnInstance(
            self,
            "CDKInstance",
            key_name=KeyPair.value_as_string,
            instance_type=InstanceType.value_as_string,
            image_id=AmiId.value_as_string,
            subnet_id=public_subnet.attr_subnet_id,
            tags=[core.CfnTag(key="Name", 
            value=InstanceName.value_as_string)],
            user_data=base64_user_data,
            availability_zone='ap-south-1a',
            security_group_ids=[security_group.attr_group_id]
        )