import os

try:
    os.system("cdk destroy --force")
except:
    raise