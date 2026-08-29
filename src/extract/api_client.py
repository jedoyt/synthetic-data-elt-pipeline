import json
import urllib.error
import urllib.request


class APIClient:
    def __init__(self, url_prefix: str):
        self.url_prefix = url_prefix

    def get(self, endpoint: str):
        url = self.url_prefix + endpoint
        return_output = {}
        try:
            with urllib.request.urlopen(url) as response:
                raw_data = response.read()
                data = json.loads(raw_data)
            # print(json.dumps(data, indent=4))
            # print(f"Returned datatype: {type(data)} | Status Code: {response.status}")
            return_output["http_status_code"] = response.status
            return_output["data"] = data
        except urllib.error.HTTPError as e:
            print(f"HTTP Error: {e.code} - {e.reason}")
            return_output["http_status_code"] = response.status
            return_output["data"] = None
            return_output["error_message"] = f"HTTP Error: {e.code} - {e.reason}"
        except urllib.error.URLError as e:
            print(f"Connection Error: {e.reason}")
            return_output["http_status_code"] = response.status
            return_output["data"] = None
            return_output["error_message"] = f"Connection Error: {e.reason}"
        # print(json.dumps(return_output, indent=4))
        return return_output

    def post(self, endpoint: str, form_data=None):
        if form_data is None:
            form_data = {}
        url = self.url_prefix + endpoint
        return_output = {}
        try:
            request = urllib.request.Request(url, data=form_data)
            with urllib.request.urlopen(request, form_data) as response:
                raw_data = response.read()
                data = json.loads(raw_data)
            print(json.dumps(data, indent=4))
            print(f"Returned datatype: {type(data)} | Status Code: {response.status}")
            return_output["http_status_code"] = response.status
            return_output["data"] = data
        except urllib.error.HTTPError as e:
            print(f"HTTP Error: {e.code} - {e.reason}")
            return_output["http_status_code"] = response.status
            return_output["data"] = None
            return_output["error_message"] = f"HTTP Error: {e.code} - {e.reason}"
        except urllib.error.URLError as e:
            print(f"Connection Error: {e.reason}")
            return_output["http_status_code"] = response.status
            return_output["data"] = None
            return_output["error_message"] = f"Connection Error: {e.reason}"
        # print(json.dumps(return_output, indent=4))
        return return_output


# Test APIClient
# if __name__ == "__main__":
#     URL_PREFIX = "http://127.0.0.1:8000"
#     client = APIClient(url_prefix=URL_PREFIX)

#     # Check API health
#     client.get("/health")

#     # Check number of initial sessions
#     client.get("/sessions/count")

#     # Test sessions/since/<timestamp>
#     timestamp = "2026-08-29 00:00:00"
#     formatted_ts = timestamp.replace(" ", "%20").replace(":", "%3A").replace("+", "%2B")
#     client.get(f"/sessions/since/{formatted_ts}")

#     # Test generation of additional sessions
#     additional_sessions = 10
#     client.post(f"/sessions/generate/{additional_sessions}")

#     # Check again final session counts
#     client.get("/sessions/count")
