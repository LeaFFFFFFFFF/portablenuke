import urllib.request
import urllib.parse
import json
import tkinter as tk
import tkinter.messagebox
from MyQR import myqr
import os
from PIL import Image
import webbrowser

#生成QRcode
myqr.run(words="http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule",
                save_name="code.png",
                version = 1)
IMAGE = Image.open('code.png')
IMG = IMAGE.resize((150,150)).save('code.png')  #尺寸缩放

#窗口主体
class Translate():
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("有路翻译")                                       #定义窗口名称
        self.window.resizable(0,0)
        self.window.protocol("WM_DELETE_WINDOW",self.close_all)             #监听右上角叉，调用函数提示关闭
        self.labelframe_input = tk.LabelFrame(self.window,text = '输入内容')
        self.input = tk.Entry(self.labelframe_input,width = 50)                                                             #输入框
        self.input.focus()                                                                                                  #聚焦输入文本框
        self.labelframe_result = tk.LabelFrame(self.window,text = '翻译结果')                                               #标签框
        self.info = tk.Text(self.labelframe_result,height = 8,width = 50,state = 'disabled',bg = 'WhiteSmoke')              #展示框
        self.label_announcement = tk.Label(self.window,text='使用有道线上翻译，支持多语言自动识别，仅供学习交流使用',fg = 'Red')     #声明标签
        self.label_note = tk.Label(self.window,text='扫我前往手机有道翻译')                    #二维码注释        
        self.t_button = tk.Button(self.window, text = '从有道在线翻译',bg = 'Red',fg = 'white',relief=tk.GROOVE,width = 20,height = 5,command = self.translate_func)                            #翻译按钮
        self.window.bind('<Return>',self.translate_func_enter)
        self.window.bind('<Escape>',self.close_all_esc)
        self.r_button = tk.Button(self.window,text='重新键入',bg = 'Red',fg = 'white',relief=tk.GROOVE, width = 20, height = 2, command = self.cle_e)                                           #清空
        self.q_button = tk.Button(self.window,text='退出',bg = 'Red',fg = 'white',relief=tk.GROOVE,width = 20,height = 2, command = self.close_all)                                             #退出
        self.button_link1 = tk.Button(self.window, text='点击前往有道翻译原网页',bg = 'Black',fg = 'White',relief=tk.GROOVE,width = 77,height = 1, command = self.open_url_1)                      #链接1
        self.button_link2 = tk.Button(self.window, text='觉得自己行了？点击前往CET-4、6报名',bg = 'Black',fg = 'White',relief=tk.GROOVE,width = 77,height = 1, command =self.open_url_2)           #链接2
        self.c_button = tk.Button(self.labelframe_result,text = '复制内容',command = self.copy,width = 51,bg = 'Red',fg = 'white',relief=tk.GROOVE)
        global image_file
        image_file = tk.PhotoImage(file='code.png')
        self.label_Image = tk.Label(self.window,image=image_file)   #二维码
        os.remove('code.png')                                       #调用后删除二维码
        
    #对页面元素布局，设置各部件的位置
    def gui_arrange(self):
        self.input.grid(row = 0,ipadx = 5,ipady = 35,padx = 2)
        self.labelframe_input.grid(row = 0,column = 0,sticky = "N")
        self.labelframe_result.grid(row = 2,column = 0,ipadx = 5,ipady = 8,padx = 2,rowspan = 6,sticky = "N")
        self.info.grid(row = 2,column = 0,ipadx = 5,ipady = 8,padx = 2,rowspan = 6,sticky = "N")
        self.label_announcement.grid(row = 5,column = 0,columnspan = 2,sticky = "N")
        self.label_note.grid(row = 4,column = 1,sticky = "N")
        self.button_link1.grid(row = 6,column = 0,columnspan = 2)
        self.button_link2.grid(row = 7,column = 0,columnspan = 2)
        self.t_button.grid(row = 0,column = 1,padx = 2,rowspan=1,sticky="S")
        self.r_button.grid(row = 1,sticky = "N",column = 1,padx = 2,pady = 1)
        self.q_button.grid(row = 2,column = 1,padx = 2,pady = 1)
        self.c_button.grid(row = 8,column = 0,sticky="S")
        self.label_Image.grid(row = 3,column = 1,padx = 1,pady = 1,sticky="N"+"S")
        
    #翻译函数本体
    def translate_func(self):
        try:
            original_str = self.input.get()
            url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule"
            data = {
            'i':self,
            'from':'AUTO',
            'to':'AUTO',
            'smartresult':'dict',
            'client':'fanyideskweb',
            'doctype':'json',
            'i': original_str
            }                                   #网页字典data
            
            myheaders = {
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36 Maxthon/5.2.7.5000'
                }                               #伪造headers
            
            data = urllib.parse.urlencode(data).encode('utf-8')                     #用utf-8编码，用urllib.parse模块分析
            request = urllib.request.Request(url,data,myheaders)
            response = urllib.request.urlopen(request)
            html = response.read().decode('utf-8')
            result = json.loads(html)
            translate_result = result['translateResult'][0][0]["tgt"]
            self.info.config(state = 'normal')
            self.info.delete(1.0,"end")                                             #输出翻译内容前，先清空输出框的内容
            self.info.insert('end',translate_result)                                #将翻译结果添加到输出框中
            self.info.config(state = 'disabled')
        except:
            tkinter.messagebox.showwarning(title='空值拦截', message='请输入内容')  #异常捕获拦截空值
            
    def translate_func_enter(self,event):
        self.translate_func()
    
    def open_url_1(self):
        webbrowser.open("http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule", new=0)
    def open_url_2(self):
        webbrowser.open("http://cet-bm.neea.edu.cn/", new=0)

    #复制按钮功能
    def copy(self):
        self.info.config(state = 'normal')
        self.info.clipboard_append(''.join(self.info.get(1.0,"end")))
        self.info.config(state = 'disabled')
        
    #清空输入输出框的内容
    def cle_e(self):
        self.info.config(state = 'normal')
        self.info.delete(1.0,"end")
        self.input.delete(0,"end")
        self.info.config(state = 'disabled')

    #定义退出提示
    def close_all(self):
        a=tkinter.messagebox.askyesno('提示', '是否退出此程序？')
        if a == True:
            self.window.destroy()
        else:
            tk.mainloop()

    def close_all_esc(self,event):
        self.close_all()
    
#----------类定义结束-----------
        
def main():     #主程序
        t = Translate()
        t.gui_arrange()
        tk.mainloop()

if __name__ == '__main__':
    main()
