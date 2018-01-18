Python API for dnsdumpster.com [![Build Status](https://travis-ci.org/PaulSec/API-dnsdumpster.com.svg?branch=master)](https://travis-ci.org/PaulSec/API-dnsdumpster.com)
========


Usage
========

### Install with pip (from the Github repository): 

```shell
➜  ~ pip install https://github.com/PaulSec/API-dnsdumpster.com/archive/master.zip --user
Collecting https://github.com/PaulSec/API-dnsdumpster.com/archive/master.zip
  Downloading https://github.com/PaulSec/API-dnsdumpster.com/archive/master.zip
Installing collected packages: dnsdumpster
  Running setup.py install for dnsdumpster ... done
Successfully installed dnsdumpster-0.1
```

### Install with pip (from Pypi repository)


```shell
➜  ~ pip install dnsdumpster --user
Collecting dnsdumpster
  Using cached dnsdumpster-0.1.tar.gz
Installing collected packages: dnsdumpster
  Running setup.py install for dnsdumpster ... done
Successfully installed dnsdumpster-0.1
```

Then import the class and start playing:

```python
from dnsdumpster.DNSDumpsterAPI import DNSDumpsterAPI
results = DNSDumpsterAPI().search('microsoft.com')
```

### Install from the sources

Clone the repo

```shell
git clone https://github.com/PaulSec/API-dnsdumpster.com
```

Install requirements

```shell
pip install -r requirements.txt
```

Import the class:

```python
from dnsdumpster.DNSDumpsterAPI import DNSDumpsterAPI
```

Then, search for a specific domain:


```python
res = DNSDumpsterAPI({'verbose': True}).search('microsoft.com')
print res
```

And the result:

```
$ python API_example.py
####### Domain #######
microsoft.com



####### DNS Servers #######
ns2.msft.net.  (208.84.2.53) AS8075 Microsoft Corporation United States
ns3.msft.net.  (193.221.113.53) AS8075 Microsoft Corporation United Kingdom
ns4.msft.net.  (208.76.45.53) AS8075 Microsoft Corporation United States
ns1.msft.net.  (208.84.0.53) AS8075 Microsoft Corporation United States



####### MX Records #######
10 microsoft-com.mail.protection.outlook.com. (207.46.163.138) AS8075 Microsoft Corporation United States



####### Host Records (A) #######
abctool.partners.extranet.microsoft.com (65.55.28.192) AS3598 Microsoft Corporation United States
account-int.mpgsc.glbdns2.microsoft.com (65.55.98.145) AS8075 Microsoft Corporation United States
accumendev.microsoft.com (147.243.197.16) AS6453 TATA COMMUNICATIONS (AMERICA) INC Singapore
acumen.microsoft.com (147.243.197.19) AS6453 TATA COMMUNICATIONS (AMERICA) INC Singapore
adfs.parttest.extranettest.microsoft.com (157.58.204.81) AS3598 Microsoft Corporation United States
ae-3.ibr02.dfw05.network.microsoft.com (104.44.4.14) AS8075 Microsoft Corporation United States
ae-3.ibr03.atb.network.microsoft.com (104.44.4.15) AS8075 Microsoft Corporation United States
agentweb.store.microsoft.com (65.54.248.79) AS8075 Microsoft Corporation United States
ampudc.udc0.glbdns2.microsoft.com (137.116.81.24) AS8075 Microsoft Corporation United States
api.bingads.glbdns2.microsoft.com (65.54.165.80) AS8075 Microsoft Corporation United States
apollo.api.msnmx.glbdns2.microsoft.com (131.253.12.36) AS8075 Microsoft Corporation United States
apolloint.consumer.glbdns2.microsoft.com (23.102.152.149) AS8075 Microsoft Corporation United States
apolloint.dev.cpxint.glbdns2.microsoft.com (23.102.157.92) AS8075 Microsoft Corporation United States
apolloint.feedback.cpxint.glbdns2.microsoft.com (157.55.178.72) AS8075 Microsoft Corporation United States
apolloprodmarketplaceservice.wpsisv.glbdns2.microsoft.com (23.101.177.130) AS8075 Microsoft Corporation United States
appetiteforlife.set.glbdns2.microsoft.com (65.55.116.223) AS8075 Microsoft Corporation United States
app.maps.glbdns2.microsoft.com (111.221.29.26) AS8075 Microsoft Corporation Singapore
app.maps.glbdns2.microsoft.com (131.253.14.117) AS8075 Microsoft Corporation United States
app.maps.glbdns2.microsoft.com (131.253.40.74) AS8075 Microsoft Corporation United States
appsubmissionservice.wpsapp.glbdns2.microsoft.com (65.55.78.53) AS8075 Microsoft Corporation United States
apselfserviceuat.parttest.extranettest.microsoft.com (157.58.204.103) AS3598 Microsoft Corporation United States
archive01.messaging.microsoft.com (65.55.88.42) AS20046 Microsoft Corporation United States
archive03.emea.messaging.microsoft.com (213.199.177.221) AS8075 Microsoft Corporation Ireland
archive05.us2.messaging.microsoft.com (157.55.145.164) AS8075 Microsoft Corporation United States
archive.causes.set.glbdns2.microsoft.com (65.55.116.223) AS8075 Microsoft Corporation United States
att.admin.messaging.microsoft.com (216.32.181.66) AS8075 Microsoft Corporation United States
av1.lyncweb.microsoft.com (194.69.127.69) AS6584 Microsoft Corporation United Kingdom
awsui-ext.glbdns2.microsoft.com (157.58.248.111) AS3598 Microsoft Corporation United States
axis.partners.extranet.microsoft.com (131.107.115.185) AS3598 Microsoft Corporation United States
axisuat.partners.extranet.microsoft.com (131.107.119.220) AS3598 Microsoft Corporation United States
064-smtp-in-2a.microsoft.com (157.54.41.370) AS3598 Microsoft Corporation United States
a.calendars.office.microsoft.com (65.54.206.25) AS8075 Microsoft Corporation United States
a.config.office.microsoft.com (65.54.206.57) AS8075 Microsoft Corporation United States
a.i.office.microsoft.com (65.54.206.53) AS8075 Microsoft Corporation United States
a.officeint.microsoft.com.microsoft.com (207.68.130.204) AS8075 Microsoft Corporation United States
a.officeupdate.microsoft.com (65.54.206.33) AS8075 Microsoft Corporation United States
a.services.office.microsoft.com (65.54.206.56) AS8075 Microsoft Corporation United States
a.shapes.office.microsoft.com (65.54.206.34) AS8075 Microsoft Corporation United States
abtesting.microsoft.com (207.46.131.30) AS8075 Microsoft Corporation United States
ac-staging.support.microsoft.com (65.55.22.157) AS8075 Microsoft Corporation United States
ac2.microsoft.com (65.55.157.94) AS8075 Microsoft Corporation United States
academic.research.microsoft.com (65.54.113.26) AS8075 Microsoft Corporation United States
academymobile.microsoft.com (131.107.97.10) AS3598 Microsoft Corporation United States
accesscontrol.ex.azure.microsoft.com (65.55.54.20) AS8075 Microsoft Corporation United States
accountants.microsoft.com (207.68.165.81) AS8075 Microsoft Corporation United States
accounts.co1.cp.microsoft.com (65.55.7.79) AS8075 Microsoft Corporation United States
accounts.dm2.cp.microsoft.com (134.170.48.205) AS8075 Microsoft Corporation United States
activation.drm.microsoft.com (65.55.61.30) AS8075 Microsoft Corporation United States
activation.isv.drm.microsoft.com (65.55.61.25) AS8075 Microsoft Corporation United States
activation.msft.scm.microsoft.com (207.68.143.247) AS8075 Microsoft Corporation United States
adcenterapi-ppe.microsoft.com (207.46.202.21) AS8075 Microsoft Corporation United States
adcenterapi.adintelligence.microsoft.com (207.46.202.96) AS8075 Microsoft Corporation United States
adcenterapidownload-ppe.microsoft.com (207.46.119.181) AS8075 Microsoft Corporation United States
adcenterhelp-si.microsoft.com (207.46.120.189) AS8075 Microsoft Corporation United States
adcrm.jazz.microsoft.com (207.46.160.27) AS8075 Microsoft Corporation United States
adfs.catcrm-stg.microsoft.com (157.56.138.45) AS8075 Microsoft Corporation United States
adinquiry.adcenter.microsoft.com (207.46.119.245) AS8075 Microsoft Corporation United States
adinquiry.advertiser-si.adcenter.microsoft.com (65.55.130.62) AS8075 Microsoft Corporation United States
adinquiry.bcp.bingads.microsoft.com (65.52.105.117) AS8075 Microsoft Corporation United States
adinquiry.beta.si.bingads.microsoft.com (207.46.119.62) AS8075 Microsoft Corporation United States
adintelligence.pace2.adcenter.microsoft.com (207.46.22.160) AS8075 Microsoft Corporation United States
adintelligence.pace3ldc2.adcenter.microsoft.com (207.46.22.161) AS8075 Microsoft Corporation United States
adlab.microsoft.com (157.55.150.71) AS8075 Microsoft Corporation United States
admin.billing.dm2.cp.microsoft.com (134.170.48.196) AS8075 Microsoft Corporation United States
admin.tagppe.microsoft.com (207.46.203.204) AS8075 Microsoft Corporation United States
admin.tagtst.microsoft.com (207.46.105.245) AS8075 Microsoft Corporation United States
admin.training.partner.microsoft.com (131.107.114.134) AS3598 Microsoft Corporation United States
adminportal.msft.scm.microsoft.com (207.68.143.234) AS8075 Microsoft Corporation United States
adminui.msft.scm.microsoft.com (207.68.143.230) AS8075 Microsoft Corporation United States
adreport-ppe.microsoft.com (65.55.36.254) AS8075 Microsoft Corporation United States
advertiser-pace.adcenter.microsoft.com (207.46.119.170) AS8075 Microsoft Corporation United States
advertiser-rep1.adcenter.microsoft.com (65.55.157.78) AS8075 Microsoft Corporation United States
advertiser-si.adcenter.microsoft.com (65.55.129.45) AS8075 Microsoft Corporation United States
ae-61.ibr01.atb.network.microsoft.com (104.44.8.56) AS8075 Microsoft Corporation United States
ae-61.ibr01.bn1.network.microsoft.com (104.44.8.0) AS8075 Microsoft Corporation United States
ae-61.ibr01.ch1.network.microsoft.com (104.44.8.24) AS8075 Microsoft Corporation United States
ae-62.ibr01.atb.network.microsoft.com (104.44.8.58) AS8075 Microsoft Corporation United States
ae-62.ibr01.bn1.network.microsoft.com (104.44.8.2) AS8075 Microsoft Corporation United States
ae-62.ibr01.ch1.network.microsoft.com (104.44.8.26) AS8075 Microsoft Corporation United States
ae-63.ibr01.bn1.network.microsoft.com (104.44.8.4) AS8075 Microsoft Corporation United States
ae-63.ibr01.ch1.network.microsoft.com (104.44.8.28) AS8075 Microsoft Corporation United States
ae-64.ibr01.bn1.network.microsoft.com (104.44.8.6) AS8075 Microsoft Corporation United States
ae-64.ibr01.ch1.network.microsoft.com (104.44.8.30) AS8075 Microsoft Corporation United States
ae-65.ibr01.bn1.network.microsoft.com (104.44.8.8) AS8075 Microsoft Corporation United States
ae-65.ibr01.ch1.network.microsoft.com (104.44.8.32) AS8075 Microsoft Corporation United States
ae-66.ibr01.bn1.network.microsoft.com (104.44.8.10) AS8075 Microsoft Corporation United States
ae-66.ibr01.ch1.network.microsoft.com (104.44.8.34) AS8075 Microsoft Corporation United States
ae-71.ibr02.atb.network.microsoft.com (104.44.8.60) AS8075 Microsoft Corporation United States
ae-71.ibr02.bn1.network.microsoft.com (104.44.8.12) AS8075 Microsoft Corporation United States
ae-71.ibr02.ch1.network.microsoft.com (104.44.8.36) AS8075 Microsoft Corporation United States
ae-72.ibr02.atb.network.microsoft.com (104.44.8.62) AS8075 Microsoft Corporation United States
ae-72.ibr02.bn1.network.microsoft.com (104.44.8.14) AS8075 Microsoft Corporation United States
ae-72.ibr02.ch1.network.microsoft.com (104.44.8.38) AS8075 Microsoft Corporation United States
ae-73.ibr02.bn1.network.microsoft.com (104.44.8.16) AS8075 Microsoft Corporation United States
ae-73.ibr02.ch1.network.microsoft.com (104.44.8.40) AS8075 Microsoft Corporation United States
ae-74.ibr02.bn1.network.microsoft.com (104.44.8.18) AS8075 Microsoft Corporation United States
ae-74.ibr02.ch1.network.microsoft.com (104.44.8.42) AS8075 Microsoft Corporation United States
ae-75.ibr02.bn1.network.microsoft.com (104.44.8.20) AS8075 Microsoft Corporation United States
ae-75.ibr02.ch1.network.microsoft.com (104.44.8.44) AS8075 Microsoft Corporation United States
ae-76.ibr02.bn1.network.microsoft.com (104.44.8.22) AS8075 Microsoft Corporation United States
ae-76.ibr02.ch1.network.microsoft.com (104.44.8.46) AS8075 Microsoft Corporation United States
ae-81.ibr03.ch1.network.microsoft.com (104.44.8.48) AS8075 Microsoft Corporation United States
ae-82.ibr03.ch1.network.microsoft.com (104.44.8.50) AS8075 Microsoft Corporation United States
ae-83.ibr03.ch1.network.microsoft.com (104.44.8.52) AS8075 Microsoft Corporation United States
ae-84.ibr03.ch1.network.microsoft.com (104.44.8.54) AS8075 Microsoft Corporation United States
aer.microsoft.com (94.245.126.209) AS8075 Microsoft Corporation United Kingdom
agent.wau.store.microsoft.com (65.54.122.25) AS8075 Microsoft Corporation United States
akamaiingester.services.microsoft.com (131.253.14.108) AS8075 Microsoft Corporation United States
alpha.sqm.microsoft.com (65.52.100.12) AS8075 Microsoft Corporation United States
alpha.watson.microsoft.com (65.52.100.80) AS8075 Microsoft Corporation United States
am1ehsobe001.messaging.microsoft.com (213.199.154.204) AS8075 Microsoft Corporation United Kingdom
am1ehsobe002.messaging.microsoft.com (213.199.154.205) AS8075 Microsoft Corporation United Kingdom
am1ehsobe003.messaging.microsoft.com (213.199.154.206) AS8075 Microsoft Corporation United Kingdom
am1outboundsmtppool1.messaging.microsoft.com (213.199.180.165) AS8075 Microsoft Corporation Ireland
am1outboundsmtppool2.messaging.microsoft.com (213.199.180.166) AS8075 Microsoft Corporation Ireland
apac.gmevpn.microsoft.com (192.48.225.100) AS8075 Microsoft Corporation United States
api.bc.adcenter-pace.microsoft.com (65.54.161.204) AS8075 Microsoft Corporation United States
api.current.adcenter-pace.microsoft.com (64.4.21.60) AS8075 Microsoft Corporation United States
api.express.bingads.microsoft.com (131.253.40.78) AS8075 Microsoft Corporation United States
api.next.adcenter-pace.microsoft.com (65.54.165.49) AS8075 Microsoft Corporation United States
api.office.microsoft.com (207.46.222.37) AS8075 Microsoft Corporation United States
api.si.adcenter.microsoft.com (65.55.129.46) AS8075 Microsoft Corporation United States
api.si.yahoo.adcenterapi.microsoft.com (207.46.119.60) AS8075 Microsoft Corporation United States
appinfo.microsoft.com (207.46.153.30) AS8075 Microsoft Corporation United States
aps.mail.microsoft.com (207.46.53.32) AS8075 Microsoft Corporation United States
apsowa.mail.microsoft.com (207.46.55.46) AS8075 Microsoft Corporation India
argoadfs.microsoft.com (207.46.154.163) AS8075 Microsoft Corporation United States
argoctp.microsoft.com (207.46.131.26) AS8075 Microsoft Corporation United States
arr.si.adcenter.microsoft.com (65.55.129.59) AS8075 Microsoft Corporation United States
as.cwa.microsoft.com (131.107.106.30) AS3598 Microsoft Corporation United States
asia-adcenterapi-si.adcenter.microsoft.com (111.221.21.46) AS8075 Microsoft Corporation Singapore
asia1.sysdev-int.microsoft.com (111.221.25.71) AS8075 Microsoft Corporation Singapore
asia1.sysdev.microsoft.com (111.221.25.72) AS8075 Microsoft Corporation Singapore
asia2.sysdev-int.microsoft.com (111.221.18.137) AS8075 Microsoft Corporation Singapore
asia2.sysdev.microsoft.com (111.221.18.136) AS8075 Microsoft Corporation Singapore
aspire.microsoft.com (207.46.159.98) AS8075 Microsoft Corporation United States
assessment.learning.microsoft.com (65.55.191.223) AS8075 Microsoft Corporation United States
assessment.learningbeta.microsoft.com (65.55.191.217) AS8075 Microsoft Corporation United States
assessment.microsoft.com (131.107.100.44) AS3598 Microsoft Corporation United States
assessmentbeta.learning.microsoft.com (131.107.119.61) AS3598 Microsoft Corporation United States
assets.pinpoint.microsoft.com (157.56.79.40) AS8075 Microsoft Corporation United States
assets.ppv1.microsoft.com (134.170.48.180) AS8075 Microsoft Corporation United States
asws.ship.support.microsoft.com (66.119.147.128) AS8075 Microsoft Corporation United States
athlon.cam.uk.eu.microsoft.com (213.199.145.25) AS8075 Microsoft Corporation United Kingdom
atp.agent.services.microsoft.com (134.170.223.242) AS8075 Microsoft Corporation United States
audience-si.bingads.microsoft.com (207.68.157.42) AS8075 Microsoft Corporation United States
audience.bingads.microsoft.com (157.55.150.72) AS8075 Microsoft Corporation United States
auditgw-ppe.css.microsoft.com (157.56.57.110) AS8075 Microsoft Corporation United States
audituat.ws.microsoft.com (157.58.248.44) AS3598 Microsoft Corporation United States
auth.catcrm.microsoft.com (157.56.138.80) AS8075 Microsoft Corporation United States
autobugstaging.microsoft.com (131.107.127.127) AS3598 Microsoft Corporation United States
autodiscover.service.exchange.microsoft.com (131.107.125.8) AS3598 Microsoft Corporation United States
autodiscover.windows.mail.microsoft.com (131.107.1.95) AS3598 Microsoft Corporation United States
autodiscover.winse.microsoft.com (131.107.1.83) AS3598 Microsoft Corporation United States
av00.lyncweb.microsoft.com (131.107.255.87) AS3598 Microsoft Corporation United States
av00.ocsweb.microsoft.com (131.107.106.27) AS3598 Microsoft Corporation United States
av01.lyncweb.microsoft.com (131.107.255.88) AS3598 Microsoft Corporation United States
av01.ocsweb.microsoft.com (131.107.247.197) AS3598 Microsoft Corporation United States
av02.lyncweb.microsoft.com (131.107.255.89) AS3598 Microsoft Corporation United States
av02.ocsweb.microsoft.com (131.107.247.200) AS3598 Microsoft Corporation United States
av03.lyncweb.microsoft.com (131.107.255.90) AS3598 Microsoft Corporation United States
av10.ocsweb.microsoft.com (94.245.124.74) AS8075 Microsoft Corporation United Kingdom
av11.lyncweb.microsoft.com (94.245.124.239) AS8075 Microsoft Corporation United Kingdom
av11.ocsweb.microsoft.com (94.245.124.232) AS8075 Microsoft Corporation United Kingdom
av2.lyncweb.microsoft.com (207.46.55.124) AS8075 Microsoft Corporation India
av20.lyncweb.microsoft.com (207.46.55.127) AS8075 Microsoft Corporation India
av20.ocsweb.microsoft.com (207.46.55.122) AS8075 Microsoft Corporation India
av21.lyncweb.microsoft.com (207.46.53.109) AS8075 Microsoft Corporation United States
av21.ocsweb.microsoft.com (207.46.53.6) AS8075 Microsoft Corporation United States
av3.lyncweb.microsoft.com (65.55.30.131) AS3598 Microsoft Corporation United States
avd1.lync.mds.microsoft.com (157.56.91.170) AS8075 Microsoft Corporation United States
avicode.galleries.microsoft.com (65.55.56.75) AS8075 Microsoft Corporation United States
bac.microsoft.com (65.55.12.248) AS8075 Microsoft Corporation United States
backup.exchange.microsoft.com (131.107.1.98) AS3598 Microsoft Corporation United States
backup12.microsoft.com (207.46.249.29) AS8075 Microsoft Corporation United States
backupserver.flighting.cp.microsoft.com (65.55.145.1) AS8075 Microsoft Corporation United States
barcod.store.microsoft.com (64.4.21.178) AS8075 Microsoft Corporation United States
barcode.store.microsoft.com (207.46.101.211) AS8075 Microsoft Corporation United States
bay-1.extsky.microsoft.com (65.54.239.7) AS8075 Microsoft Corporation United States
bay-2.extsky.microsoft.com (65.54.239.8) AS8075 Microsoft Corporation United States
ae-1.ibr01.atb.network.microsoft.com (104.44.4.38) AS8075 Microsoft Corporation United States
ae-1.ibr01.bn1.network.microsoft.com (104.44.4.62) AS8075 Microsoft Corporation United States
ae-1.ibr01.ch1.network.microsoft.com (104.44.4.52) AS8075 Microsoft Corporation United States
ae-1.ibr01.den07.network.microsoft.com (104.44.4.58) AS8075 Microsoft Corporation United States
ae-1.ibr01.dfw05.network.microsoft.com (104.44.4.6) AS8075 Microsoft Corporation United States
ae-1.ibr01.lax03.network.microsoft.com (104.44.4.0) AS8075 Microsoft Corporation United States
ae-1.ibr01.nyc04.network.microsoft.com (104.44.4.50) AS8075 Microsoft Corporation United States
ae-1.ibr01.yto02.network.microsoft.com (104.44.4.60) AS8075 Microsoft Corporation United States
ae-1.ibr02.atb.network.microsoft.com (104.44.4.39) AS8075 Microsoft Corporation United States
ae-1.ibr02.bn1.network.microsoft.com (104.44.4.63) AS8075 Microsoft Corporation United States
ae-1.ibr02.ch1.network.microsoft.com (104.44.4.53) AS8075 Microsoft Corporation United States
ae-1.ibr02.den07.network.microsoft.com (104.44.4.59) AS8075 Microsoft Corporation United States
ae-1.ibr02.dfw05.network.microsoft.com (104.44.4.7) AS8075 Microsoft Corporation United States
ae-1.ibr02.lax03.network.microsoft.com (104.44.4.1) AS8075 Microsoft Corporation United States
ae-1.ibr02.nyc04.network.microsoft.com (104.44.4.51) AS8075 Microsoft Corporation United States
ae-1.ibr02.yto02.network.microsoft.com (104.44.4.61) AS8075 Microsoft Corporation United States
ae-2.ibr01.ch1.network.microsoft.com (104.44.4.64) AS8075 Microsoft Corporation United States
ae-2.ibr01.dfw05.network.microsoft.com (104.44.4.8) AS8075 Microsoft Corporation United States
ae-2.ibr01.ftw01.network.microsoft.com (104.44.4.9) AS8075 Microsoft Corporation United States
ae-2.ibr01.nyc04.network.microsoft.com (104.44.4.67) AS8075 Microsoft Corporation United States
ae-2.ibr01.sn1.network.microsoft.com (104.44.4.5) AS8075 Microsoft Corporation United States
ae-2.ibr01.yto02.network.microsoft.com (104.44.4.66) AS8075 Microsoft Corporation United States
ae-2.ibr02.atb.network.microsoft.com (104.44.4.40) AS8075 Microsoft Corporation United States
ae-2.ibr02.ch1.network.microsoft.com (104.44.4.56) AS8075 Microsoft Corporation United States
ae-4.ibr02.dfw05.network.microsoft.com (104.44.4.16) AS8075 Microsoft Corporation United States
ae-4.ibr02.ftw01.network.microsoft.com (104.44.4.17) AS8075 Microsoft Corporation United States
ae-2.ibr02.lax03.network.microsoft.com (104.44.4.4) AS8075 Microsoft Corporation United States
ae-2.ibr02.yto02.network.microsoft.com (104.44.4.65) AS8075 Microsoft Corporation United States
ae-2.ibr03.atb.network.microsoft.com (104.44.4.41) AS8075 Microsoft Corporation United States
ae-2.ibr03.ch1.network.microsoft.com (104.44.4.57) AS8075 Microsoft Corporation United States
ae-3.ibr01.atb.network.microsoft.com (104.44.4.42) AS8075 Microsoft Corporation United States
ae-2.ibr01.bn1.network.microsoft.com (104.44.4.49) AS8075 Microsoft Corporation United States
ae-3.ibr01.ch1.network.microsoft.com (104.44.4.54) AS8075 Microsoft Corporation United States
ae-3.ibr01.nyc04.network.microsoft.com (104.44.4.35) AS8075 Microsoft Corporation United States
ae-2.ibr02.atb.network.microsoft.com (104.44.4.48) AS8075 Microsoft Corporation United States
ae-3.ibr02.bn1.network.microsoft.com (104.44.4.27) AS8075 Microsoft Corporation United States
ae-3.ibr03.atb.network.microsoft.com (104.44.4.43) AS8075 Microsoft Corporation United States
ae-3.ibr03.ch1.network.microsoft.com (104.44.4.55) AS8075 Microsoft Corporation United States
ae-4.ibr01.atb.network.microsoft.com (104.44.4.46) AS8075 Microsoft Corporation United States
ae-2.ibr01.by2.network.microsoft.com (104.44.4.3) AS8075 Microsoft Corporation United States
ae-4.ibr01.ch1.network.microsoft.com (104.44.4.37) AS8075 Microsoft Corporation United States
ae-3.ibr01.dfw05.network.microsoft.com (104.44.4.10) AS8075 Microsoft Corporation United States
ae-2.ibr01.lax03.network.microsoft.com (104.44.4.2) AS8075 Microsoft Corporation United States
ae-4.ibr01.sn2.network.microsoft.com (104.44.4.47) AS8075 Microsoft Corporation United States
ae-3.ibr02.dm2.network.microsoft.com (104.44.4.11) AS8075 Microsoft Corporation United States
ae-4.ibr02.nyc04.network.microsoft.com (104.44.4.29) AS8075 Microsoft Corporation United States
ae-3.ibr03.atb.network.microsoft.com (104.44.4.23) AS8075 Microsoft Corporation United States
ae-4.ibr03.ch1.network.microsoft.com (104.44.4.33) AS8075 Microsoft Corporation United States
ae-4.ibr01.atb.network.microsoft.com (104.44.4.44) AS8075 Microsoft Corporation United States
ae-2.ibr02.dfw05.network.microsoft.com (104.44.4.12) AS8075 Microsoft Corporation United States
ae-2.ibr03.atb.network.microsoft.com (104.44.4.13) AS8075 Microsoft Corporation United States
ae-4.ibr03.ch1.network.microsoft.com (104.44.4.45) AS8075 Microsoft Corporation United States
api.si.bingads.glbdns2.microsoft.com (65.55.130.13) AS8075 Microsoft Corporation United States
a.r.office.microsoft.com (65.54.206.58) AS8075 Microsoft Corporation United States
agent.microsoft.com (134.170.185.46) AS8075 Microsoft Corporation United States
asia.microsoft.com (134.170.185.46) AS8075 Microsoft Corporation United States
backoffice.microsoft.com (134.170.185.46) AS8075 Microsoft Corporation United States
autosstore.jpchn.glbdns2.microsoft.com (202.89.225.60) AS8075 Microsoft Corporation Japan
am1ehsobe004.messaging.microsoft.com (213.199.154.207) AS8075 Microsoft Corporation United Kingdom
am1ehsobe005.messaging.microsoft.com (213.199.154.208) AS8075 Microsoft Corporation United Kingdom
am1ehsobe006.messaging.microsoft.com (213.199.154.209) AS8075 Microsoft Corporation United Kingdom
autodiscover.microsoft.com (131.107.125.5) AS3598 Microsoft Corporation United States
av10.lyncweb.microsoft.com (194.69.127.66) AS6584 Microsoft Corporation United Kingdom
microsoft.com (134.170.188.221) AS8075 Microsoft Corporation United States
agent.microsoft.com (134.170.188.221) AS8075 Microsoft Corporation United States
asia.microsoft.com (134.170.188.221) AS8075 Microsoft Corporation United States
backoffice.microsoft.com (134.170.188.221) AS8075 Microsoft Corporation United States
api.tools-int.cp.microsoft.com (65.55.252.49) AS8075 Microsoft Corporation United States
acttproxy.rte.microsoft.com (131.107.67.16) AS3598 Microsoft Corporation United States
archive.messaging.microsoft.com (12.129.20.22) AS17226 AT&T Enhanced Network Services United States



####### TXT Records #######
"v=spf1 include:_spf-a.microsoft.com include:_spf-b.microsoft.com include:_spf-c.microsoft.com include:_spf-ssg-a.microsoft.com include:spf-a.hotmail.com ip4:147.243.128.24 ip4:147.243.128.26 ip4:147.243.1.153 ip4:147.243.1.47 ip4:147.243.1.48 -all"
"FbUF6DbkE+Aw1/wi9xgDi8KVrIIZus5v8L6tbIQZkGrQ/rVQKJi8CjQbBtWtE64ey4NJJwj5J65PIggVYNabdQ=="
```

Result is an array of all subdomains.

Contributing
=======

Feel free to open issues, contribute and submit your Pull Requests.
You can also ping me on Twitter (@PaulWebSec)

