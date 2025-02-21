from python_terraform import Terraform
import sys

# path to the dir that has the tf file (this folder)
tf = Terraform(working_dir='./')

# run terraform init
print("Running terraform init...")
output = tf.init(capture_output = True)
if "Error" in output[2]: #if there is an error prints it 
    print(f"Error during terraform plan: {output[2]}")
else:
    print(output[1]) #prints the output of init

# run terraform plan
print("Running terraform plan...")
output = tf.plan(capture_output = True)
if "Error" in output[2]:
    print(f"Error during terraform plan: {output[2]}")
else:
    print(output[1])#prints the output of plan



# run terraform apply
print("Running terraform apply...")
apply_code, apply_stdout, apply_stderr = tf.apply(skip_plan=True) #skip plain because it already performed it 
output = tf.apply(skip_plan=True)
if "Error" in output[2]:
    print(f"Error during terraform plan: {output[2]}")
else:
    print(output[1]) #prints the output of apply

# taking the output of the terraform
output_code, output_stdout, output_stderr = tf.output()
if output_code != 0:
    print(f"Error capturing Terraform output: {output_stderr}")
    sys.exit(1)

# displaying instance ID, LB DNS name
print("Terraform Output:")
print(output_stdout)
