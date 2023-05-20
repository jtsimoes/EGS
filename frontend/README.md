# Frontend

To install all the requirements, simply type in the terminal:

    $ pip install -r requirements.txt

To run, simply type in the terminal:

    $ uvicorn main:app --reload 

After that, the app should be running on browser `localhost` at port 8000.

For a production environment, you should remove the flag `--reload` and, if needed, you can custom the host and the port where you want to run the app:

    $ uvicorn main:app --host 0.0.0.0 --port 80

## DEPLOYMENT

```bash
docker buildx build --platform linux/amd64 --network=host -t registry.deti:5000/egs-ressellr/frontend:v1 .
docker push registry.deti:5000/egs-ressellr/frontend:v1

kubectl apply -f storage.yaml
kubectl apply -f deployment.yaml
kubectl get pods -n egs-ressellr
kubectl get services -n egs-ressellr

kubectl delete -f deployment.yaml
kubectl delete -f storage.yaml
```