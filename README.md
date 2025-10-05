# the Project is technical test for papernest

.

I have a CSV who contains coverage mobile in lambert data. And i must call Api gouv to retrieve coordonates and verifiy with a specific circonference the coverage 2G : 30km, 3G : 5km,4G : 10km, if it's true or wrong.




## 🛠️ Install Dependencies

1. If not already done, install Docker Compose (v2.10+)

🧰 Bash Automation Script

The project includes a helper script to simplify developer tasks (running, generating reports, etc.).

2. Run the script bash and write flag help: 
```bash :
bash script.sh help
```
You have got multiple option if you want run all write :
```bash
bash script.sh all# The Project is a technical test for papernest.

I have a CSV who contains coverage mobile in lambert data. And i must call Api gouv to retrieve coordonates and verifiy with a specific circonference the coverage 2G : 30km, 3G : 5km,4G : 10km, if it's true or wrong.




## 🛠️ Install Dependencies

1. If not already done, install Docker Compose (v2.10+)

🧰 Bash Automation Script

The project includes a helper script to simplify developer tasks (running, generating reports, etc.).

2. Run the script bash and write flag help: 
```bash :
bash script.sh help
```
You have got multiple option if you want all run :
```bash
bash script.sh all
```
Or if you want run rapport about coverage :

```bash
bash script.sh coverage
```

### Expected Ports

8000 → FastAPI or 8000/docs to look swagger

4200 → Angular 

9090 → Prometheus to check graph


### ⚙️ Technology Stack

| Layer                | Technology                           | Description                                             |
| -------------------- | ------------------------------------ | ------------------------------------------------------- |
| **Frontend**         | Angular                        | Dynamic UI for job submission and results visualization |
| **Backend**          | FastAPI                              | REST API for asynchronous data processing               |
| **Database**         | SQLite (local)  | Stores job metadata and performance metrics             |
| **Metrics**          | Prometheus                           | Collects job timings and API metrics                    |
| **HTTP Client**      | httpx                                | Async requests to external services                     |
| **ORM**              | SQLAlchemy                           | Database abstraction                                    |
| **Tests**            | pytest, pytest-cov                   | Unit and integration testing                          
| **Containerization** | Docker + docker-compose              | Reproducible local development


## 💻 curl Examples
Check API health

```

curl -X GET http://localhost:8000/ping

```


##### Submit Job 

you have swagger please check this url 

`http://localhost:8000/docs`

or you have collection postman to execute schedule runs

Example : 

```
curl -X POST http://localhost:8000/job-submission \
     -H "Content-Type: application/json" \
     -d '{
           "root": {
             "addr1": "place des ramacles Aubiere",
           }
         }'

```

##### Response :

```
{
    "jobsUUID": "f2df5a99-f1ea-4c1e-9a2f-bc4dab706c14",
    "jobs": {
        "id1": {
            "Orange": {
                "2G": true,
                "3G": true,
                "4G": true
            },
            "SFR": {
                "2G": true,
                "3G": true,
                "4G": true
            },
            "Bouygues": {
                "2G": true,
                "3G": true,
                "4G": true
            }
        }
    }
}
```



## 📈 queries prometheus example 

You can add this queries to look on the dashboard's graph in Prometheus


### Prometheus screen

![Cover](https://github.com/Haroun-Azoulay/papernest/blob/master/img/img-prometheus.png)

### Error rate in % over the last day.
```
100 * sum(rate(job_requests_total{result="error"}[1d]))
  / sum(rate(job_requests_total[1d]))
```

### Items processed per second over the last 5 minutes.
```
sum(rate(job_items_processed_total[5m]))
 ```
### Total all job requests
```
job_requests_total
```
### RPS over 5 minutes
```
sum(rate(job_requests_total[5m]))
```

## ✅ You can run the postman collection to run the collection manually

### Postman screen

![Cover](https://github.com/Haroun-Azoulay/papernest/blob/master/img/img-postman_collection.png)
