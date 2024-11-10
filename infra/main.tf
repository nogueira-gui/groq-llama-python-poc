provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "ec2" {
  ami                    = "ami-0c101f26f147fa7fd"
  instance_type          = "t2.nano"
  user_data              = file("user_data.sh")
  vpc_security_group_ids = ["ec2-securitygroup"]
}

output "public_ip" {
  value = aws_instance.ec2.public_ip
}