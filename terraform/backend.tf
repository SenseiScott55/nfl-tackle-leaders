terraform {
  backend "s3" {
    bucket         = "nfl-tackle-leaders-terraform-state"
    key            = "terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "nfl-tackle-leaders-terraform-locks"
    encrypt        = true
  }
}