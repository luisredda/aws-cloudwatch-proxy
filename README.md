# AWS Cloudwatch proxy

[![Build Status](https://cloud.drone.io/api/badges/luisredda/aws-cloudwatch-proxy/status.svg)](https://cloud.drone.io/luisredda/aws-cloudwatch-proxy)

A simple Python service to get Metrics and Logs from CloudWatch. It wraps get_metric_data method to fetch metrics and start_query to fetch logs. Great to use as a bridge in integrations or when it's not possible to customize your logic or implement the AWS API Authentication directly.

If you run the service inside a AWS instance it just assume the current IAM role, otherwise you can use the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables to define your credentials.

The region should be passed as a http header (x-metrics-region) and the start/end time as URL parameters using epoch time.

Example: 

*Fetch ELB Metrics:*

(POST) http://127.0.0.1:5000/getMetrics?start=${start_time_epoch_seconds}&end=${end_time_epoch_seconds}
(HTTP Header) x-metrics-region: us-east-1
 
Payload (the same standard from the AWS MetricStat object):
```json
{
            "Id": "m1",
            "MetricStat": {
                "Metric": {
                    "Namespace": "AWS/ApplicationELB",
                    "MetricName": "HTTPCode_Target_4XX_Count",
                    "Dimensions": [
                        {
                            "Name": "LoadBalancer",
                            "Value": "app/ami-demo/2g3g5f3e31dfe52fd2fdf3e2"
                        }
                    ]
                },
                "Period": 60,
                "Stat": "Average"
            }
        }
  ```
        
 *Fetch metrics with multiple dimensions:*
 
 (POST) http://127.0.0.1:5000/getMetrics?start=${start_time_epoch_seconds}&end=${end_time_epoch_seconds}
 (HTTP Header) x-metrics-region: us-east-1
 
 Payload (the same standard from the AWS MetricStat object):
 
 ```json
 {
      "Id": "m1",
      "MetricStat": {
        "Metric": {
          "Namespace": "/aws/sagemaker/Endpoints",
          "MetricName": "MemoryUtilization",
          "Dimensions": [
            {
              "Name": "EndpointName",
              "Value": "lr-endpoint"
            },
            {
              "Name": "VariantName",
              "Value": "AllTraffic"
            }
          ]
        },
        "Period": 60,
        "Stat": "Average"
      }
    }
```    
          
 *Fetch Logs from a specific EKS Pod:*

(POST)http://127.0.0.1:5000/getLogs?start=${start_time_epoch_seconds}&end=${end_time_epoch_seconds}
(HTTP Header) x-metrics-region: us-east-1

Payload (The query field represents a CloudWatch log insights query): 

```json
 {
  "customLogs": {
    "query": "fields @timestamp, msg, kubernetes.pod_name | filter kubernetes.pod_name = '${host}'",
    "log_group": "/eks/cluster-name/containers"
  }
}
```
 
    
