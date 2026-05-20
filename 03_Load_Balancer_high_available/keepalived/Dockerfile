FROM alpine:latest
RUN apk add --no-cache keepalived
ENTRYPOINT ["keepalived", "-n", "-l", "-D"]
