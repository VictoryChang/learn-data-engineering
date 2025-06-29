# learn-data-engineering

## Motivation
The purpose of this project is to learn how to do data engineering using modern open-source data engineer tools.


### Sources

<details open>
<summary>MongoDB</summary>

* Docker: 
docker run --name mongodb -p 27017:27017 -d mongodb/mongodb-community-server:latest

* UI: MongoDB Compass

* CLI: mongosh "mongodb://localhost:27017"

* Inserting Sample Data
  * use mongodb_demo
  * db.createCollection("users")
  * db.users.insertOne({name: "jonathan", age: 27, job: "architect"})
  * db.users.insertMany([{name: "Emily", age: 30, job: "electrician"}, {name: "Marco", age: 30, job: "biologist"}])
* Finding Data
  * db.users.find()
</details>


<details open>
<summary>Postgres</summary>

* Docker: docker run --name some-postgres -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword -d postgres

* UI: dbeaver

* CLI: psql -h localhost -p 5432 -d postgres -U postgres
* Inserting Sample Data

```
postgres=# \c postgres_demo;

postgres=# CREATE TABLE users (
  name  varchar(80),
  age   int,
  job   varchar(80)
);

postgres=# INSERT INTO users(name, age, job)
VALUES('Anthony', 36, 'plumber');

postgres=# INSERT INTO users(name, age, job)
VALUES
  ('Cynthia', 25, 'estate agent'),
  ('julian', 36, 'dog walker');

postgres=# SELECT * FROM users;
```
</details>


<details open>
<summary>API</summary>

* Python Environment Manager
    * brew install pyenv
    * pyenv install -l (list all available versions)
    * pyenv install 3.13.3 (latest stable version at this time)
    * pyenv global 3.13.3 (use everywhere)

* Code
```
from pathlib import Path
import os

from dotenv import load_dotenv
import requests


def users():
    headers = {"x-api-key": os.environ["REQRES_API_KEY"]}
    response = requests.get("https://reqres.in/api/users?page=2", headers=headers)
    assert response.status_code == 200
    return response.json()["data"]


if __name__ == "__main__":
    load_dotenv(Path("~/.env").expanduser())
    print(users())
```
</details>


<details open>
<summary>CSV</summary>


* Code
```
pandas_df = pd.read_csv("src/etl_tutorial/defs/data/csv_demo.csv")

```
</details>
