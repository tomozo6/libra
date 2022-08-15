# -----------------------------------------------------------------------
# tomozo6.com
# -----------------------------------------------------------------------
data "aws_route53_zone" "tomozo6_com" {
  name = "tomozo6.com"
}

# -----------------------------------------------------------------------
# libra
# -----------------------------------------------------------------------
resource "aws_route53_record" "libra" {
  zone_id = data.aws_route53_zone.tomozo6_com.zone_id
  name    = local.fqdn
  type    = "A"

  alias {
    name                   = data.aws_api_gateway_domain_name.libra.regional_domain_name
    zone_id                = data.aws_api_gateway_domain_name.libra.regional_zone_id
    evaluate_target_health = false
  }
}