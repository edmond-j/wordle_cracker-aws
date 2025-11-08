715871776555.dkr.ecr.ap-southeast-2.amazonaws.com/wordlecracker:latest

715871776555.dkr.ecr.ap-southeast-2.amazonaws.com/lambda-python_chrome:3.10

aws ecr get-login-password --region ap-southeast-2 | docker login --username AWS --password-stdin 715871776555.dkr.ecr.ap-southeast-2.amazonaws.com

docker run -it --rm <image ID> /bin/bash

sam build

sam deploy --guided

sam local invoke WordleCrackerLambda -e .\events\event.json   

docker build -t 715871776555.dkr.ecr.ap-southeast-2.amazonaws.com/wordlecracker:latest .

docker push 715871776555.dkr.ecr.ap-southeast-2.amazonaws.com/wordlecracker:latest 

#获取最新的image的uri，且挑选有容量的那个，一般是第二个，所以用imageDetails[1]  
$image = aws ecr describe-images --repository-name wordlecracker --query 'imageDetails[1].imageDigest' --output text

#自动化更新image  
aws lambda update-function-code --function-name wordlecracker-container --image-uri 715871776555.dkr.ecr.ap-southeast-2.amazonaws.com/wordlecracker@${image}
