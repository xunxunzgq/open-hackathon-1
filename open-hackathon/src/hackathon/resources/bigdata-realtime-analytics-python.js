{
    "expr_name": "jstrom hackathon_python",
    "virtual_environments": [
        {
            "provider": "docker",
            "name": "web",
            "image": "msopentechcn/flask",
            "ports":[{
                "name": "website",
                "port": 5000,
                "host_port": 80,
                "public": true
            },{
                "name": "Deploy",
                "port": 22
            }],
            "mnt2":["%s/src","/src"],
            "mnt": ["/home/opentech/github/flask-example/src", "/src"],
            "AttachStdin":false,
            "AttachStdout":true,
            "AttachStderr":true,
            "remote": {
                "provider": "guacamole",
                "protocol": "ssh",
                "username": "root",
                "password": "root",
                "port": 22
            }
        },
        {
            "pri":"avm"
            "cloud-service":{},
            "deployment":{}
        },
        {
            "provider": "docker",
            "name": "vnc",
            "image": "sffamily/ubuntu-gnome-vnc-eclipse",
            "ports":[{
                "name": "Dev",
                "port": 5901
            }],
            "AttachStdin":false,
            "AttachStdout":true,
            "AttachStderr":true,
            "tty": true,
            "stdin_open": true,
            "remote": {
                "provider": "guacamole",
                "protocol": "vnc",
                "username": "root",
                "password": "acoman",
                "port": 5901
            }
        }
    ]
}