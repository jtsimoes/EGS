# Authentication 

## DEPLOYMENT
```bash
docker buildx build --platform linux/amd64 --network=host -t registry.deti:5000/egs-ressellr/authentication:v1 .
docker push registry.deti:5000/egs-ressellr/authentication:v1

kubectl apply -f deployment.yaml
kubectl get pods -n egs-ressellr
kubectl get services -n egs-ressellr

kubectl delete -f deployment.yaml
```