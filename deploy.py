import os
import json

flag2='n'
flag1=input("Do you want to synthesise first (Type 'y' if there are any changes)?(y/n) ")
if(flag1 == 'y' or flag1 == 'Y'):
    try:
        os.system("cdk synth")
    except:
        raise
    flag2=input("Do you want to deploy the above stack?(y/n) ")

if(flag2 == 'y' or flag2 == 'Y' or flag1 != 'y' or flag1 != 'Y'):
    try:
        parameter_file = open('cdk/data/parameters.json','r')
        Parameters=json.load(parameter_file)

        command=f"cdk deploy --require-approval never "
        for key, value in Parameters.items():
            command=command+f"--parameters {key}={value} "

        os.system(command)

    except:
        raise

