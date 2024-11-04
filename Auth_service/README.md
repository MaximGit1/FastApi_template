# Auth service

## The current directory should contain JWT keys. 

#### For example:
- certs/jwt-private.pem
- certs/jwt-public.pem


### How to generate keys

###### Generate an RSA private key, of size 2048
```Bash
openssl genrsa -out jwt-private.pem 2048
```

###### Generate an RSA public key,
```Bash
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
```
___