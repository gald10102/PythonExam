import jinja2

#taking the data from the deployment file and creating terraform file using jinja2
def create_tf_file(aws_info):
  terraform_template = """
  provider "aws" {
    region = "{{ region }}"
  }

  resource "aws_instance" "web_server" {
    ami           = "{{ ami }}"
    instance_type = "{{ instance_type }}"
    availability_zone = "{{ availability_zone }}"
    subnet_id = aws_subnet.public[0].id
    tags = {
      Name = "WebServer"
    }
  }

  resource "aws_lb" "application_lb" {
    name               = "{{ alb_name }}"
    internal           = false
    load_balancer_type = "application"
    security_groups    = [aws_security_group.lb_sg.id]
    subnets            = aws_subnet.public[*].id
    depends_on         = [aws_security_group.lb_sg]
  }

  resource "aws_security_group" "lb_sg" {
    name        = "gal-lb_security_group"
    description = "Allow HTTP inbound traffic"

    ingress {
      from_port   = 80
      to_port     = 80
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }

    egress {
      from_port   = 0
      to_port     = 0
      protocol    = "-1"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }

  resource "aws_lb_listener" "http_listener" {
    load_balancer_arn = aws_lb.application_lb.arn
    port              = 80
    protocol          = "HTTP"

    default_action {
      type             = "forward"
      target_group_arn = aws_lb_target_group.web_target_group.arn
    }
  }

  resource "aws_lb_target_group" "web_target_group" {
    name     = "gal-web-target-group"
    port     = 80
    protocol = "HTTP"
    vpc_id   = aws_vpc.main.id
  }

  resource "aws_lb_target_group_attachment" "web_instance_attachment" {
    target_group_arn = aws_lb_target_group.web_target_group.arn
    target_id        = aws_instance.web_server.id
  }

  resource "aws_vpc" "main" {
    cidr_block = "10.0.0.0/16"
  }

  resource "aws_subnet" "public" {
    count = 2
    vpc_id = aws_vpc.main.id
    cidr_block = "10.0.${count.index}.0/24"
    availability_zone = element(["us-east-1a", "us-east-1b"], count.index)
  }

  resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  }

  resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
}

  resource "aws_route" "public_route" {
    route_table_id         = aws_route_table.public.id
    destination_cidr_block = "0.0.0.0/0"
    gateway_id             = aws_internet_gateway.main.id
  }
  
  resource "aws_route_table_association" "public_association" {
    count          = 2
    subnet_id      = aws_subnet.public[count.index].id
    route_table_id = aws_route_table.public.id
  }

  """
  
  template = jinja2.Template(terraform_template)
  terraform_config = template.render(aws_info)
  #saving the template into a file named "tf_template.tf"
  try:
    with open("tf_template.tf", "w") as f:
        f.write(terraform_config)
  except:
    print("Error creating terraform file!")
    return
  
  print("Terraform configuration has been generated in 'tf_template.tf'.")
