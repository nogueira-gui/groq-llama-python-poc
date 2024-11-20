provider "aws" {
  region = "us-east-1"
}


# Role para a instância EC2
# resource "aws_iam_role" "ec2_ssm_role" {
#   name               = "ec2-ssm-role"
#   assume_role_policy = jsonencode({
#     Version = "2012-10-17",
#     Statement = [
#       {
#         Effect    = "Allow",
#         Principal = {
#           Service = "ec2.amazonaws.com"
#         },
#         Action = "sts:AssumeRole"
#       }
#     ]
#   })
# }

# # Política gerenciada do SSM Parameter Store anexada à Role
# resource "aws_iam_policy_attachment" "ssm_policy" {
#   name       = "ssm-policy-attachment"
#   roles      = ["ec2-ssm-role"]
#   policy_arn = "arn:aws:iam::aws:policy/AmazonSSMFullAccess"
# }

# # Perfil de instância para anexar a Role à EC2
# resource "aws_iam_instance_profile" "ec2_instance_profile" {
#   name = "ec2-instance-profile"
#   role = "ec2-ssm-role"
# }

#data "aws_security_group" "existing_sg" {
 # filter {
 #   name   = "group-name"
 #   values = ["ec2-securitygroup"]
 # }
#}
# resource "aws_security_group" "securitygroup" {
#   name        = "ec2-securitygroup"
#   description = "Ingress Http and SSH and Egress to anywhere"

#   ingress {
#     from_port   = 80
#     to_port     = 80
#     protocol    = "tcp"
#     cidr_blocks = ["0.0.0.0/0"]
#   }

#   ingress {
#     from_port   = 22
#     to_port     = 22
#     protocol    = "tcp"
#     cidr_blocks = ["0.0.0.0/0"]
#   }

#   egress {
#     from_port   = 0
#     to_port     = 65535
#     protocol    = "tcp"
#     cidr_blocks = ["0.0.0.0/0"]
#   }
# }

# resource "aws_instance" "ec2" {
#   ami                    = "ami-012967cc5a8c9f891"
#   instance_type          = "t2.micro"
#   user_data              = file("user_data.sh")
#   iam_instance_profile = "ec2-instance-profile"
#   vpc_security_group_ids = [data.aws_security_group.existing_sg.id]
# }

# output "public_ip" {
#   value = aws_instance.ec2.public_ip
# }


