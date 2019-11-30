#!/usr/bin/python3
import pygame,random,os,subprocess
import easygui,pickle

from pygame.locals import *
from sys import exit
from functools import cmp_to_key

colorchoices=[("拯救 Chtholly",(96,158,215),(218,7,48)),
              ("Vocaloid",(57,197,187),(102,204,255)),
              ("AK IOI",(82,196,26),(231,76,60))]
ccaptions=["拯救 Chtholly","翻转棋 - Vocaloid","AK IOI"]
ccursucc1s=["你成功地拯救了 Chtholly！\n你的分数是%f分。","成功了！\n你的分数是%f分。","Accepted! \n你的分数是%f分。"]
ccursucc2s=["成为了勇者！这位勇者的姓名是：","高分！请问尊姓大名：","You AK IOI！请在 OI 史上留下姓名："]
ccursucc3s=["Willem Kmetsch","百万调音师","三中神犇"]
ccurnohighscores=["还没有勇者来到这个悬浮岛！","当前大小的棋盘尚无高分！","这片赛场上还没有人 AK IOI！"]
ccurhighscore1s=["第 %d 位勇者  %s  %f 级  总步数 %d 步","第 %d 名  %s  %f 分  总步数 %d 步","第 %d 位神犇  %s  %f 分  总步数 %d 步"]
ccurhighscore2s=["这里的勇者不足 3 人，继续努力！","高分不足 3 人，继续努力！","AK IOI 的神犇不足 3 人，继续努力！"]
cbgpaths=["chtholly.png","miku3.png","noi.png"]

colors=list()

n=5
m=5
wid=800
hei=600
blhei,blwid,sphei,spwid=0,0,0,0
sxpos=int(0.05*hei)
sypos=int(0.05*hei)
expos=int(0.95*hei)
eypos=int(0.95*hei)
has_done,unfi,bstst=0,0,0
shadowi,shadowj=-1,-1
tipx,tipy=-1,-1
istip=0
nowcolor=0
button_pos=[Rect(665,210,130,70),Rect(665,300,130,70),Rect(665,390,130,70),Rect(665,480,130,70)]
button_text=["重新开始","设置","高分","关于"]
highscores=dict()
buildsys="Windows" # Change this to "Windows" or "Linux"

curcaption="翻转棋"
cursucc1="成功了！\n你的分数是%f分。"
cursucc2="高分！请问尊姓大名："
cursucc3="三中神犇"
curnohighscore="当前大小的棋盘尚无高分！"
curhighscore1="第 %d 名  %s  %f 分  总步数 %d 步"
curhighscore2="高分不足 3 人，继续努力！"
curbackground=pygame.surface.Surface((wid,hei))

def filledRoundedRect(surface,rect,color,radius=0.3):
    """
    filledRoundedRect(surface,rect,color,radius=0.3)

    surface : destination
    rect    : rectangle
    color   : rgb or rgba
    radius  : 0 <= radius <= 1
    """

    rect         = Rect(rect)
    color        = Color(*color)
    alpha        = color.a
    color.a      = 0
    pos          = rect.topleft
    rect.topleft = 0,0
    rectangle    = pygame.Surface(rect.size,SRCALPHA)

    circle       = pygame.Surface([min(rect.size)*3]*2,SRCALPHA)
    pygame.draw.ellipse(circle,(0,0,0),circle.get_rect(),0)
    circle       = pygame.transform.smoothscale(circle,[int(min(rect.size)*radius)]*2)

    radius              = rectangle.blit(circle,(0,0))
    radius.bottomright  = rect.bottomright
    rectangle.blit(circle,radius)
    radius.topright     = rect.topright
    rectangle.blit(circle,radius)
    radius.bottomleft   = rect.bottomleft
    rectangle.blit(circle,radius)

    rectangle.fill((0,0,0),rect.inflate(-radius.w,0))
    rectangle.fill((0,0,0),rect.inflate(0,-radius.h))

    rectangle.fill(color,special_flags=BLEND_RGBA_MAX)
    rectangle.fill((255,255,255,alpha),special_flags=BLEND_RGBA_MIN)

    return surface.blit(rectangle,pos)

def set_color(ti):
    global colors,colorchoices,nowcolor,curcaption,cursucc1,cursucc2,cursucc3
    global curnohighscore,curhighscore1,curhighscore2,curbackground
    if ti is None:
        return
    nowcolor=ti
    color0,color1=colorchoices[ti][1:]
    tlamb=1.1
    ccolor0=tuple(map(lambda x:int(min(255,x*tlamb)),color0))
    ccolor1=tuple(map(lambda x:int(min(255,x*tlamb)),color1))
    colors=[color0,color1,ccolor0,ccolor1]
    curcaption=ccaptions[ti]
    cursucc1=ccursucc1s[ti]
    cursucc2=ccursucc2s[ti]
    cursucc3=ccursucc3s[ti]
    pygame.display.set_caption(curcaption)
    curnohighscore=ccurnohighscores[ti]
    curhighscore1=ccurhighscore1s[ti]
    curhighscore2=ccurhighscore2s[ti]
    curbackground=pygame.image.load(cbgpaths[ti])

def all_redraw():
    global swindow
    swindow.blit(curbackground,(0,0))
    draw_flag()
    for i in range(len(button_pos)):
        draw_button(button_pos[i],button_text[i])

def change_nm():
    global blhei,blwid,sphei,spwid
    global grid,has_done,unfi,bstst
    global tipx,tipy
    blhei=int((eypos-sypos)*5/(6*n-1))
    blwid=int((expos-sxpos)*5/(6*m-1))
    sphei=int(blhei/5)
    spwid=int(blwid/5)
    grid=list()
    for i in range(n):
        tl=list()
        for j in range(m):
            tl.append(0)
        grid.append(tl)
    tdraw()
    for tries in range(40):
        change_5_color(random.randint(0,n-1),random.randint(0,m-1))
    tresult=getans()
    bstst=tresult[0]
    tipx,tipy=tresult[1]
    while not bstst:
        if n==1 and m==1:
            change_5_color(0,0)
        else:
            for tries in range(random.randint(1,10)):
                change_5_color(random.randint(0,n-1),random.randint(0,m-1))
        tresult=getans()
        bstst=tresult[0]
        tipx,tipy=tresult[1]
    has_done=0
    unfi=count_unf()
    
    draw_text(Rect(665,135,130,70),"%d"%has_done)
    

def getpos(i,j):
    global blhei,blwid,sphei,spwid
    return Rect(sxpos+(blwid+spwid)*j,sypos+(blhei+sphei)*i,blwid,blhei)

def draw(i,j,col):
    global colors,swindow
    filledRoundedRect(swindow,getpos(i,j),colors[col])

def tdraw():
    global grid,swindow
    #swindow.fill((255,255,255),Rect(0,0,hei,hei))
    swindow.blit(curbackground.subsurface(Rect(0,0,hei,hei)),(0,0))
    for i in range(n):
        for j in range(m):
            draw(i,j,grid[i][j])

def set_shadow(ui,uj,istotip):
    global shadowi,shadowj,grid,istip
    if (shadowi==ui and shadowj==uj) or istip:
        return
    if shadowi>=0 and shadowj>=0:
        ti,tj=shadowi,shadowj
        if ti>0:
            draw(ti-1,tj,grid[ti-1][tj])
        if tj>0:
            draw(ti,tj-1,grid[ti][tj-1])
        if ti<n-1:
            draw(ti+1,tj,grid[ti+1][tj])
        if tj<m-1:
            draw(ti,tj+1,grid[ti][tj+1])
        draw(ti,tj,grid[ti][tj])
    shadowi=ui
    shadowj=uj
    if shadowi>=0 and shadowj>=0:
        ti,tj=shadowi,shadowj
        if ti>0:
            draw(ti-1,tj,grid[ti-1][tj]+2)
        if tj>0:
            draw(ti,tj-1,grid[ti][tj-1]+2)
        if ti<n-1:
            draw(ti+1,tj,grid[ti+1][tj]+2)
        if tj<m-1:
            draw(ti,tj+1,grid[ti][tj+1]+2)
        draw(ti,tj,grid[ti][tj]+2)
    if istotip:
        istip=1

def draw_button(pos,text,egsz=3,fsize=30):
    global swindow
    filledRoundedRect(swindow,pos,(144,144,144))
    pos.inflate_ip(-egsz,-egsz)
    filledRoundedRect(swindow,pos,(255,255,255))
    tfont=pygame.font.Font("simsun.ttf",fsize)
    text_surface=tfont.render(text,True,(0,0,0))
    swindow.blit(text_surface,
    (int(pos.centerx-text_surface.get_width()/2),
    int(pos.centery-text_surface.get_height()/2)))

def draw_text(pos,text,fsize=30):
    global swindow
    #swindow.fill((255,255,255),pos)
    swindow.blit(curbackground.subsurface(pos),(pos.left,pos.top))
    tfont=pygame.font.Font("simsun.ttf",fsize)
    text_surface=tfont.render(text,True,(0,0,0))
    swindow.blit(text_surface,
    (int(pos.centerx-text_surface.get_width()/2),
    int(pos.centery-text_surface.get_height()/2)))

def draw_flag():
    global swindow
    tdx=10
    tdy=-10
    #swindow.fill((255,255,255),Rect(705+tdx,50+tdy,60,100))
    swindow.blit(curbackground.subsurface(Rect(700+tdx,50+tdy,60,100)),(700+tdx,50+tdy))
    pygame.draw.polygon(swindow,colors[0],[(700+tdx,50+tdy),(700+tdx,150+tdy),
                                           (705+tdx,150+tdy),(705+tdx,50+tdy)],0)
    pygame.draw.polygon(swindow,colors[0],[(700+tdx,50+tdy),(700+tdx,100+tdy),(760+tdx,80+tdy)],0)

def search_pos(tx,ty):
    currect=Rect(tx,ty,0,0)
    for i in range(n):
        for j in range(m):
            trect=getpos(i,j)
            if trect.contains(currect):
                return (i,j,)
    for i in range(len(button_pos)):
        trect=button_pos[i]
        if trect.contains(currect):
            return (-2,i)
    tdx=10
    tdy=-10
    trect=Rect(705+tdx,50+tdy,60,100)
    if trect.contains(currect):
        return (-3,0)
    return (-1,-1,)

def change_5_color(ti,tj):
    global grid
    change_color(ti,tj)
    if ti>0:
        change_color(ti-1,tj)
    if tj>0:
        change_color(ti,tj-1)
    if ti<n-1:
        change_color(ti+1,tj)
    if tj<m-1:
        change_color(ti,tj+1)
        

def change_color(ti,tj):
    global grid
    grid[ti][tj]=1-grid[ti][tj]
    draw(ti,tj,grid[ti][tj])

def getans():
    fin=open("flip.in","w")
    fin.write("%d %d\n"%(n,m))
    for i in range(n):
        for j in range(m):
            fin.write("%d "%(grid[i][j]))
        fin.write("\n")
    fin.close()

    if buildsys=="Windows":
        subprocess.run("solve.exe",shell=True,
                       stdin=subprocess.PIPE,stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
    else:
        os.system("./solve")
    
    fans=open("flip.out","r")
    steps=int(fans.readline())
    todo_st=(-1,-1)
    if steps:
        for i in range(n):
            thisline=fans.readline().split(' ')
            for j in range(m):
                if thisline[j].strip()=='1':
                    todo_st=(i,j)
                    break
            if todo_st[0]>=0:
                break
    fans.close()

    if buildsys=="Windows":
        subprocess.run("del flip.in",shell=True,
                       stdin=subprocess.PIPE,stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
        subprocess.run("del flip.out",shell=True,
                       stdin=subprocess.PIPE,stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
    else:
        os.system("rm ./flip.in")
        os.system("rm ./flip.out")
    return (steps,todo_st)

def count_unf():
    tans=0
    for i in range(n):
        for j in range(m):
            tans+=grid[i][j]
    return tans

def mycmp(tup1,tup2):
    #Score
    if tup1[1]>tup2[1]:
        return -1
    if tup1[1]<tup2[1]:
        return 1
    #Steps
    if tup1[2]>tup2[2]:
        return -1
    return 1

def fgethighscore():
    global highscores
    with open("highscore.rec","rb") as f:
        highscores=pickle.load(f)

def fwritehighscore():
    global highscores
    with open("highscore.rec","wb") as f:
        pickle.dump(highscores,f)

def frestart():
    change_nm()

def fsetting():
    global n,m,nowcolor
    nn=easygui.integerbox(msg="自定义行数:",default=n,title="设置",lowerbound=1,upperbound=15)
    if nn:
        n=nn
    mm=easygui.integerbox(msg="自定义列数:",default=m,title="设置",lowerbound=1,upperbound=15)
    if mm:
        m=mm
    colorc=[x[0] for x in colorchoices]
    tchoice=easygui.choicebox(msg="选择主题",title="设置",choices=colorc,preselect=nowcolor)
    if tchoice in colorc:
        set_color(colorc.index(tchoice))
    #print(nowcolor)
    all_redraw()
    change_nm()


def fhighscore():
    if (n,m,) not in highscores.keys():
        highscore_window=easygui.msgbox(msg=curnohighscore,title="高分")
        return
    highscore_lst=[]
    tlst=highscores[(n,m,)]
    for i in range(len(tlst)):
        highscore_lst.append(curhighscore1%(i+1,tlst[i][0],tlst[i][1],tlst[i][2]))
    if len(highscore_lst)<3:
        highscore_lst.append(curhighscore2)
    highscore_window=easygui.choicebox(msg="高分",title="高分",choices=highscore_lst)

def fabout():
    about_window=easygui.msgbox(msg=
    """制作:Sweetlemon
版本号:0.3.4 %s build"""%(buildsys),title="关于")

def fgame_over():
    global bstst,has_done
    pygame.display.update()
    tscore=100*bstst/has_done
    congra=easygui.msgbox(msg=cursucc1%(tscore),title="成功")
    if (n,m,) in highscores.keys():
        tlst=highscores[(n,m,)]
    else:
        tlst=list()
    curscore=["Sweetlemon",tscore,has_done]
    if len(tlst)<3 or mycmp(tuple(curscore),tlst[-1])<0:
        player_name=easygui.enterbox(msg=cursucc2,title="高分",default=cursucc3)
        curscore[0]=player_name
        if len(tlst)<3:
            tlst.append(tuple(curscore))
        else:
            tlst[-1]=tuple(curscore)
        tlst=sorted(tlst,key=cmp_to_key(mycmp))
        highscores[(n,m,)]=tlst
        fwritehighscore()
    change_nm()

button_funcs=[frestart,fsetting,fhighscore,fabout]

def handle_buttons(buttoni):
    button_funcs[buttoni]()

def main():
    global swindow,has_done,bstst,unfi,tipx,tipy,istip
    pygame.init()
    swindow=pygame.display.set_mode((wid,hei),0,32)
    set_color(0)
    pygame.display.set_caption(curcaption)
    fgethighscore()
    
    all_redraw()
    change_nm()
    pygame.display.update()
    tresult=getans()
    #print(tresult[0])
    tipx,tipy=tresult[1]
    pygame.event.set_allowed((QUIT,MOUSEBUTTONDOWN,MOUSEBUTTONUP,MOUSEMOTION))
    while 1:
        for event in pygame.event.get():
            #print(event)
            if event.type==QUIT:
                pygame.quit()
                exit()
            if event.type==MOUSEBUTTONDOWN:
                if event.button==1:
                    ti,tj=search_pos(*event.pos)
                    if ti>=0 and tj>=0:
                        change_5_color(ti,tj)
                        has_done+=1
                        tresult=getans()
                        #print(tresult[0])
                        tipx,tipy=tresult[1]
                        draw_text(Rect(665,135,130,70),"%d"%has_done)
                        unfi=count_unf()
                        if not unfi:
                            fgame_over()
                            continue
                    if ti==-2:
                        handle_buttons(tj)
                    if ti==-3:
                        istip=0
                        set_shadow(tipx,tipy,1)
            if event.type==MOUSEMOTION:
                set_shadow(*search_pos(*event.pos),0)
            if event.type==MOUSEBUTTONUP and event.button==1 and istip:
                istip=0
                set_shadow(-1,-1,0)
        pygame.display.update()
if __name__=="__main__":
    main()
