# Shopee
## Project Structure
```
shopee
├─ config/
│  ├─ keyword.env.sample
├─ data/
├─ scripts/
│  ├─ keyword_crontab
├─ services/
│  ├─ keyword_service/
│  │  ├─ module
│  │  │  ├─ __init__.py
│  │  │  └─ google_spreadsheets_module.py
│  │  ├─ utils/
│  │  │  ├─ __init__.py
│  │  │  └─ mongo.py
│  │  ├─ Dockerfile
│  │  ├─ main.py
│  │  ├─ README.md
│  │  └─ requirements.txt
├─ .gitattributes
├─ .gitignore
├─ docker-compose.yml
├─ Makefile
└─ README.md
```
---
## How To Use
- build image
    ```
    make build
    ```
- start container
    ```
    make up
    ```
- stop container
    ```
    make down
    ```
- enter container
    ```
    make bash service={container_name}
    ```
  container_name :
  - keyword-service 
---