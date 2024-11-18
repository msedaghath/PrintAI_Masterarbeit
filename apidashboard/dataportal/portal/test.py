from octorest import OctoRest
import requests

class CustomOctoRest(OctoRest):
    def new_method(self, path):
        response = self.session.get(self.url + path)
        return self._check_response(response)

# Create an instance of the CustomOctoRest client1997   
client = CustomOctoRest(url="http://127.0.0.1:5000", apikey="18CDBE4D7907479E84B9C293C3B0CBBC")

# Use the client to send a GET request to a custom endpoint
try:

    # gcode_file =   # Get the uploaded file
    # if gcode_file:
    #     try:
    #         client.upload(gcode_file.name, gcode_file.read())  # Upload the file to OctoPrint
    #     except Exception as e:
    #         print(e)
    # response = client.new_method('/api/job')
    # post conetent to the endpoint
    # try : 
    #     print('upload')
    #     client.upload
    # except Exception as e:
    #     print(f"An error occurred: {e}")
    # print(f"Response: {response}")
    # response_content = response.json()
    # print(response_content)

    # import requests

    # url = "http://your-printer-ip/api/printer/printhead"
    # headers = {"X-Api-Key": "your-api-key"}
    # data = {"command": "home", "axes": ["x", "y"]}

    # response = requests.post(url, headers=headers, json=data)

    pass
except Exception as e:
    print(e)
    
import os
import tempfile
from octorest import OctoRest

def upload_file_to_octoprint(file_path, url, api_key):
    client = OctoRest(url=url, apikey=api_key)
    
    with open(file_path, 'rb') as file:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(file.read())
            tmp.flush()  # Make sure all data is written to disk
        print(tmp.name)
        client.upload(file=tmp.name, select=True)
        os.unlink(tmp.name)  # delete the temporary


upload_file_to_octoprint(
    file_path='apidashboard/dataportal/portal/test.gcode',
    url="http://127.0.0.1:5000",
    api_key="18CDBE4D7907479E84B9C293C3B0CBBC"
)