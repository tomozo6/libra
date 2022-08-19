data "aws_acm_certificate" "libra_us-east-1" {
  provider    = aws.us-east-1
  domain      = "*.libra.tomozo6.com"
  statuses    = ["ISSUED"]
  most_recent = true
}
