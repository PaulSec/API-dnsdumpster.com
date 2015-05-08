Python API for dnsdumpster.com 
========


Usage 
========

Import the class: 

```python
from DNSDumpsterAPI import DNSDumpsterAPI
```

Then, search for a specific domain: 


```python
res = DNSDumpsterAPI({'verbose': True}).search('microsoft.com')
print res
```

And the result: 

```
$ python API_example.py 
[verbose] Retrieved token: Llx8c9vTCAQXuRdij3CAuMhLeDgKI2Oo
[verbose] Retrieving all subdomains
['b.i.office', 'auditgw-ppe.css', 'be-apiqsg-prod-search.glbdns2', 'blugro7gms.groove', 'avd1.lync.mds', 'avicode.galleries', 'activation.isv.drm', 'blugro1provision.groove', 'alpha.sqm', 'api.express.bingads', 'barcode.store', 'bcp.evdesktop.adcenter', 'bi2', 'asia2.sysdev-int', 'billingjournalservice.dm2.cp', 'api.si.bingads.glbdns2', 'beta.sts.advertising', 'autosstore.jpchn.glbdns2', 'auth.catcrm', 'appsubmissionservice.wpsapp.glbdns2', 'billpay.money.glbdns', 'beta2.preview.games.metaservices', 'accounts.co1.cp', 'advertiser-si.adcenter', 'am1outboundsmtppool1.messaging', 'betalearningservices', 'bcp.adcenter', '4', 'b.calendars.office', '8', 'auth.office', 'backoffice', 'a.services.office', 'adcenterapidownload-ppe', 'blu.officetestfive1', 'beta.wsp', 'blu.officebeta', 'preview.info.music.metaservices', 'beta.mail', '9', 'apolloint.consumer.glbdns2', 'aer', 'adminui.msft.scm', '6.messaging', '2', 'apollo.api.msnmx.glbdns2', 'assessment.learningbeta', 'blu.fast.office', '1.lyncweb', 'beta.express.bingads', 'beta.si.bingads.glbdns2', 'blugro1gms.groove', 'services.officebeta', 'asws.ship.support', 'am1outboundsmtppool2.messaging', 'activation.msft.scm', 'assessment.learning', 'bac', 'billing-co1.cp', 'a.r.office', 'bayprofile15', 'adlab', 'adinquiry.advertiser-si.adcenter', 'advertiser-pace.adcenter', 'adcenterapi-ppe', '2.lyncweb', 'av2.lyncweb', 'bayprofile14', 'academymobile', 'blugro4relay.groove', 'mail', 'bayprofile11', 'bayprofile12', 'sf.msft.scm', 'config.officebeta', 'argoctp', '64-smtp-in-2a', 'billingservices', 'blu.social.msn.glbdns', 'argoadfs', 'a.i.office', 'asia1.sysdev', 'articles.moneycentral.blu.cb3.glbdns', 'blu.rr.office', 'apsowa.mail', 'asia2.sysdev', 'asia', 'blugro4gms.groove', 'account-int.mpgsc.glbdns2', '3.emea.messaging', '3', 'av3.lyncweb', 'ch1.agent.services', '7', 'blugro6gms.groove', '1.ocsweb', 'appinfo', 'bid.mobilling', 'bizspark', 'blugro6relay.groove', 'billingjournalservice.co1.cp', 'blu-3.extsky2', 'agent.wau.store', 'adminportal.msft.scm', 'biretta.cam.uk.eu', '3.messaging', 'api.si.yahoo.adcenterapi', 'api.si.adcenter', 'blugro3gms.groove', 'advertiser-rep1.adcenter', 'agentweb.store', 'bemisstaging', 'barcod.store', 'billing-dm2.cp', 'api.si.bingads', 'beta.bac', 'bingads.glbdns2', 'admin.tagtst', 'bcp.adcenterapidownload', 'aspire', 'blu.officeimages', 'backup.exchange', 'bl2-1.extsky', 'autodiscover.winse', 'bcp.adcenterhelp', 'blu.api.social.msn.glbdns', 'activation.drm', 'spf-ssg-a', 'abtesting', 'adcenterhelp-si', 'audience-si.bingads', 'bl.msft.scm', '5.messaging', 'arr.si.adcenter', 'blugro2gms.groove', 'api.next.adcenter-pace', 'admin.billing.dm2.cp', '1.messaging', 'autodiscover', 'av11.lyncweb', 'adcrm.jazz', 'bay-3.extsky2', 'blugro2relay.groove', 'assets.pinpoint', 'assessmentbeta.learning', 'acttproxy.rte', 'b.config.office', 'ac2', 'att.admin.messaging', 'assessment', 'bl2-2.extsky', 'a.calendars.office', 'bemisdev', 'blu.kolr.office', 'evdesktop-si.adcenter', 'billingservice.dm2.cp', 'spf-c', 'spf-b', 'spf-a', '6', 'blugro5relay.groove', '3.lyncweb', 'blu.messaging.office', 'athlon.cam.uk.eu', 'beta.cam', 'alpha.watson', 'av21.ocsweb', 'a.config.office', 'a.officeupdate', 'aps.mail', 'winse', 'beta.snackbox', 'adintelligence.pace3ldc2.adcenter', 'ac-staging.support', 'api.dds', 'api.current.adcenter-pace', 'academic.research', 'api.office', 'c2.by2.adcenterapi', 'bcp.internal.adcenter', 'adintelligence.pace2.adcenter', 'adreport-ppe', 'av1.lyncweb', 'app.maps.glbdns2', 'awsui-ext.glbdns2', 'appetiteforlife.set.glbdns2', 'bay-1.extsky', 'apolloprodmarketplaceservice.wpsisv.glbdns2', 'autodiscover.windows.mail', 'archive.causes.set.glbdns2', 'adinquiry.beta.si.bingads', 'audience.bingads', 'agent', 'beta.mail.windows', 'audituat.ws', '2.ocsweb', 'beta.itasignon', 'bizweb.store', 'bl2.emailautoconfig', 'grv', 'api.tools-int.cp', '2.messaging', '5.us2.messaging', 'api.bc.adcenter-pace', 'billingservices-staging', 'adcenterapi.adintelligence', '1', 'agent.services', 'av21.lyncweb', 'as.cwa', '5', 'accounts.dm2.cp', 'blu.officebetaimages', 'adfs.catcrm-stg', 'autodiscover.service.exchange', 'blu.ewa.office', 'assets.ppv1', '.lyncweb', 'bay-2.extsky', 'autobugstaging', 'a.shapes.office', 'api.bingads.glbdns2', 'blugro1relay.groove', '4.messaging', 'blugro5gms.groove', 'archive.messaging', 'accountants', 'a.messaging.office', 'bc.pubcenter-pace', 'accesscontrol.ex.azure', 'beta.research', 'adinquiry.bcp.bingads', 'blugro3relay.groove', 'beta3.pubcenter', 'blugro7relay.groove', 'adfs.parttest.extranettest', 'backup12', '.ocsweb', 'asia1.sysdev-int', 'billingservice.co1.cp', 'beta.usnews.money.glbdns', 'admin.tagppe', 'mpan.accounting', 'asia-adcenterapi-si.adcenter', 'av11.ocsweb', 'adinquiry.adcenter']
```

Result is an array of all subdomains. 

Contributing
=======

Feel free to open issues, contribute and submit your Pull Requests. 
You can also ping me on Twitter (@PaulWebSec)

