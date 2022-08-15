# -----------------------------------------------------------------------
# *.libra.tomozo6.com
# -----------------------------------------------------------------------
# ap-northeast-1
resource "aws_acm_certificate" "libra" {
  domain_name               = "*.libra.tomozo6.com"
  subject_alternative_names = []
  validation_method         = "DNS"
  tags                      = local.tags
}

resource "aws_route53_record" "libra_acm" {
  for_each = {
    for i in aws_acm_certificate.libra.domain_validation_options : i.domain_name => {
      name   = i.resource_record_name
      record = i.resource_record_value
      type   = i.resource_record_type
    }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 60
  type            = each.value.type
  zone_id         = local.zone_id
}


resource "aws_acm_certificate_validation" "libra" {
  certificate_arn         = aws_acm_certificate.libra.arn
  validation_record_fqdns = [for record in aws_route53_record.libra_acm : record.fqdn]
}

