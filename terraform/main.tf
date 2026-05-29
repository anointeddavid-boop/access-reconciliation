provider "aws" {
  region = "us-east-1"
}

# S3 bucket for input files
resource "aws_s3_bucket" "input_bucket" {
  bucket = "access-reconciliation-input-030157669158"
}

# S3 bucket for output files
resource "aws_s3_bucket" "output_bucket" {
  bucket = "access-reconciliation-output-030157669158"
}
