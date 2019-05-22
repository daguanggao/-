import requests
import json
import execjs
import tkinter as tk

# 翻译工具
# header = {
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
#             }
# date = {
#     'from': 'en',
#     'to': 'zh',
#     'query': 'hello',
#     'transtype': 'translang',
#     'simple_means_flag': '3',
#     'sign': '54706.276099',
#     # 'token':'553dfc32bbc22addba88b48fc2490aad',
#     }
# post_url = 'https://fanyi.baidu.com/v2transapi'
# r = requests.post(post_url, data = date, headers= header)
# print(r.content.decode())

# 以上请求失败   转成从手机版入手
# Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 Mobile Safari/537.36
# header = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Mobile Safari/537.36' }
# data = {
#     'f': 'auto',
# 't': 'auto',
# 'w': sys.argv[1],
#     }
#
# post_url = 'http://fy.iciba.com/ajax.php?a=fy'
# r = requests.post(post_url, data= data,headers=header)
# r_dict = json.loads(r.content.decode())
# print(r_dict['content']['out'])



class BaiDuFanYi:
    def __init__(self):
        self.str = None
        self.url = 'https://fanyi.baidu.com/v2transapi'
        self.header = {'Cookie': 'BAIDUID=58568C369576E359525CCEDBC2F14363:FG=1; '
                                 'PSTM=1557282822; BIDUPSID=A9F41A771EFBD17D7813E711EA01EB08; '
                                 'REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; '
                                 'SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; BDORZ=FFFB88E999055A3F8A630C64834BD6D0;'
                                 ' Hm_lvt_afd111fa62852d1f37001d1f980b6800=1558339813; '
                                 'H_WISE_SIDS=131528_126891_100805_113879_128069_130510_131891_131075_125696_132019_'
                                 '120144_132213_131517_132260_118880_118872_131401_118845_118821_118790_130763_132211_'
                                 '131650_131577_131535_131533_131529_130222_131295_131871_131390_129564_107319_131796_131396_'
                                 '130121_131874_130569_131194_130349_117428_131241_129653_131246_124625_131861_131436_131687_131035_'
                                 '131905_132091_131045_129374_129644_132204_132267_131167_110085_127969_131357_123290_131752_127317_'
                                 '130603_128201_131827_131265_131262; H_PS_PSSID=; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1558344337,'
                                 '1558344853,1558344997,1558345360; delPer=0; PSINO=1; locale=zh; Hm_lpvt_64ecd82404c51e03dc91cb9e8c02557'
                                 '4=1558347248; BDRCVFR[-2cV2yayoy0]=wiUTwlWC6HnnHbdnHRdQhPEUf; to_lang_often=%5B%7B%22value%22%3A%22zh%2'
                                 '2%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7'
                                 'D%5D; from_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%'
                                 '22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Mobile Safari/537.36'}
        self.data ={'from': None,'to': None,'query': None,'transtype': 'translang','simple_means_flag': '3',
                    'sign': None,'token': '553dfc32bbc22addba88b48fc2490aad'}

    def get_zh_en(self):
        '''获取输入的语言'''
        url = 'https://fanyi.baidu.com/langdetect'
        data = {'query': self.str}
        print(data)
        r = requests.post(url, data=data, headers= self.header)
        dict_s = json.loads(r.content.decode())
        print(dict_s)
        return dict_s['lan']

    def set_data(self):
        from_s = self.get_zh_en()
        to_s = 'en' if from_s == 'zh' else 'zh'
        with open('baidu.js') as f:
            jsData = f.read()
        sign = execjs.compile(jsData).call('e', self.str)
        self.data['from'] = from_s
        self.data['to'] = to_s
        self.data['sign'] = sign
        self.data['query']=self.str
        return self.data

    def run(self,str):
        self.str=str
        self.str=self.str.replace(' ','')
        r = requests.post(self.url, data=self.set_data(), headers=self.header)
        return  self.end(r)

    def end(self,r):
        dict_r = json.loads(r.content.decode())
        print(dict_r)
        return dict_r['trans_result']['data'][0]['dst']

class OnGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('英汉互译')
        # self.window.geometry('500x300')
        photo = tk.PhotoImage(file='h.gif')
        self.canvas = tk.Canvas(self.window, width=500, height=300)
        self.canvas.create_image(100,100, image=photo)
        self.baidu=BaiDuFanYi()
        self.start()

    def run(self):
        str = self.baidu.run(self.e.get('1.0','end'))
        self.end_str.delete('1.0','end')
        self.end_str.insert('1.0',str)

    def set_input(self):
        l = tk.Label(self.window, text='输入要翻译的内容',bg="DarkGray", font=('Arial', 12), width=15, height=0)
        l.place(x=50, y=10, anchor='nw')
        self.e= tk.Text(self.window, show=None,font=('Arial', 12), width=20, height=10)
        self.e.place(x=20, y=50, anchor='nw')

    def set_button(self):
        b = tk.Button(self.window, text='翻译',bg='DarkGray', font=('Arial', 12), width=5, height=2, command=lambda :self.run())
        b.place(x=220, y=240, anchor='nw')

    def get_result(self):
        l = tk.Label(self.window, text='结果', bg='DarkGray',font=('Arial', 12), width=4, height=0)
        l.place(x=370, y=10, anchor='nw')
        self.end_str = tk.Text(self.window,show=None,font=('Arial', 12), width=20, height=10)
        self.end_str.place(x=300, y=50, anchor='nw')

    def start(self):
        self.set_input()
        self.get_result()
        self.set_button()
        self.canvas.pack()
        self.window.mainloop()

if __name__ =='__main__':
    gui = OnGUI()