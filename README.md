# Network Manager API

We are currently facing a technological boom, changing the way in how networks are being deployed and managed, due to evolution towards network automation, as well as all kinds of services and systems migration to the cloud, giving rise to hybrid environments (cloud and on-premise), where we find both physical and virtual network elements from different vendors.

This revolution brings the spawning of many tools, as well as work methodologies, which have changed the traditional network administrator role aka ClickOps, towards NetDevOps engineer, needing a high technical knowledge degree and continuous learning.

In order to simplify this landscape and ease network tasks, this project aims to develop a REST API in Python programming language, allowing to manage network elements multi-vendor and multi-environment (cloud and on-premise).



## Documentation and specifications

You can check API documentation [here](https://documenter.getpostman.com/view/18346026/2s9YeEcs15)

### Pre-requisites

You need to configure [mongoDB](https://www.mongodb.com/es/cloud/atlas/lp/try4) instance, and edit url value in the configuration file

tenant/config_files/config_db.yaml

```yaml
db_connection:
  database: ACME
  url: mongodb+srv://<username>:<password>@networkmanager.my.mongodb.net/?retryWrites=true&w=majority
db_tenant:
  type: mongo_db_tenant
db_users:
  type: mongo_db_user
```



For security reasons, SECRET KEYS, must be changed.

generate_secret_key function, provide secret keys.

tenant/application/password_crypt.py

```python
class PasswordCrypt:

    def __init__(self):
        SECRET_KEY = b'SECRET'
        self.cipher = Fernet(SECRET_KEY)

    def encode_password(self, password: str):
        return self.cipher.encrypt(password.encode()).decode()

    def decode_password(self, encrypted_password: str) -> str:
        return self.cipher.decrypt(encrypted_password).decode()

    @staticmethod
    def generate_secret_key() -> str:
        return Fernet.generate_key().decode()
```



Also, you have to change the JWTAccessToken class properties, at least the secret key.

```python
class JWTAccessToken(IAccessToken):
    TOKEN_DURATION: int = 60*24*7
    ALGORITHM: str = "HS256"
    TOKEN_TYPE: str = "bearer"
    SECRET_KEY: str = "987423984321ad9432143c4312d43123f98372614986238765238748312afe9873a"
```



### Deploy

This program has been developed with FastAPI Framework. You can deploy this application following the intructions, avaiable on FastAPI official documentation https://fastapi.tiangolo.com/deployment/ 



Once, service is up: 

Endpoint to access the online documentation   `/docs` 

Endpoint to create organization and admin user  `/api/v1/organization`



![image-20231222153702050](/Users/dtorrejon/Library/Application Support/typora-user-images/image-20231222153702050.png)



![image-20231222153736486](/Users/dtorrejon/Library/Application Support/typora-user-images/image-20231222153736486.png)



Important: Before first access, you must be restart application service



![image-20231222155456898](/Users/dtorrejon/Library/Application Support/typora-user-images/image-20231222155456898.png)







