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
# create cloned devices based on an existing device using REST APIs
# step 1: Change lines 22-30
# step 2: Execute the script
#################################################################################################

import urllib.request, urllib, urllib.parse
from base64 import b64encode
import simplejson as json

D42_URL = 'https://IP'  # your_d42_fqdn_or_ip  #no / in the end
D42_USERNAME = 'user'  # your_d42_username_here
D42_PASSWORD = 'password'  # your_d42_password_here
DEBUG = True  # True or False. True for detailed info
ORIGINAL_DEVICE_NAME = 'server01'
NEW_DEVICE_NAMES = ['server02', 'server02', ]  # Leave last , even if a single name
CLONE_HARDWARE = True
CLONE_OS = True
CLONE_CPU_RAM = True

d42_get_device_url = D42_URL + '/api/1.0/device/name/' + ORIGINAL_DEVICE_NAME + '/'
d42_add_device_url = D42_URL + '/api/device/'


def post(params):
    data = urllib.parse.urlencode(params).encode('utf-8')
    headers = {
        'Authorization': 'Basic ' + b64encode((D42_USERNAME + ':' + D42_PASSWORD).encode('utf-8')).decode('utf-8'),
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    req = urllib.request.Request(d42_add_device_url, data, headers)
    if DEBUG: print('---REQUEST--- %s' % req.get_full_url())
    if DEBUG: print(req.headers)
    if DEBUG: print(req.data)
    try:
        urllib.request.urlopen(req)
        return True, ''
    except urllib.request.HTTPError as e:
        error_response = e.read()
        if DEBUG:
            print("%s %s" % (e.code, error_response))
        return False, error_response


notadded = []
added = []

request = urllib.request.Request(d42_get_device_url)
request.add_header('Authorization', 'Basic ' + b64encode((D42_USERNAME + ':' + D42_PASSWORD).encode('utf-8')).decode('utf-8'))
try:
    r = urllib.request.urlopen(request)
    if r.getcode() == 200:
        obj = r.read()
        device_to_be_cloned = json.loads(obj)
        if device_to_be_cloned == "device not found":
            print('Device not found')
            exit()
        for new_device in NEW_DEVICE_NAMES:
            devargs = {'name': new_device, 'type': device_to_be_cloned['type'],
                       'service_level': device_to_be_cloned['service_level']}
            if CLONE_HARDWARE and device_to_be_cloned['hw_model']:
                devargs.update({'hardware': device_to_be_cloned['hw_model']})
                if device_to_be_cloned['manufacturer']: devargs.update(
                    {'manufacturer': device_to_be_cloned['manufacturer']})
            if CLONE_OS and device_to_be_cloned['os']:
                devargs.update({'os': device_to_be_cloned['os']})
                if 'osver' in device_to_be_cloned: devargs.update({'osver': device_to_be_cloned['osver']})
                if 'osverno' in device_to_be_cloned: devargs.update({'osverno': device_to_be_cloned['osverno']})
            if CLONE_CPU_RAM:
                if 'cpucount' in device_to_be_cloned:
                    devargs.update({'cpucount': device_to_be_cloned['cpucount']})
                    if 'cpucore' in device_to_be_cloned: devargs.update({'cpucore': device_to_be_cloned['cpucore']})
                    if 'cpuspeed' in device_to_be_cloned and device_to_be_cloned['cpuspeed'] is not None:
                        devargs.update(
                        {'cpupower': int(device_to_be_cloned['cpuspeed'])})
                if 'ram' in device_to_be_cloned:
                    devargs.update({'memory': device_to_be_cloned['ram']})
            if DEBUG: print('Device Arguments: %s' % str(devargs))
            try:
                ADDED, msg = post(devargs)
                if ADDED:
                    added.append(new_device)
                else:
                    notadded.append([new_device + ' ' + msg])
            except Exception as Err:
                notadded.append([new_device + str(Err)])
        print('notadded %s' % notadded)
        print('added %s' % added)
    else:
        print('Exiting, HTTP return code: %s' % str(r.getcode()))
except Exception as s:
    print('Exception: %s ' % str(s))
