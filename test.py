import urllib.parse

url = "https://spb.zoon.ru/redirect/?to=https%3A%2F%2Fvk.com%2Fmedpraxis&hash=96b7208ff2d5af3c246bd6493057401e&from=596844cd64288e27c6149ce6.d6f3&ext_site=ext_vk&backurl=https%3A%2F%2Fspb.zoon.ru%2Fmedical%2Ftsentr_semejnoj_meditsiny_medpraxis_v_kudrovo%2F"


print(urllib.parse.unquote(url).split("?to=")[1].split("&")[0])