resource "aws_lambda_function" "wordle_cracker" {
  function_name = "wordlecracker-container"
  role          = "arn:aws:iam::715871776555:role/lambda_executor"
  package_type  = "Image"
  image_uri     = "715871776555.dkr.ecr.ap-southeast-2.amazonaws.com/wordlecracker:7731c1c66f2e836312ff1f403781e18afccdf711"
  memory_size   = 1024
  timeout       = 300
  environment {
    variables = {
      "LOG_LEVEL"  = "INFO"
      "bucket"     = "wordlecracker-s3"
      "dictionary" = "words-5.txt"
      "results"    = "everyday_results.json"
    }
  }
}

resource "aws_cloudwatch_event_rule" "daily-trigger" {
  event_pattern       = null
  schedule_expression = "cron(0 12 * * ? *)"
}

resource "aws_cloudwatch_event_target" "wordlecracker-container" {
  rule = "daily-trigger"
  arn  = aws_lambda_function.wordle_cracker.arn
}

resource "aws_s3_bucket" "wordlecracker-s3" {
  bucket = "wordlecracker-s3"
}

resource "aws_ecr_repository" "wordlecracker-ecr" {
  name      = "wordlecracker"
#   image_uri = "715871776555.dkr.ecr.ap-southeast-2.amazonaws.com/wordlecracker"
}
