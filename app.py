#!./bin/python
from waitress import serve
from flask import Flask, jsonify, request
from flask.json import JSONEncoder
from os import environ
from datetime import datetime, date
import time
import boto3

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, date):
                return obj.timestamp()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)

app = Flask(__name__)
app.json_encoder = CustomJSONEncoder

@app.route('/getMetrics', methods = ['POST'])
def metrics():
    try:
        auth_token = request.headers.get('x-metrics-token')
        aws_region = request.headers.get('x-metrics-region')
        start_time = request.args.get("start")
        end_time = request.args.get("end")
        data = request.json
        cloudwatch = boto3.client('cloudwatch', region_name=aws_region)
        metricData =  cloudwatch.get_metric_data(

        MetricDataQueries=[
             data,
        ],
            StartTime=start_time,
            EndTime=end_time,
    )
        return jsonify(metricData)

    except Exception as e:
        raise


@app.route('/getLogs', methods = ['POST'])
def logs():
    try:
        auth_token = request.headers.get('x-metrics-token')
        aws_region = request.headers.get('x-metrics-region')
        start_time = int(request.args.get("start"))
        end_time = int(request.args.get("end"))
        data = request.json

        #query = "fields @timestamp, log, kubernetes.pod_name | filter kubernetes.pod_name = 'kubernetes-dashboard-57df4db6b-rb9dz'"
        #query= "fields @timestamp, log, kubernetes.pod_name | filter kubernetes.pod_name = 'cart-7d5f5fbf46-zb6j6'"
        query = data['customLogs']['query']
        #log_group = '/eks/clustername/containers'
        log_group = data['customLogs']['log_group']

        cloudwatch = boto3.client('logs', region_name=aws_region)

        start_query_results = cloudwatch.start_query(
            logGroupName=log_group,
            startTime=start_time,
            endTime=end_time,
            queryString=query,
            )

        query_id = start_query_results['queryId']

        results = None

        while results == None or results['status'] == 'Running':
            print('Query not ready, will try again ...')
            time.sleep(1)
            results = cloudwatch.get_query_results(
                queryId=query_id
            )

        return jsonify(results)

    except Exception as e:
        raise


@app.route('/health', methods = ['GET'])
def healthCheck():

    return "{\"status\": \"UP\"}"

if __name__ == '__main__':
    #app.run(debug=False)
    serve(app, host='0.0.0.0', port=5000)
