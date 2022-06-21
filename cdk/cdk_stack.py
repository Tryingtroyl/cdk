import aws_cdk as core
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_ssm as ssm

vpcID="vpc-0036d569"
vpcCidr='192.168.50.0/24'
instanceName="webserver-1"
instanceType="t2.micro"
amiName="amzn2-ami-hvm-2.0.20200520.1-x86_64-gp2"
keypair="hygieia"
with open("cdk/data/userdata.sh") as f:
    user_data = f.read()

class Ec2InstanceStack(core.Stack):

    def __init__(self, scope: core.App, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Stack definition

        # Find an already existing VPC using the VPC ID
        # vpc = ec2.Vpc.from_lookup(
        #     self,
        #     "vpc",
        #     vpc_id=vpcID,
        # )

        env_name = self.node.try_get_context("env")

        InstanceType = core.CfnParameter(self, "InstanceType", type="String", default="t2.micro",
        description="The type of the instance.")
        InstanceName = core.CfnParameter(self, "InstanceName", type="String", default="webserver-7",
        description="The name of the instance.")

        self.vpc = ec2.CfnVPC(self, 'CDKVPC',
            cidr_block = vpcCidr,
            # max_azs = 2,
            # enable_dns_hostnames = True,
            # enable_dns_support = True, 
            # subnet_configuration=[
            #     ec2.SubnetConfiguration(
            #         name = 'Public-Subent',
            #         subnet_type = ec2.SubnetType.PUBLIC,
            #         cidr_mask = 26,
            #     ),
            #     ec2.SubnetConfiguration(
            #         name = 'Private-Subnet',
            #         subnet_type = ec2.SubnetType.PRIVATE_WITH_NAT,
            #         cidr_mask = 26
                # )
            # ],
            # nat_gateways = 1,
        )
        print(self.vpc)
        # priv_subnets = [subnet.subnet_id for subnet in self.vpc.private_subnets]

        # count = 1
        # for psub in priv_subnets: 
        #     ssm.StringParameter(self, f'private-subnet-{count}',
        #         string_value = psub,
        #         parameter_name = f'/{env_name}private-subnet-{count}'
        #         )
        #     count += 1 


        
        # Creating a new security group
        # security_group = ec2.CfnSecurityGroup(
        #     self,
        #     "sec-group-allow-ssh",
        #     vpc=self.vpc,
        #     allow_all_outbound=True,
        # )

        # # Adding a new inbound rule to allow port 22 to external hosts
        # security_group.add_ingress_rule(
        #     peer=ec2.Peer.ipv4('0.0.0.0/0'),
        #     description="Allow SSH connection", 
        #     connection=ec2.Port.tcp(22)
        # )
        
        # # Adding a new inbound rule to allow port 80 to external hosts
        # security_group.add_ingress_rule(
        #     peer=ec2.Peer.ipv4('0.0.0.0/0'),
        #     description="Allow Http connection", 
        #     connection=ec2.Port.tcp(80)
        # )

        security_group = ec2.CfnSecurityGroup(self, "CDKSecurityGroup",
            group_description="groupDescription",

            security_group_egress=[ec2.CfnSecurityGroup.EgressProperty(
                ip_protocol="tcp",

                # the properties below are optional
                cidr_ip="0.0.0.0/0",
                from_port=-1,
                to_port=-1
            )],
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
            
        public_subnet = ec2.CfnSubnet(self, "CDKSubnet", vpc_id = self.vpc.attr_vpc_id)
        # Defining a new ec2 instance
        ec2_instance = ec2.CfnInstance(
            self,
            "CDKInstance",
            # instance_name=InstanceName.value_as_string,
            # instance_type=ec2.InstanceType(InstanceType.value_as_string),
            # machine_image=ec2.MachineImage().lookup(name=amiName),
            # vpc=self.vpc,
            # security_group=security_group,
            # user_data=ec2.UserData.custom(user_data),
            key_name=keypair,
            # vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC)
            instance_type="t2.micro",
            image_id="ami-08df646e18b182346",
            subnet_id=public_subnet
        )