# Messages

## DEPLOYMENT
```bash
#create the configmap for the messages database
kubectl create configmap mysql-initdb-messages -n egs-ressellr --from-file=./db/dbInit.sql

# The rest of the deployment is done with the following commands
docker buildx build --platform linux/amd64 --network=host -t registry.deti:5000/egs-ressellr/messages:v1.5 .
docker push registry.deti:5000/egs-ressellr/messages:v1.5

kubectl apply -f storage.yaml
kubectl apply -f deployment.yaml
kubectl get pods -n egs-ressellr
kubectl get services -n egs-ressellr

kubectl delete -f deployment.yaml
kubectl delete -f storage.yaml
```