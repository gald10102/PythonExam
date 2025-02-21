Gal Danenberg

This file contains the folloing files:
1.Python Script - deploymentscript.py - (getting the user input and sends it to jinja2)
2.Jinja2fie.py  - this file creates terraform file (.tf)
3.Generated Terraform File - tf_template.tf - The .tf file created from the Jinja2 template.
4.Authantication file - terraformauth.py -  using python-terraform to init, plan and apply the tf code.
5.Validation code using boto3 - validation.py
6.AWS Validation JSON (aws_validation.json) - Proof that the deployment succeeded.
