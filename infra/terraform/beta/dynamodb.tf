resource "aws_dynamodb_table" "pay" {
  name           = format("%s-%s-pay-dynamodb-table", local.tags.project, local.tags.env)
  billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1
  hash_key       = "Payer"
  range_key      = "InputDate"

  attribute {
    name = "Payer"
    type = "S"
  }

  attribute {
    name = "InputDate"
    type = "S"
  }
}
