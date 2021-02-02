import datetime
ls = []
with open("head.txt","r",encoding='UTF-8') as f:
    for line in f.readlines():
        line = line.strip()
        ls.append(line)
f.close()
g = 0
k = len(ls)
ls.append("<li> <span class ='touxiang'> <img src='https://wx2.sbimg.cn/2020/08/04/PfKBn.jpg' class ='avatar avatar-48 zhuan' width='48' height='48'> </span>")
ls.append("<a class ='cbp_tmlabel' href=''>")

with open("my.txt","r",encoding='UTF-8') as f:
    for line in f.readlines():
        line = line.strip()
        print(line)
        if line == "text":
            g = 1
            ls.append("<p></p>")
        elif line == "img":
            g = 2
            ls.append("<p></p>")
        elif line == "music":
            g = 3
            ls.append("<p></p>")
        elif g == 1:
            if line != '':
                ls.append("<p>"+line+"</p>")
        elif g == 2:
            if line != '':
                ls.append("<p> <img src='"+line+"'></p>")
        elif g == 3:
            if line != '':
                ls.append("<iframe frameborder='no' border='0' marginwidth='0' marginheight='0' width=340 height=86 src='"+line+"'></iframe>")
        elif line != "":
            exit()
f.close()
ls.append("<p>&nbsp;</p>")
ls.append("<p class='shuoshuo_time'><i class='fa fa-clock-o'></i>")
ISOTIMEFORMAT = '%Y-%m-%d %H:%M:%S'
theTime = str(datetime.datetime.now().strftime(ISOTIMEFORMAT))
ls.append(theTime)
ls.append("</p></a></li>")
with open("foot.txt","r",encoding='UTF-8') as f:
    for line in f.readlines():
        line = line.strip()
        ls.append(line)
f.close()
with open("index.md","w",encoding='UTF-8') as f:
    for a in ls:
        f.write(a+'\n')
f.close()
with open("foot.txt","w",encoding='UTF-8') as f:
    for i in range(k,len(ls)):
        f.write(ls[i]+'\n')
f.close()
