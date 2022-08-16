# -----------------------------------------------------------------------
# libra.tomozo6.com
# -----------------------------------------------------------------------
# ap-northeast-1
data "aws_acm_certificate" "tomozo6_com" {
  domain      = "libra.tomozo6.com"
  statuses    = ["ISSUED"]
  most_recent = true
}

