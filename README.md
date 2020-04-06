# Prometheus Signal glue

Small daemon that "glues" together Prometheus Alertmanager webhook messages with signal.org using [signal-cli-rest-api](https://github.com/bbernhard/signal-cli-rest-api). This project is intended as a proof of concept.

The docker directory contains a `docker-compose` file that can be used to setup a local alertmanager.

## Testing

Pytest is used for testing. Run test cases with

```shell
pytest test_glue.py
```

### Test webhook

Send a single alert.

```shell
curl -X POST -H "Content-Type: application/json" \
-d @fixtures/alerts.json \
'http://127.0.0.1:5000/alerts'
```

## Running

Set the following environment variables to configure signal. 

```env
SIGNAL_URL
SIGNAL_RECEIPIENTS
SIGNAL_NUMBER
```

Start the daemon

```shell
python glue.py
```
