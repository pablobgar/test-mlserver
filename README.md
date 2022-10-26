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
- Install k6
- Execute `test-mlserver/benchmarking/load-tests/scenarios/k6/rest_df.js`
- Execute `test-mlserver/benchmarking/load-tests/scenarios/k6/rest_base64.js`

```bash
k6 run --vus 100 --duration 30s scenarios/k6/rest_df.js
```

```bash
k6 run --vus 100 --duration 30s scenarios/k6/rest_base64.js
```
