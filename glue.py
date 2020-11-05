from flask import Flask
from flask import request
import logging
from datetime import datetime
from flask import jsonify
import os

import requests

app = Flask(__name__)

SIGNAL_URL = os.getenv("SIGNAL_URL", "http://127.0.0.1:8080/v1/send")
SIGNAL_RECEIPIENTS = os.getenv("SIGNAL_RECEIPIENTS", "+000000000").split(",")
SIGNAL_NUMBER = os.getenv("SIGNAL_NUMBER", "+000000")

def send_alerts(alerts):
    """Translates Prometheus alerts to a signal message
    
    Arguments:
        alerts {dict} -- Prometheus Alertmanager webhook
    """

    for a in alerts["alerts"]:
        message = "Status: " + a['status'] + "\n" + \
          "Severity: " + a['labels']['severity'] + "\n" + \
          "Alertname: " + a['labels']['alertname'] + "\n" + \
          "Start: " + a['startsAt'] + "\n" + \
          "End: " + a['endsAt'] + "\n" + \
          "Hostgroup: " + a['labels']['group'] + "\n" + \
          "Host: " + a['labels']['instance'] + "\n" + \
          "Summary: " + a['annotations']['summary'] + "\n" + \
          "Description: " + a['annotations']['description']

        send_message(message, SIGNAL_NUMBER, recipients=SIGNAL_RECEIPIENTS)


def send_message(message, number, recipients=[]):
    """Sends a (preformatted) message using signal rest cli
    
    Arguments:
        message {str} -- Message to send
        number {str} -- Number to send message from
    
    Keyword Arguments:
        recipients {list} -- List of recipients (default: {[]})
    """
    response = requests.post(
        SIGNAL_URL,
        json={"message": message, "number": number, "recipients": recipients},
        timeout=5,
    )


@app.route("/alerts", methods=["POST"])
def alerts():
    """Receive alerts from alertmanager, translate and forward to signal-cli-rest
    """
    try:
        if request.method == "POST":
            content = request.json
            send_alerts(content)
            # Send the message
    except Exception as e:
        app.logger.error("Unable to send message to signal %s", e)
        return "Error sending alerts to signal, check logs of prometheus-signal-glue", 500

    return "Alerts delivered to signal", 200


def main():
    port = os.environ.get("PORT", 5000)
    host = os.environ.get("HOST", "0.0.0.0")
    app.run(host=host, port=port)


if __name__ == "__main__":
    main()
