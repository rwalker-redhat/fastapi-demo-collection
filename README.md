# fastapi-demo-collection
Collection of APIs for PoC and demos. 

# Quickstart

```commandline
git clone https://github.com/rwalker-redhat/fastapi-demo-collection.git
cd fastapi-demo-collection
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirments.txt
```


## sqlite3


```commandline
.mode column
select * from cartoon_characters;
delete from cartoon_characters where id = 3;
.quit
```

```commandline
.mode column
select * from users;
delete from users where id = 2;
.quit
```


# project-disney-auth

Simple CRUD APIs with user token Authentication using TLS.

## Usage

Visit [https://localhost/api/docs](https://localhost/api/docs)
Get a user token from `/api/users/token` using:

username: jdoe 
password: changeme


```commandline
curl --location --request GET 'https://localhost/api/disney/users' --header 'Authorization: Bearer <TOKEN>' --cacert local_ca.pem
```


## Certificate

Local CA and application certificate generation for development and testing:

```commandline
openssl genrsa -des3 -out local_ca.key 2048
openssl req -x509 -new -nodes -key local_ca.key -sha256 -days 1825 -out local_ca.pem
openssl x509 -in local_ca.pem -text
```

```commandline
openssl genrsa -out cluster.lab.com.key 2048
```

```commandline
openssl genrsa -out localhost.key 2048
openssl req -new -key localhost.key -out localhost.csr
vi cluster.lab.com.ext
```

```text
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
subjectAltName = @alt_names

[alt_names]
DNS.1 = 127.0.0.1
DNS.2 = exampleforyou.net
```

```commandline
openssl x509 -req -in localhost.csr -CA local_ca.pem -CAkey local_ca.key -CAcreateserial -out localhost.crt -days 825 -sha256 -extfile localhost.ext
cat local_ca.pem >> localhost.crt
```
