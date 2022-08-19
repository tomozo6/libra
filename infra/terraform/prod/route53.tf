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
    name                   = aws_cloudfront_distribution.libra.domain_name
    zone_id                = aws_cloudfront_distribution.libra.hosted_zone_id
    evaluate_target_health = false
  }
}