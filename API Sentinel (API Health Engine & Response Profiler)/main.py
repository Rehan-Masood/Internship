import json
import os
import time
from datetime import datetime
import requests


class APISentinel:

  def __init__(self, log_file='api_metrics.json'):
    self.log_file = log_file

  def test_endpoint(
      self, url, method='GET', payload=None, headers=None, timeout=5
  ):
    """Executes an HTTP request and measures status, latency, and payload size."""
    headers = headers or {'User-Agent': 'APISentinel/1.0'}
    start_time = time.perf_counter()

    try:
      response = requests.request(
          method=method,
          url=url,
          json=payload,
          headers=headers,
          timeout=timeout,
      )
      elapsed_ms = (time.perf_counter() - start_time) * 1000

      metrics = {
          'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
          'url': url,
          'method': method.upper(),
          'status_code': response.status_code,
          'success': response.ok,
          'response_time_ms': round(elapsed_ms, 2),
          'payload_size_kb': round(len(response.content) / 1024, 3),
          'error': None,
      }

      # Try parsing response payload
      try:
        metrics['response_data'] = response.json()
      except ValueError:
        metrics['response_data'] = response.text[:200]  # First 200 chars

      return metrics

    except requests.exceptions.Timeout:
      return self._build_error_metric(url, method, 'Connection Timeout (>5s)')
    except requests.exceptions.ConnectionError:
      return self._build_error_metric(
          url, method, 'Failed to connect to host'
      )
    except requests.exceptions.RequestException as e:
      return self._build_error_metric(url, method, str(e))

  def _build_error_metric(self, url, method, error_msg):
    return {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'url': url,
        'method': method.upper(),
        'status_code': None,
        'success': False,
        'response_time_ms': 0,
        'payload_size_kb': 0,
        'error': error_msg,
        'response_data': None,
    }

  def log_metrics(self, metrics_list):
    """Saves API health audit report to JSON."""
    with open(self.log_file, 'w') as f:
      json.dump(metrics_list, f, indent=4)
    print(f'\n💾 Health report saved to {self.log_file}')


def main():
  print('====================================================')
  print('⚡ API SENTINEL — HTTP Requests & API Profiler')
  print('====================================================\n')

  sentinel = APISentinel()

  # Public REST APIs to benchmark
  endpoints_to_test = [
      {
          'url': 'https://jsonplaceholder.typicode.com/posts/1',
          'method': 'GET',
      },
      {
          'url': 'https://jsonplaceholder.typicode.com/posts',
          'method': 'POST',
          'payload': {
              'title': 'API Sentinel Test',
              'body': 'Benchmarking HTTP POST',
              'userId': 1,
          },
      },
      {
          'url': 'https://httpbin.org/delay/1',
          'method': 'GET',
      },  # Latency test
      {
          'url': 'https://httpbin.org/status/404',
          'method': 'GET',
      },  # 404 Error test
      {
          'url': 'https://invalid-non-existent-domain-123.com',
          'method': 'GET',
      },  # Invalid domain test
  ]

  audit_results = []

  for item in endpoints_to_test:
    print(f"📡 Testing [{item['method']}] {item['url']} ...")
    result = sentinel.test_endpoint(
        url=item['url'],
        method=item['method'],
        payload=item.get('payload'),
    )

    if result['success']:
      print(
          f"   ✅ {result['status_code']} OK | Time:"
          f" {result['response_time_ms']} ms | Size:"
          f" {result['payload_size_kb']} KB"
      )
    else:
      print(
          f"   ❌ FAILED | Status: {result['status_code']} | Error:"
          f" {result['error']}"
      )

    audit_results.append(result)
    print('-' * 52)

  # Export metrics
  sentinel.log_metrics(audit_results)


if __name__ == '__main__':
  main()