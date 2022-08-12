provider "aws" {
  region = "ap-northeast-1"
}

provider "aws" {
  alias  = "us-east-1"
  region = "us-east-1"
}

terraform {
  backend "s3" {
    bucket = "tomozo-base-terraform-s3"
    key    = "tomozo-dev-libra.tfstate"
    region = "ap-northeast-1"
  }
}