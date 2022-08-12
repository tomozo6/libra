data "aws_api_gateway_domain_name" "libra" {
  domain_name = local.fqdn
}