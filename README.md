# Teleinsight 

![teleinsight_new.gif](docs/teleinsight_new.gif)



### You can autorize into telegram using this script!    
[get_session_string.py](drafts/get_session_string.py)


### Main ingesting parts
#### Handle any new update from telegram ( using SESSION_STRING which we get above )   
[new_messages_handler.py](ingestor/new_messages_handler.py)    

#### Old message dump mechanism        
[old_messages_handler.py](ingestor/old_messages_handler.py)

```shell
├── Dockerfile.embedder
├── Dockerfile.ingestor
├── README.md
├── cloud_functions
│        # Cloud function which receive image description, 
│        # get text embeddings and insert to Clickhouse
│   └── visioneer 
│       ├── main.py
│       ├── requirements.txt
│       └── tools
├── docker-compose.yaml
├── drafts
│   ├── examples
        # Example of received telegram events
│   │   ├── channel_message.json
│   │   ├── chat_message.json
│   │   └── user_message.json
│         # Simple script to get active user token
│   ├── get_session_string.py
│   └── text-embedding.ipynb
│ # Service which use Clip model to get image embeddings 
├── embedder
│   ├── __init__.py
│   ├── certificates
│   │   └── YandexInternalRootCA.crt
│   ├── clip.py
│   ├── config.py
│   ├── main.py
│   ├── requirements.txt
│   └── storage.py
│ # Service to get real time update and old message as well
├── ingestor
│   ├── __init__.py
│   ├── config.py
│   ├── db
│   │   ├── __init__.py
│   │   └── handler.py
│   ├── new_messages_handler.py
│   ├── old_messages_handler.py
│   ├── requirements.txt
│   ├── storage
│   │   ├── __init__.py
│   │   └── objects.py
│   └── utils
│       ├── __init__.py
│       ├── events.py
│       └── meta.py
├── poetry.lock
├── pyproject.toml
│ # Simple and pretty stupid API and frontend page to search thru attachments
└── web
    ├── api
    │   ├── example.csv
    │   └── main.py
    ├── index.html
    ├── script.js
    └── styles.css

```
