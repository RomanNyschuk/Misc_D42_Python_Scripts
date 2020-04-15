"""
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

#################################################################################################
# create device reports in CSV format using device42 APIs
# step 1: Change lines 22-25 and then 35 & 37
# step 2: Execute the script
#################################################################################################

import requests
from requests.exceptions import RequestException
from requests.auth import HTTPBasicAuth
import csv

D42_URL = 'https://IP'  # your_d42_fqdn_or_ip
D42_USERNAME = 'USER'  # your_d42_username_here
D42_PASSWORD = 'PASS'  # your_d42_password_here
CSV_FILE_NAME = 'device_report.csv'  # csv file name

d42_get_devices_url = D42_URL + '/api/1.0/devices/all/'

try:
    r = requests.get(d42_get_devices_url, auth=HTTPBasicAuth(D42_USERNAME, D42_PASSWORD))
    if r.status_code == 200:
        devices_data = r.json()

        f = csv.writer(open(CSV_FILE_NAME, "w+"))
        f.writerow(['Name', 'CPU Count', 'Cores', 'CPU Speed', 'Memory', 'Hardware'])
        for device in devices_data['Devices']:
            f.writerow([device['name'], device['cpucore'], device['cpucount'], device['cpuspeed'], device['ram'],
                        device['hw_model'], device['os']])
    else:
        print('Exiting, HTTP return code: %s' % str(r.status_code))
except RequestException as s:
    print(str(s))
