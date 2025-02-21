import jinja2file

class UserSelectionError(Exception): # i created a custom exception for try-except
    pass

#taking ami, instance type and region from the user
def user_input():
    ami = {"1": "ami-0f9575d3d509bae0c", "2": "ami-0f1a6835595fb9246"}
    instances = {"1": "t3.small", "2": "t3.medium"}
    region = "us-east-1"
    alb_name = "" #default name 
    try:
        #taking ami choise
        ami_choise = input("Choose an AMI: 1-Ubuntu or 2-Amazon Linux: ")
        if ami_choise not in ami:
            raise UserSelectionError("Invalid AMI selection.")
        #taking instance type choise
        instance_choise = input("Choose an instance type: 1- t3.small or 2- t3.medium: ")
        if instance_choise not in instances:
            raise UserSelectionError("Invalid instance type selection.")
        #taking region choise
        region_choise = input("Choose a region (default is us-east-1): ")
        if region_choise and region_choise != "us-east-1": #if the user enters somthing else than us-east-1
            print("Wrong region! Setting region to \"us-east-1\".")
            region_choise = "us-east-1"
        
        #user enters a non-empty alb name
        while not alb_name:
            alb_name = input("Please enter Load Balancer name: ").strip()
            if not alb_name: #checking if the name is empty
                print("alb name cannot be empty! try again.")
            else:
                break

        # returning the data 
        return {
            "ami": ami[ami_choise],
            "instance_type": instances[instance_choise],
            "region": region_choise,
            "alb_name": alb_name
        }
    
    #if user enters wrong values, it raises a UserSelectionError with the right message
    except UserSelectionError as e:
        print(f"Error: {e}")
        return {}

tf_info = user_input()
jinja2file.create_tf_file(tf_info)
