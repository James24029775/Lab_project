FROM golang:1.19
ADD . /webui/
WORKDIR "/webui"
VOLUME /home/james/Lab_project/webui

# CMD ["./compile_frontend.sh"]
CMD ["sh", "-c", "go run server.go"]