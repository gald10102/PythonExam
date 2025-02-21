from python_terraform import Terraform
import sys

# path to the dir that has the tf file (this folder)
tf = Terraform(working_dir='./')

# run terraform init
print("Running terraform init...")
init_code, init_stdout, init_stderr = tf.init()
if init_code != 0:
    print(f"Error during terraform init: {init_stderr}")
    sys.exit(1)
else:
    print(init_stdout)

# run terraform plan
print("Running terraform plan...")
plan_code, plan_stdout, plan_stderr = tf.plan()
if plan_code != 0:
    print(f"Error during terraform plan: {plan_stderr}")
    sys.exit(1)
else:
    print(plan_stdout)


# run terraform apply
print("Running terraform apply...")
apply_code, apply_stdout, apply_stderr = tf.apply(skip_plan=True)
if apply_code != 0:
    print(f"Error during terraform apply: {apply_stderr}")
    sys.exit(1)
else:
    print(apply_stdout)

# taking the output of the terraform
output_code, output_stdout, output_stderr = tf.output()
if output_code != 0:
    print(f"Error capturing Terraform output: {output_stderr}")
    sys.exit(1)

# displaying instance ID, LB DNS name
print("Terraform Output:")
print(output_stdout)
