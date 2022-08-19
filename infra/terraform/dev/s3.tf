# ------------------------------------------------------------------------------
# WebSite
# ------------------------------------------------------------------------------
resource "aws_s3_bucket" "website" {
  bucket        = format("%s-%s-website-s3", local.tags.project, local.tags.env)
  force_destroy = false
  tags          = local.tags
}

resource "aws_s3_bucket_server_side_encryption_configuration" "website" {
  bucket = aws_s3_bucket.website.bucket

  rule {
    bucket_key_enabled = true

    apply_server_side_encryption_by_default {
      sse_algorithm     = "AES256"
      kms_master_key_id = null
    }
  }
}

resource "aws_s3_bucket_website_configuration" "website" {
  bucket = aws_s3_bucket.website.bucket

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "error.html"
  }
}

resource "aws_s3_bucket_ownership_controls" "website" {
  bucket = aws_s3_bucket.website.bucket

  rule {
    object_ownership = "BucketOwnerEnforced"
  }
}

resource "aws_s3_bucket_policy" "website" {
  bucket = aws_s3_bucket.website.bucket

  policy = templatefile("files/libra-website-s3-bucket-policy.json", {
    bucket_name = format("%s-%s-website-s3", local.tags.project, local.tags.env)
  })
}

resource "aws_s3_bucket_public_access_block" "website" {
  bucket                  = aws_s3_bucket.website.bucket
  block_public_acls       = true
  block_public_policy     = false
  ignore_public_acls      = true
  restrict_public_buckets = false
}

resource "aws_s3_bucket_logging" "website" {
  bucket        = aws_s3_bucket.website.bucket
  target_bucket = aws_s3_bucket.log.bucket
  target_prefix = "s3/"
}

# ------------------------------------------------------------------------------
# Log
# ------------------------------------------------------------------------------
resource "aws_s3_bucket" "log" {
  bucket        = format("%s-%s-log-s3", local.tags.project, local.tags.env)
  force_destroy = false
  tags          = local.tags
}

resource "aws_s3_bucket_server_side_encryption_configuration" "log" {
  bucket = aws_s3_bucket.log.bucket

  rule {
    bucket_key_enabled = true

    apply_server_side_encryption_by_default {
      sse_algorithm     = "AES256"
      kms_master_key_id = null
    }
  }
}

resource "aws_s3_bucket_acl" "log" {
  bucket = aws_s3_bucket.log.bucket
  acl    = "log-delivery-write"
}
