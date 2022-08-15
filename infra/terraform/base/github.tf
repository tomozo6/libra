# -----------------------------------------------------------------------
# OIDC Provider
# -----------------------------------------------------------------------
resource "aws_iam_openid_connect_provider" "github_actions" {
  url             = "https://token.actions.githubusercontent.com"
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = ["6938fd4d98bab03faadb97b34396831e3780aea1"]
}

# -----------------------------------------------------------------------
# IAM Role
# -----------------------------------------------------------------------
resource "aws_iam_role" "github_actions" {
  name = format("%s-%s-githubactions-role", local.tags.project, local.tags.env)
  path = "/"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = "sts:AssumeRoleWithWebIdentity"
        Principal = {
          Federated = aws_iam_openid_connect_provider.github_actions.arn
        }
        Condition = {
          StringEquals = {
            "token.actions.githubusercontent.com:aud" = "sts.amazonaws.com"
          },
          StringLike = {
            "token.actions.githubusercontent.com:sub" = [
              "repo:${local.github.org}/${local.github.repo}:*"
            ]
          }
        }
      }
    ]
  })
}

# -----------------------------------------------------------------------
# IAM Policy
# -----------------------------------------------------------------------
resource "aws_iam_role_policy_attachment" "github_actions" {
  role = aws_iam_role.github_actions.name
  for_each = toset(concat([
    "arn:aws:iam::aws:policy/AdministratorAccess"
  ]))
  policy_arn = each.value
}
