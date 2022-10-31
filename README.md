# test-mlserver

### Install dependencies
``` bash
poetry install
```

### Run app
``` bash
poetry run app-start
```


### Run load test
- [Install k6](https://k6.io/docs/es/empezando/instalacion/)
- Execute the following test scenarios

Rest tests
```bash
k6 run --vus 100 --duration 30s benchmarking/load-tests/scenarios/k6/rest_df.js
```

```bash
k6 run --vus 100 --duration 30s benchmarking/load-tests/scenarios/k6/rest_base64.js
```

Grpc tests
```bash
k6 run --vus 100 --duration 30s benchmarking/load-tests/scenarios/k6/grpc_df.js
```

```bash
k6 run --vus 100 --duration 30s benchmarking/load-tests/scenarios/k6/grpc_base64.js
```

