#!/bin/bash

CERT_DIR="certs"
mkdir -p $CERT_DIR

echo "Generating CA..."
openssl genrsa -out $CERT_DIR/ca.key 2048
openssl req -x509 -new -nodes -key $CERT_DIR/ca.key -sha256 -days 365 -out $CERT_DIR/ca.crt -subj "/CN=MyDemoCA"

generate_cert() {
    local name=$1
    local dns_name=$2
    echo "Generating certificate for $dns_name..."
    openssl genrsa -out $CERT_DIR/$name.key 2048
    openssl req -new -key $CERT_DIR/$name.key -out $CERT_DIR/$name.csr -subj "/CN=$dns_name"
    
    cat <<EOT > $CERT_DIR/$name.ext
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
subjectAltName = @alt_names

[alt_names]
DNS.1 = $dns_name
DNS.2 = localhost
IP.1 = 127.0.0.1
EOT

    openssl x509 -req -in $CERT_DIR/$name.csr -CA $CERT_DIR/ca.crt -CAkey $CERT_DIR/ca.key -CAcreateserial         -out $CERT_DIR/$name.crt -days 365 -sha256 -extfile $CERT_DIR/$name.ext
}

generate_cert "loadbalancer" "loadbalancer.tevs"
generate_cert "webserver1" "webserver1.tevs"
generate_cert "webserver2" "webserver2.tevs"

echo "Certificates generated in $CERT_DIR/"
