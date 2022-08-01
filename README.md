# Projeto -  APP Flask realizando deploy no Kubernetes

##  Sobre o Projeto 

Projeto afins de estudos com o objetivo de práticar o uso da ferramenta de orquestração chamada Kubernetes (K8S).


### Resumo Aplicação

Criada uma aplicação utilizando a biblioteca Flask do Python, com o objetivo do usuário digitar uma sigla referente
a um FII (fundo imobiliário) e através desse papel digitado o usuário é encaminhado para uma página na qual ele contém as principais informações 
sobre o FII escolhido.

Site na qual o usuário é encaminhado: https://www.fundsexplorer.com.br/funds/


### Objetivo

Foram criados de forma declarativas alguns scripts no formato YAML para a criação de Deployments,
Namespace e Services diretamente no Azure - AKS (Serviço de Kubernetes Gerenciado).



***Scripts disponíveis no path***: app-final/app.yaml



#### Ferramentas utilizadas no desenvolvimento

- Azure AKS (Serviço de Kubernetes Gerenciado)  
- Azure ACR (Azure container registry)
- Docker Hub
- VsCode

#### Linguagens utilizadas no desenvolvimento

- Python (módulo Flask)
- Html
- YAML


## Desenvolvimento

- Código da aplicação utilizando a biblioteca Flask do Python.

```
from flask import Flask, redirect, url_for, render_template,request


app = Flask(__name__)

@app.route("/funds")
@app.route("/", methods=['GET', 'POST'])   # criando rota principal
def bemvindo():
    if request.method == 'POST':
        FII_desejado  = request.form.get('FII_desejado')
        #framework = request.form.get('framework')
        return redirect(f'https://www.fundsexplorer.com.br/funds/{FII_desejado}')
    return render_template('index.html')

       
if __name__  == "__main__":
    app.run(debug= True, host= "0.0.0.0", port=5001) 
```    

- DockerFile para a criação do Build da aplicação
```
FROM  python:3.9.5

RUN apt-get update -y && \
  apt-get install -y python-pip python-dev

COPY . /app

RUN pip install flask

WORKDIR /app

EXPOSE 5001

CMD ["python","app-fii.py"]
```

- Verificando a image criada localmente no DockerHub  
  
  ![alt text](https://github.com/GumaFernando/proj-flask-k8s/blob/master/evidencias/1%20-%20verificando%20image%20local.png)
  
- Verificando a image após realizar o push da aplicação para o Azure ACR - ( Azure container registry)

![alt text](https://github.com/GumaFernando/proj-flask-k8s/blob/master/evidencias/verificando%20ACR.png)

- Verificando o Cluster Kubernetes criado para o deploy da aplicação

![alt text](https://github.com/GumaFernando/proj-flask-k8s/blob/master/evidencias/cluster%20k8s.PNG)


- Criando o script para a criação do namespace no kubernetes 
```
apiVersion: v1
kind: Namespace
metadata:
  name: ns-fii
```


- Criando o script para a criação do ***deploy*** e dos ***serviços**** no cluster
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask
  namespace: ns-fii
spec:
  replicas: 2
  selector:
    matchLabels:
      app: flask
  template:
    metadata:
      labels:
        app: flask
    spec:
      containers:
      - name: flask
        image: gumacr.azurecr.io/fii-flask:v08
        imagePullPolicy: Always
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 250m
            memory: 256Mi
        ports:
        - containerPort: 5001
          name: flask
---
apiVersion: v1
kind: Service
metadata:
  name: flask
  namespace: ns-fii
spec:
  type: LoadBalancer
  loadBalancerIP: 20.124.43.86
  ports:
  - port: 5001
    nodePort: 30030
    targetPort: 5001
  selector:
    app: flask
```


- Criando o Namespace -> 'ns-fii'   no cluster K8S

![alt text](https://github.com/GumaFernando/proj-flask-k8s/blob/master/evidencias/criando_ns.PNG)

- Criando o deploy e o serviço no cluster K8S.
OBS: Nesta etapa conseguimos identificar os objetos existentes (PODS,DEPLOY,SERVICES,REPLICASETs) e seus devidos status no namespace criado.

![alt text](https://github.com/GumaFernando/proj-flask-k8s/blob/master/evidencias/criando_deploy_services.PNG)

- Acessando a aplicação através do IP EXTERNO de acesso.

![alt text](https://github.com/GumaFernando/proj-flask-k8s/blob/master/evidencias/acessando_app.PNG)


- Testando a aplicação - Mostrando o redirecionando de página para o site do fundsexplorer.

![alt text](https://github.com/GumaFernando/proj-flask-k8s/blob/master/evidencias/teste-app-funds.PNG)




