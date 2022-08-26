# -----------------------------------------------------------------------------
# IAM
# -----------------------------------------------------------------------------
resource "aws_iam_role" "auth-lambdaedge" {
  name               = format("%s-%s-auth-lambdaedge-role", local.tags.project, local.tags.env)
  assume_role_policy = data.aws_iam_policy_document.auth-lambdaedge-assumerole.json
}

data "aws_iam_policy_document" "auth-lambdaedge-assumerole" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type = "Service"
      identifiers = [
        "lambda.amazonaws.com",
        "edgelambda.amazonaws.com"
      ]
    }
  }
}

resource "aws_iam_role_policy_attachment" "auth-lambdaedge-basic" {
  role       = aws_iam_role.auth-lambdaedge.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}


data "aws_iam_policy_document" "auth-lambdaedge" {
  statement {
    effect = "Allow"
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    resources = [
      "arn:aws:logs:*:*:*"
    ]
  }
}

resource "aws_iam_policy" "auth-lambdaedge" {
  name   = format("%s-%s-auth-lambdaedge-policy", local.tags.project, local.tags.env)
  path   = "/"
  policy = data.aws_iam_policy_document.auth-lambdaedge.json
}

resource "aws_iam_role_policy_attachment" "auth-lambdaedge" {
  role       = aws_iam_role.auth-lambdaedge.name
  policy_arn = aws_iam_policy.auth-lambdaedge.arn
}

