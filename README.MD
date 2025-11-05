715871776555.dkr.ecr.ap-southeast-2.amazonaws.com/wordlecracker-ecr:latest
715871776555.dkr.ecr.ap-southeast-2.amazonaws.com/lambda-python_chrome:3.10

aws ecr get-login-password --region ap-southeast-2 | docker login --username AWS --password-stdin 715871776555.dkr.ecr.ap-southeast-2.amazonaws.com

docker run -it --rm <image ID> /bin/bash

sam build

sam deploy --guided

sam local invoke WordleCrackerLambda -e .\events\event.json   
