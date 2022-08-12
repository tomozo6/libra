resource "aws_route53_record" "libra" {
  zone_id = data.aws_route53_zone.tomozo6_com.zone_id
  name    = local.www.fqdn
  type    = "A"

  alias {
    name                   = module.www_cloudfront.domain_name
    zone_id                = module.www_cloudfront.hosted_zone_id
    evaluate_target_health = false
  }
}