provider "aws" {
  region = "us-east-1"
}

resource "aws_security_group" "securitygroup" {
  name        = "ec2-securitygroup"
  description = "Ingress Http and SSH and Egress to anywhere "

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "ec2" {
  ami                    = "ami-012967cc5a8c9f891"
  instance_type          = "t2.micro"
  user_data              = file("user_data.sh")
  vpc_security_group_ids = ["${aws_security_group.securitygroup.id}"]
  depends_on = [ aws_security_group.securitygroup ]
}

output "public_ip" {
  value = aws_instance.ec2.public_ip
}