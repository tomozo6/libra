# ------------------------------------------------------------------------------
# CloudFront
# ------------------------------------------------------------------------------
resource "aws_cloudfront_distribution" "libra" {
  aliases             = [local.fqdn]
  comment             = "Managed by Terraform"
  default_root_object = "index.html"
  enabled             = true
  http_version        = "http2"
  is_ipv6_enabled     = true
  price_class         = "PriceClass_200"
  retain_on_delete    = false
  wait_for_deployment = false
  web_acl_id          = null
  tags                = local.tags

  logging_config {
    include_cookies = false
    bucket          = aws_s3_bucket.log.bucket_domain_name
    prefix          = format("cf/%s/", local.fqdn)
  }


  origin {
    domain_name = aws_s3_bucket.website.website_endpoint
    origin_id   = aws_s3_bucket.website.bucket
    origin_path = ""

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "http-only"
      origin_ssl_protocols   = ["TLSv1.2"]

    }
  }

  origin {
    domain_name = local.api_gateway_domain_name
    origin_id   = "apigateway"
    origin_path = ""

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "https-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  default_cache_behavior {
    target_origin_id       = aws_s3_bucket.website.bucket
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods        = ["HEAD", "GET", "OPTIONS"]
    cached_methods         = ["HEAD", "GET", "OPTIONS"]
    compress               = true
    min_ttl                = 0
    default_ttl            = 0
    max_ttl                = 0

    forwarded_values {
      query_string = false

      cookies {
        forward = "none"
      }
    }
  }

  ordered_cache_behavior {
    target_origin_id       = "apigateway"
    path_pattern           = "api/*"
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods        = ["HEAD", "DELETE", "POST", "GET", "OPTIONS", "PUT", "PATCH"]
    cached_methods         = ["HEAD", "GET"]
    compress               = true
    min_ttl                = 0
    default_ttl            = 0
    max_ttl                = 0

    forwarded_values {
      query_string = false

      cookies {
        forward = "none"
      }
    }
  }

  viewer_certificate {
    acm_certificate_arn      = data.aws_acm_certificate.libra_us-east-1.arn
    minimum_protocol_version = "TLSv1.2_2021"
    ssl_support_method       = "sni-only"
  }

  restrictions {
    geo_restriction {
      restriction_type = "whitelist"
      locations        = ["JP"]
    }
  }
}
