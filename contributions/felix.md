I generated a pair of a private key and a public certificate and made changes in `client` so it was possible to connect through TLS. Made a copy of the original `docker-compose` and added pointers to the location of the certificate, both for the client and the server, and named it `docker-compose.tls`. Also made a copy of `docker-compose.attack`, added an environment flag so it is possible to run the baseline and TLS without needing to switch branches, and named it `docker-compose.attack-tls`. 

With the environment flag that was added, it was also used in `legit-server`, so the server would either run on port 443 with the generated certificate and HTTPS instead of our baseline on HTTP and 8080. 

`Openssl` was used to create the certificate for the implementation of TLS between the client and the server. 
The following commands were used:
`openssl req -x509 -noenc -days 365 -newkey rsa:2048 \
  -keyout certs/server.key \
  -out certs/server.crt \
  -subj "/CN=agent.invoice.test" \
  -addext "subjectAltName=DNS:agent.invoice.test,DNS:legit-server"  `
- x509, to generate a certificate instead of a request
- noenc, no password protection on the private key
- days 365, how long it is valid for
- newkey rsa:2048, the encryption method
- keyout, location to store the private key
- out, location to store the certificate
- subj, domain name for the certificate
- addext, also shows the domain name, but in a way that Python requests can read it

