# New commands for hybrid cloud

```bash
docker build -t hybrid-cloud .
docker tag hybrid-cloud:latest hasagar97/hybrid-cloud:latest
docker push hasagar97/hybrid-cloud:latest
docker run -it --entrypoint bash hybrid-cloud
```

## Cloning repo in openfaas
```
git clone -b hybrid-cloud https://github.com/AnirudhPI/video-processing-lambda.git
```


## Faas cli
```bash
faas-cli new --lang dockerfile procvideo
#get cluster IP
kubectl get service -n openfaas

# checking the services
kubectl get deploy -n openfaas



# faas-cli build -f procvideo
faas-cli deploy -f procvideo.yml -n openfaas --gateway 10.104.206.67
faas-cli deploy --image hybrid-cloud:latest --name docker-only-facerecog
```

- debugging links: 
1. https://stackoverflow.com/questions/70174034/open-faas-function-will-not-deploy
2. https://docs.openfaas.com/deployment/troubleshooting/


```bash
#get cluster IP
kubectl get service -n openfaas

# checking the services
kubectl get deploy -n openfaas

# checking my image 
docker run -it --entrypoint bash  hasagar97/hybrid-cloud:latest

# faas-cli build -f procvideo
faas-cli deploy -f procvideo.yml -n openfaas --gateway 10.104.206.67
```


### trying different ways to launch the openfaas

```bash

# internal gateway
faas-cli deploy -f facerecog.yml -n openfaas --gateway 10.104.206.67


# using image
faas-cli deploy --image hasagar97/hybrid-cloud:latest --name facerecog-docker --gateway 192.168.49.2
```
## Some success

```bash
export gw=http://$(minikube ip):31112
faas-cli deploy --image hasagar97/hybrid-cloud:latest --name facerecog-docker --gateway 192.168.49.2:31112


# Checking functions that are running
export gw=http://$(minikube ip):31112
faas-cli list --gateway $gw
# check for 0/1 here
kubectl get deploy -n openfaas-fn



# checking the logs
faas-cli logs hybrid-cloud --gateway $gw

```

## trying new faas method using yml file

```bash 
export gw=http://$(minikube ip):31112
faas-cli deploy -f facerecog.yml --gateway $gw


```


#### facrecog.yml
```yml
version: 1.0
provider:
  name: openfaas

functions:
  facerecog:
    image: hasagar97/hybrid-cloud:latest
    labels:
      com.openfaas.scale.min: 1
      com.openfaas.scale.max: 20

```

## testing faas

```python
import requests
event = {
                "Records": [
                    {
                        "s3": 
                        {
                            "object": {
                                "key": "test_0.mp4"
                            }
                        }
                    }   
                ]
            }
response = requests.post(url="http://192.168.49.2:31112/function/hybrid-cloud", data=event)

```

```bash
faas-cli list --gateway $gw
echo '{"Records":[{"s3":{"object":{"key":"test_0.mp4"}}}]}' | faas-cli invoke hybrid-cloud --gateway $gw

```


### Attemp 5 using new link
- link: https://github.com/openfaas/faas-cli/issues/603

```bash
export gw=http://$(minikube ip):31112

faas new --lang=dockerfile --prefix=hasagar97 hybrid-cloud --gateway=$gw
faas-cli deploy --image hasagar97/hybrid-cloud:latest --name hybrid-cloud --gateway $gw



faas-cli deploy -f hybrid-cloud.yml --gateway $gw
faas-cli invoke hybrid-cloud --gateway $gw
```


### Deleting functions
```sh
faas-cli rm  facerecog-docker --gateway=$gw
faas-cli rm  hybrid-cloud --gateway=$gw

```


#### Scaling

https://www.openfaas.com/blog/health-and-readiness-for-functions/


# How to run

- make sure you have the test cases folder copied in this folder

```bash
aws configure
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 022286511304.dkr.ecr.us-east-1.amazonaws.com
python workload.py


```


# Making the docker image



```bash
docker build -t image5 .   
docker tag image5 022286511304.dkr.ecr.us-east-1.amazonaws.com/video-processing-image:latest

# push
docker push 022286511304.dkr.ecr.us-east-1.amazonaws.com/video-processing-image:latest 
```



# Appendix for the brave










# steps to create a new docker

```bash
docker build --platform linux/amd64 -t video-image-fixed:test .
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 022286511304.dkr.ecr.us-east-1.amazonaws.com

aws ecr create-repository --repository-name video-image-fixed --region us-east-1 --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE


```

## Now you would have a repo with a response similar to this:
```json
{
    "repository": {
        "repositoryArn": "arn:aws:ecr:us-east-1:022286511304:repository/video-image-fixed",
        "registryId": "022286511304",
        "repositoryName": "video-image-fixed",
        "repositoryUri": "022286511304.dkr.ecr.us-east-1.amazonaws.com/video-image-fixed",
        "createdAt": "2023-10-25T21:01:23-07:00",
        "imageTagMutability": "MUTABLE",
        "imageScanningConfiguration": {
            "scanOnPush": true
        },
        "encryptionConfiguration": {
            "encryptionType": "AES256"
        }
    }
}
```

- next tag and push the image

```bash
docker build -t image5 .   
docker tag image5 022286511304.dkr.ecr.us-east-1.amazonaws.com/video-processing-image:latest

# push
docker push 022286511304.dkr.ecr.us-east-1.amazonaws.com/video-processing-image:latest 
```


### testing the function

```bash

aws lambda create-function --function-name video-proc-fixed --package-type Image --code ImageUri=022286511304.dkr.ecr.us-east-1.amazonaws.com/video-processing-image:latest --role arn:aws:iam::022286511304:role/LambdaAccess --region us-east-1 

aws s3api put-bucket-notification-configuration --bucket inputbucket-cloudcomputing2 --notification-configuration "{\"LambdaFunctionConfigurations\":[{\"LambdaFunctionArn\":\"arn:aws:lambda:us-east-1:022286511304:function:video-proc-fixed\",\"Events\":[\"s3:ObjectCreated:*\"]}]}"


aws lambda invoke --function-name hello-world response.json --region us-east-1


aws configure
# upload: .\test_7.mp4 to s3://inputbucket-cloudcomputing2/test_7.mp4

aws s3 cp test_2.mp4 s3://inputbucket-cloudcomputing2/

```