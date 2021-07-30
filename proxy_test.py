


PROXY_GATEWAY_POOL = [
    "45.149.145.82:8000:4apYHC:dD32xW", "45.149.144.240:8000:4apYHC:dD32xW",
    "45.149.146.66:8000:4apYHC:dD32xW", "45.149.145.77:8000:4apYHC:dD32xW",
    "45.149.145.187:8000:4apYHC:dD32xW", "45.149.146.65:8000:4apYHC:dD32xW",
    "45.149.147.129:8000:4apYHC:dD32xW", "45.149.147.16:8000:4apYHC:dD32xW",
    "45.149.145.211:8000:4apYHC:dD32xW", "45.149.147.202:8000:4apYHC:dD32xW",
    "45.149.145.247:8000:4apYHC:dD32xW", "45.149.146.9:8000:4apYHC:dD32xW",
    "45.149.144.94:8000:TtnqZk:oeLsgH"
]  # ,

for proxy in PROXY_GATEWAY_POOL:
    pxy = 'http://{2}:{3}@{0}:{1}'.format(*proxy.split(':'))
    print(pxy)