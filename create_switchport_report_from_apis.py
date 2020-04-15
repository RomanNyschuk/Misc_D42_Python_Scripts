'''
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

#################################################################################################
# create switch ports reports in CSV format using device42 APIs
# step 1: Change lines 22-25
# step 2: Execute the script
#################################################################################################

import urllib.request
from base64 import b64encode
import simplejson as json
import csv

D42_URL = 'https://IP'  # your_d42_fqdn_or_ip
D42_USERNAME = 'USER'  # your_d42_username_here
D42_PASSWORD = 'PASS'  # your_d42_password_here
CSV_FILE_NAME = 'switchports_report.csv'  # csv file name

d42_get_switchports_url = D42_URL + '/api/1.0/switchports/'
request = urllib.request.Request(d42_get_switchports_url)
request.add_header('Authorization',
                   'Basic ' + b64encode((D42_USERNAME + ':' + D42_PASSWORD).encode('utf-8')).decode('utf-8'))

try:
    r = urllib.request.urlopen(request)
    obj = r.read()
    switchportdata = json.loads(obj.decode('utf-8'))

    f = csv.writer(open(CSV_FILE_NAME, "w+"))
    f.writerow(['Description', 'Port Name', 'MAC Addresses', 'Devices'])
    value = switchportdata['switchports']
    for i in value:
        f.writerow([i['description'], i['port'], i['hwaddress'], i['devices']])

except Exception as s:
    print(str(s))
