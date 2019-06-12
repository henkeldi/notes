
# HTTPS

HTTPS = HTTP over Transport Layer Security (TLS)

TLS does two things:

* Encryption and Hashing

Hashing SHA256 (Number = size of hash in bits)

### TLS Handshake

* Step 1:

Server sends  Certificate with:

    a) Public Key
    
    b) Domain: google.com

    c) Authoritiy Signature (Browser knows the public key of Authority and can check if the signature is valid)

* Step 2:

Client generates random key and encrypts it with the servers public key and sends it to the server

* Step 3:

The server decrypts the random key and uses it for further communication

### Debug TLS Handshake:

```bash
openssl s_client -connect <ip>:443
```

### Useful links

* [Firesheep](https://codebutler.com/2010/10/24/firesheep/)
* [Bad SSL](https://badssl.com/)
