# -*- coding: utf-8 -*
import requests
from bs4 import BeautifulSoup
import json
import ast
import io
import codecs
import sys
import re
import os
import datetime

max_page = 16
dic = {
  'ene':'01',
  'feb':'02',
  'mar':'03',
  'abr':'04',
  'may':'05',
  'jun':'06',
  'jul':'07',
  'ago':'08',
  'sept':'09',
  'oct':'10',
  'nov':'11',
  'dic':'12'
}

true_num = 0
cnt = 0
for page in range(1, max_page+1):
  url = "https://www.elpais.com.uy/noticias/china?page="+str(page)
  payload = {}
  headers = {
    'authority': 'www.elpais.com.uy',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,es;q=0.5',
    'cache-control': 'no-cache',
    'cookie': 'cf_clearance=FnNXLjiddv89bKrI_bfOMaI_OjW9bzXn1VlhLNq1K2A-1699071085-0-1-2191e54f.1b5ab033.7690baaf-150.0.0; _pctx=%7Bu%7DN4IgrgzgpgThIC4B2YA2qA05owMoBcBDfSREQpAeyRCwgEt8oBJAEzIE4AmHgZgBYAbAA5ePDgFYA7BInCZIAL5A; _pcid=%7B%22browserId%22%3A%22lojj25s6iqp0eyvo%22%7D; cX_P=lojj25s6iqp0eyvo; compass_uid=7206fd5b-0a6a-4bd6-90be-21514a216049; cX_G=cx%3A2xlt0bcofskbe2imb1pruv4ro6%3A14m3tdzyl5ksy; _fbp=fb.2.1699071120272.257167521; _pbjs_userid_consent_data=3524755945110770; _li_dcdm_c=.elpais.com.uy; _lc2_fpi=80587b274ca6--01hec8gkp1gcdact7eya0jdpbj; _pubcid=b37d2bbd-fe0a-4e02-92df-8a188e8f0807; _cc_id=267cc3771c76df79b900426104f145d6; _au_1d=AU1D-0100-001699071157-TZ96BHIS-38DO; _ga_TZCWF9VBFR=GS1.3.1699071208.1.1.1699071267.1.0.0; _lr_env_src_ats=false; pbjs-unifiedid=%7B%22TDID%22%3A%22839db8aa-c56b-4e26-a612-d4f9665cee2f%22%2C%22TDID_LOOKUP%22%3A%22FALSE%22%2C%22TDID_CREATED_AT%22%3A%222023-11-04T04%3A16%3A09%22%7D; ___nrbi=%7B%22firstVisit%22%3A1699071093%2C%22userId%22%3A%227206fd5b-0a6a-4bd6-90be-21514a216049%22%2C%22userVars%22%3A%5B%5B%22mrfExperiment_recommenderInline%22%2C%221%22%5D%2C%5B%22mrfExperiment_ABtest%22%2C%221%22%5D%2C%5B%22mrfExperiment_Test1%22%2C%221%22%5D%5D%2C%22futurePreviousVisit%22%3A1699500522%2C%22timesVisited%22%3A2%7D; _gid=GA1.3.1294218122.1699500524; vido_visitor_id=6357f5c4e00e5cd56abc56110740cf5b; _vfa=www%2Eelpais%2Ecom%2Euy.00000000-0000-4000-8000-24109e8ba54f.c462a308-3397-41b5-a6ca-e2838b24a846.1699071093.1699071093.1699500524.2; __li_idex_cache_e30=%7B%22nonId%22%3A%22jEDwHYJOFNC2cHPXgZK4DyUSD2uVDbgXhgqunA%22%7D; pbjs_li_nonid=%7B%22nonId%22%3A%22jEDwHYJOFNC2cHPXgZK4DyUSD2uVDbgXhgqunA%22%7D; cto_dna_bundle=LnFDs19EeUJqUE9kT3pIUVR5a0JZNFNyZlVhVlZOJTJGUHdxJTJCNm5naHNhd3ZHd3RRS0x4N1BScDdDY1R0V0g5Zk50ZXAyR2hzZ1VwSzBaTEtZZkZpUSUyQnpTcmpNQSUzRCUzRA; _ga_MF621VF0E8=GS1.3.1699501227.1.0.1699501227.60.0.0; _au_last_seen_pixels=eyJhcG4iOjE2OTk1MDEzMjAsInR0ZCI6MTY5OTUwMTMyMCwicHViIjoxNjk5NTAxMzIwLCJydWIiOjE2OTk1MDEzMjAsInRhcGFkIjoxNjk5NTAxMzIwLCJhZHgiOjE2OTk1MDEzMjAsImdvbyI6MTY5OTUwMTMyMCwic21hcnQiOjE2OTkwNzExNTcsImNvbG9zc3VzIjoxNjk5MDcxMTU3LCJpbmRleCI6MTY5OTA3MTM2MCwiYWRvIjoxNjk5NTAxMzIwLCJvcGVueCI6MTY5OTA3MTM2MCwicHBudCI6MTY5OTUwMTMyMCwiYmVlcyI6MTY5OTA3MTM2MCwiYW1vIjoxNjk5MDcxMzYwLCJpbXByIjoxNjk5MDcxMzYwLCJ1bnJ1bHkiOjE2OTkwNzEzNjAsInRhYm9vbGEiOjE2OTkwNzEzNjAsInNvbiI6MTY5OTUwMTMyMH0%3D; panoramaId=f916232372bb4ec18d9efc515cad16d53938304ef2e3d3be379752366abf2d59; panoramaIdType=panoIndiv; __li_idex_cache=%7B%22unifiedId%22%3A%22jEDwHYJOFNC2cHPXgZK4DyUSD2uVDbgXhgqunA%22%7D; panoramaId_expiry=1700106123477; cto_bundle=x95uJl9EeUJqUE9kT3pIUVR5a0JZNFNyZlVYbUZScWclMkZnR0k0dm9ubVNEaG9zMjVaOTRyUkdEMktjRHBMJTJGNzZ1cnclMkZTOTFLMndabTQzbUFvb2dsRzhPa2NrMlgzaUFtTlpmV3AlMkY1OThQNU1VWHJRTGVQaXRtOEE4WG82NG83OCUyQnVaU0hJTyUyRkVOMkk2ZENma3RlZkZiQ2JuJTJCZyUzRCUzRA; cto_bundle=x95uJl9EeUJqUE9kT3pIUVR5a0JZNFNyZlVYbUZScWclMkZnR0k0dm9ubVNEaG9zMjVaOTRyUkdEMktjRHBMJTJGNzZ1cnclMkZTOTFLMndabTQzbUFvb2dsRzhPa2NrMlgzaUFtTlpmV3AlMkY1OThQNU1VWHJRTGVQaXRtOEE4WG82NG83OCUyQnVaU0hJTyUyRkVOMkk2ZENma3RlZkZiQ2JuJTJCZyUzRCUzRA; cto_bidid=D4xGJF9VVTdnNkljTmQlMkJWR1ZvSnZSNTllTnY1N3ltWVhnbGY3R3QlMkJDYmpsN3dxcmc3N3h1Q0h1Z0ZIb3dtYmUyQWxQYWx0UkMxU1B4eGk1S1NJa0VDSHBoZmd6T25iNlJjWVpLejM4U2NtWk1mS1ElM0Q; cto_bidid=D4xGJF9VVTdnNkljTmQlMkJWR1ZvSnZSNTllTnY1N3ltWVhnbGY3R3QlMkJDYmpsN3dxcmc3N3h1Q0h1Z0ZIb3dtYmUyQWxQYWx0UkMxU1B4eGk1S1NJa0VDSHBoZmd6T25iNlJjWVpLejM4U2NtWk1mS1ElM0Q; cnx_userId=da74039896c747a4bb2c0bd816f83ec4; vido_first_impression=27746; __gads=ID=f79f5153aea079af-22d6e90157e500a0:T=1699071119:RT=1699504704:S=ALNI_MYxzcoG-2Vgpyrn2wYWWOFPdvODvA; _pk_id.KL91ITUDA0MTF.d199=b5747e11298cb569.1699071108.3.1699504722.1699504722.; _pk_ses.KL91ITUDA0MTF.d199=1; _ga=GA1.3.846046633.1699071093; _gat=1; _gat_redElPaisTrk=1; _vfz=www%2Eelpais%2Ecom%2Euy.00000000-0000-4000-8000-24109e8ba54f.1699504728.1.medium=direct|source=|sharer_uuid=|terms=; _vfb=www%2Eelpais%2Ecom%2Euy.00000000-0000-4000-8000-24109e8ba54f.2.10.1699504728.true...; _vfa=www%2Eelpais%2Ecom%2Euy.00000000-0000-4000-8000-24109e8ba54f.c462a308-3397-41b5-a6ca-e2838b24a846.1699071093.1699071093.1699500524.2; __gpi=UID=00000c7f7507bd13:T=1699071119:RT=1699504730:S=ALNI_MZTJ4ZVxRDT5guU0Pt6SgoZOQaiCA; _ga_CBSZFBWGVJ=GS1.3.1699504732.3.0.1699504732.60.0.0; _ga_S7VNV656TN=GS1.3.1699504732.3.0.1699504732.60.0.0; _vfb=www%2Eelpais%2Ecom%2Euy.00000000-0000-4000-8000-24109e8ba54f.3.10.1699504728.true...; FCCDCF=%5Bnull%2Cnull%2Cnull%2Cnull%2C%5B%5B1699504734%2C423000000%5D%2C%221YNN%22%5D%2Cnull%2C%5B%5D%5D; FCNEC=%5B%5B%22AKsRol_4vjFy6xmx4_VZAsGnqT8fpZGA7A1576exMEMwQYEITVwE49oKx6Urt2zYXfDX5D9_RSG7X-jfxGQg8yCuljV1blsnEIqjxqTjISQ32qQq6kp33jc-mUL1IRz-wrPP9PwD8uGSakYpHazwVeTbceeKI1PtJA%3D%3D%22%5D%2C%5B%5D%2C%5B%5B5%2C%22187%22%5D%5D%5D; cto_bidid=W4mq5V9VVTdnNkljTmQlMkJWR1ZvSnZSNTllTnY1N3ltWVhnbGY3R3QlMkJDYmpsN3dxcmc3N3h1Q0h1Z0ZIb3dtYmUyQWxQYWx0UkMxU1B4eGk1S1NJa0VDSHBoZm9scWNMeWtsYXN2NU1meFBMeUNmRFklM0Q; cto_bundle=-xvTC19EeUJqUE9kT3pIUVR5a0JZNFNyZlVjVmRDd2xhMjAlMkY5bFdyTG9JM1o0dXZJMWdjcmk1dWlUZWlMcENQbjdTb2hJY08wV21hYlh3N0d4VnZwSlBwJTJCcUR0bHBYSEUxdXg5alRKb1dYQWZ3YzdvMVJCJTJGdjcydXJ6UkFmZFRtcTVFN3dDUmUxanh2aVhqdUgwTnd4SWYlMkZZZyUzRCUzRA; lotame_domain_check=elpais.com.uy; _ga_C3K9LY9JC6=GS1.1.1699504701.4.1.1699504771.60.0.0; ___nrbic=%7B%22previousVisit%22%3A1699071093%2C%22currentVisitStarted%22%3A1699500522%2C%22sessionId%22%3A%223070ccc7-136a-4703-a896-578ea512933c%22%2C%22sessionVars%22%3A%5B%5D%2C%22visitedInThisSession%22%3Atrue%2C%22pagesViewed%22%3A44%2C%22landingPage%22%3A%22https%3A//www.elpais.com.uy/noticias/china%22%2C%22referrer%22%3A%22%22%7D',
    'pragma': 'no-cache',
    'referer': 'https://www.elpais.com.uy/noticias/china',
    'sec-ch-ua': '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'
  }
  response = requests.request("GET", url, headers=headers, data=payload)
  response = response.content.decode("utf-8")
  s = BeautifulSoup(response, 'html.parser')
  for i in s.find_all(name='h2', attrs={'class':'Promo-title'}):
    cnt += 1
    print(cnt,'/',12*max_page)
    try:
      title = i.getText()
      link = i.a['href']
      print("title: "+title)
      print("link: "+link)
      # 开始爬取正文内容
      article_url = link
      payload = {}
      headers = {
        'authority': 'www.elpais.com.uy',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,es;q=0.5',
        'cache-control': 'no-cache',
        'cookie': 'cf_clearance=FnNXLjiddv89bKrI_bfOMaI_OjW9bzXn1VlhLNq1K2A-1699071085-0-1-2191e54f.1b5ab033.7690baaf-150.0.0; _pctx=%7Bu%7DN4IgrgzgpgThIC4B2YA2qA05owMoBcBDfSREQpAeyRCwgEt8oBJAEzIE4AmHgZgBYAbAA5ePDgFYA7BInCZIAL5A; _pcid=%7B%22browserId%22%3A%22lojj25s6iqp0eyvo%22%7D; cX_P=lojj25s6iqp0eyvo; compass_uid=7206fd5b-0a6a-4bd6-90be-21514a216049; cX_G=cx%3A2xlt0bcofskbe2imb1pruv4ro6%3A14m3tdzyl5ksy; _fbp=fb.2.1699071120272.257167521; _pbjs_userid_consent_data=3524755945110770; _li_dcdm_c=.elpais.com.uy; _lc2_fpi=80587b274ca6--01hec8gkp1gcdact7eya0jdpbj; _pubcid=b37d2bbd-fe0a-4e02-92df-8a188e8f0807; _cc_id=267cc3771c76df79b900426104f145d6; _au_1d=AU1D-0100-001699071157-TZ96BHIS-38DO; _ga_TZCWF9VBFR=GS1.3.1699071208.1.1.1699071267.1.0.0; _lr_env_src_ats=false; pbjs-unifiedid=%7B%22TDID%22%3A%22839db8aa-c56b-4e26-a612-d4f9665cee2f%22%2C%22TDID_LOOKUP%22%3A%22FALSE%22%2C%22TDID_CREATED_AT%22%3A%222023-11-04T04%3A16%3A09%22%7D; ___nrbi=%7B%22firstVisit%22%3A1699071093%2C%22userId%22%3A%227206fd5b-0a6a-4bd6-90be-21514a216049%22%2C%22userVars%22%3A%5B%5B%22mrfExperiment_recommenderInline%22%2C%221%22%5D%2C%5B%22mrfExperiment_ABtest%22%2C%221%22%5D%2C%5B%22mrfExperiment_Test1%22%2C%221%22%5D%5D%2C%22futurePreviousVisit%22%3A1699500522%2C%22timesVisited%22%3A2%7D; _gid=GA1.3.1294218122.1699500524; vido_visitor_id=6357f5c4e00e5cd56abc56110740cf5b; _vfa=www%2Eelpais%2Ecom%2Euy.00000000-0000-4000-8000-24109e8ba54f.c462a308-3397-41b5-a6ca-e2838b24a846.1699071093.1699071093.1699500524.2; __li_idex_cache_e30=%7B%22nonId%22%3A%22jEDwHYJOFNC2cHPXgZK4DyUSD2uVDbgXhgqunA%22%7D; pbjs_li_nonid=%7B%22nonId%22%3A%22jEDwHYJOFNC2cHPXgZK4DyUSD2uVDbgXhgqunA%22%7D; _ga_MF621VF0E8=GS1.3.1699501227.1.0.1699501227.60.0.0; _au_last_seen_pixels=eyJhcG4iOjE2OTk1MDEzMjAsInR0ZCI6MTY5OTUwMTMyMCwicHViIjoxNjk5NTAxMzIwLCJydWIiOjE2OTk1MDEzMjAsInRhcGFkIjoxNjk5NTAxMzIwLCJhZHgiOjE2OTk1MDEzMjAsImdvbyI6MTY5OTUwMTMyMCwic21hcnQiOjE2OTkwNzExNTcsImNvbG9zc3VzIjoxNjk5MDcxMTU3LCJpbmRleCI6MTY5OTA3MTM2MCwiYWRvIjoxNjk5NTAxMzIwLCJvcGVueCI6MTY5OTA3MTM2MCwicHBudCI6MTY5OTUwMTMyMCwiYmVlcyI6MTY5OTA3MTM2MCwiYW1vIjoxNjk5MDcxMzYwLCJpbXByIjoxNjk5MDcxMzYwLCJ1bnJ1bHkiOjE2OTkwNzEzNjAsInRhYm9vbGEiOjE2OTkwNzEzNjAsInNvbiI6MTY5OTUwMTMyMH0%3D; panoramaId=f916232372bb4ec18d9efc515cad16d53938304ef2e3d3be379752366abf2d59; panoramaIdType=panoIndiv; panoramaId_expiry=1700106123477; _pk_ses.KL91ITUDA0MTF.d199=1; _vfa=www%2Eelpais%2Ecom%2Euy.00000000-0000-4000-8000-24109e8ba54f.c462a308-3397-41b5-a6ca-e2838b24a846.1699071093.1699071093.1699500524.2; FCNEC=%5B%5B%22AKsRol_4vjFy6xmx4_VZAsGnqT8fpZGA7A1576exMEMwQYEITVwE49oKx6Urt2zYXfDX5D9_RSG7X-jfxGQg8yCuljV1blsnEIqjxqTjISQ32qQq6kp33jc-mUL1IRz-wrPP9PwD8uGSakYpHazwVeTbceeKI1PtJA%3D%3D%22%5D%2C%5B%5D%2C%5B%5B5%2C%22187%22%5D%5D%5D; cto_bidid=W4mq5V9VVTdnNkljTmQlMkJWR1ZvSnZSNTllTnY1N3ltWVhnbGY3R3QlMkJDYmpsN3dxcmc3N3h1Q0h1Z0ZIb3dtYmUyQWxQYWx0UkMxU1B4eGk1S1NJa0VDSHBoZm9scWNMeWtsYXN2NU1meFBMeUNmRFklM0Q; cto_bundle=-xvTC19EeUJqUE9kT3pIUVR5a0JZNFNyZlVjVmRDd2xhMjAlMkY5bFdyTG9JM1o0dXZJMWdjcmk1dWlUZWlMcENQbjdTb2hJY08wV21hYlh3N0d4VnZwSlBwJTJCcUR0bHBYSEUxdXg5alRKb1dYQWZ3YzdvMVJCJTJGdjcydXJ6UkFmZFRtcTVFN3dDUmUxanh2aVhqdUgwTnd4SWYlMkZZZyUzRCUzRA; _pk_ref.KL91ITUDA0MTF.d199=%5B%22%22%2C%22%22%2C0%2C%22%22%5D; cnx_userId=533344fd11c546bb85f6d37f3a402cce; _vfz=www%2Eelpais%2Ecom%2Euy.00000000-0000-4000-8000-24109e8ba54f.1699505227.1.medium=direct|source=|sharer_uuid=|terms=; vido_first_impression=28030; FCCDCF=%5Bnull%2Cnull%2Cnull%2Cnull%2C%5B%5B1699505371%2C883000000%5D%2C%221YNN%22%5D%2Cnull%2C%5B%5D%5D; __gads=ID=f79f5153aea079af-22d6e90157e500a0:T=1699071119:RT=1699505371:S=ALNI_MYxzcoG-2Vgpyrn2wYWWOFPdvODvA; _lr_retry_request=true; cto_bundle=oMvNoV9EeUJqUE9kT3pIUVR5a0JZNFNyZlVRaEJpMW0lMkZjWGFKZGU3UyUyRjFtd21ld3gwRUl6WWRrQTlGNjh5JTJGVHNaWG40THpETkVLQkxXekt3VUFZSFNkY044Z0ZmeTNYNE9BNnRrbUpPMEJuc094TnBNUkpicldpVG90U29lcWtSRlNpQnpWaVBxSkdncFBBQXhTZFUlMkY1YSUyQiUyRkElM0QlM0Q; cto_bundle=oMvNoV9EeUJqUE9kT3pIUVR5a0JZNFNyZlVRaEJpMW0lMkZjWGFKZGU3UyUyRjFtd21ld3gwRUl6WWRrQTlGNjh5JTJGVHNaWG40THpETkVLQkxXekt3VUFZSFNkY044Z0ZmeTNYNE9BNnRrbUpPMEJuc094TnBNUkpicldpVG90U29lcWtSRlNpQnpWaVBxSkdncFBBQXhTZFUlMkY1YSUyQiUyRkElM0QlM0Q; cto_bidid=S2H34l9VVTdnNkljTmQlMkJWR1ZvSnZSNTllTnY1N3ltWVhnbGY3R3QlMkJDYmpsN3dxcmc3N3h1Q0h1Z0ZIb3dtYmUyQWxQYWx0UkMxU1B4eGk1S1NJa0VDSHBoZmdlUzNGRCUyQiUyRkF6UW80Smw3ZWQyU1AwJTNE; cto_bidid=S2H34l9VVTdnNkljTmQlMkJWR1ZvSnZSNTllTnY1N3ltWVhnbGY3R3QlMkJDYmpsN3dxcmc3N3h1Q0h1Z0ZIb3dtYmUyQWxQYWx0UkMxU1B4eGk1S1NJa0VDSHBoZmdlUzNGRCUyQiUyRkF6UW80Smw3ZWQyU1AwJTNE; cto_dna_bundle=6URQA19EeUJqUE9kT3pIUVR5a0JZNFNyZlVhVlZOJTJGUHdxJTJCNm5naHNhd3ZHd3RRS0x4N1BScDdDY1R0V0g5Zk50ZXAyR2JiTHpmJTJGMnB3aEwzTHQ1TktTbUZxZyUzRCUzRA; __gpi=UID=00000c7f7507bd13:T=1699071119:RT=1699505570:S=ALNI_MZTJ4ZVxRDT5guU0Pt6SgoZOQaiCA; ___nrbic=%7B%22previousVisit%22%3A1699071093%2C%22currentVisitStarted%22%3A1699500522%2C%22sessionId%22%3A%223070ccc7-136a-4703-a896-578ea512933c%22%2C%22sessionVars%22%3A%5B%5D%2C%22visitedInThisSession%22%3Atrue%2C%22pagesViewed%22%3A49%2C%22landingPage%22%3A%22https%3A//www.elpais.com.uy/noticias/china%22%2C%22referrer%22%3A%22%22%7D; _pk_id.KL91ITUDA0MTF.d199=b5747e11298cb569.1699071108.3.1699505576.1699504722.; _ga_C3K9LY9JC6=GS1.1.1699504701.4.1.1699505577.60.0.0; _ga=GA1.3.846046633.1699071093; _gat=1; _gat_redElPaisTrk=1; _vfb=www%2Eelpais%2Ecom%2Euy.00000000-0000-4000-8000-24109e8ba54f.10.10.1699504728.true...; _ga_S7VNV656TN=GS1.3.1699504732.3.1.1699505590.60.0.0; _ga_CBSZFBWGVJ=GS1.3.1699504732.3.1.1699505590.60.0.0; _vfb=www%2Eelpais%2Ecom%2Euy.00000000-0000-4000-8000-24109e8ba54f.11.10.1699504728.true...',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'
      }
      response = requests.request("GET", article_url, headers=headers, data=payload)
      response = response.content.decode("utf-8")
      s = BeautifulSoup(response, 'html.parser')
      time = s.find_all(name='div', attrs={'class':'Page-datePublished'})[0].getText()
      month = time[3:5]
      year = time[6:10]
      time = year+month
      print("time: "+time)
      div = s.find_all(name='div', attrs={'class':'RichTextBody'})[0]
      s = str(div)
      flag = False
      if s.find('<br/>') != -1:
        s = s.replace('<br/>', '</p><p>')
        flag = True
      else:
        author = ""
      # print(s,'-----------------')
      s = BeautifulSoup(s, 'html.parser')
      # print(s)
      p = s.find_all('p')
      if flag == True:
        author = p[0].getText()
      print('author: '+author)
      output_path = 'D:/order/elpaisuy/'+'elpaisuy_'+time+'.txt'
      file1 = open(output_path, 'a', encoding = 'utf-8')
      file1.write(title+'\n\n\n')
      file1.write('Por '+author+'\n\n')
      if flag == True:
        for j in range(1, len(p)):
          if p[j].getText() == "":
            continue
          file1.write(p[j].getText()+'\n\n')
      else:
        for j in range(0, len(p)):
          if p[j].getText() == "":
            continue
          file1.write(p[j].getText()+'\n\n')
      file1.write('\n\n\n\n\n')
      true_num += 1
      print("true_num: "+str(true_num))
      file1.close()
    except Exception as e:
      file2 = open('D:/order/elpaisuy/error.txt', 'a')
      file2.write(str(cnt)+'/'+str(12*max_page)+'\n')
      file2.write("true_num: "+str(true_num)+'\n')
      file2.write(str(e)+'\n')
      file2.write('\n\n\n')
      file2.close()  