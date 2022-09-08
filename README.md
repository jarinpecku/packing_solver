# packing_solver
Shipmonk testing day


# Run

The easiest way to play with the project is:

```shell
$ docker-compose up
```

### Unit tests - Run

Enter the `test/unit` directory and simply run pytest by command:
```shell
$ py.test
```

### Integration tests - Run

Run the containers in background by command:
```shell
$ docker-compose up -d
```
Then enter the `test/integration` directory and simply run pytest by command:
```shell
$ py.test
```
When you are done with the tests stop the application containers by command:
```shell
$ docker-compose down
```
