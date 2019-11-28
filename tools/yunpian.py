import requests
import json
class YunPian(object):
    def __init__(self,apikey):
        self.apikey = apikey
        self.massage_url = 'https://sms.yunpian.com/v2/sms/single_send.json'
    def send_message(self,code,mobile):
        # code 验证码
        # mobile 手机
        data = {
            'apikey':self.apikey,
            'mobile':mobile,
            'text':"【大家庭】您的验证码是{code}。如非本人操作，请忽略本短信".format(code=code)
        }
        response = requests.post(self.massage_url,data=data)
        return json.loads(response.text)

if __name__ == '__main__':
    yp = YunPian('c60770e37f172c235b9b3c0380807108')
    yp.send_message('1234','15533062170')