# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 11:18:07 2023
@author: joeyzong256
"""

'''
#隐藏控制台
import win32gui
import win32console

win = win32console.GetConsoleWindow()
win32gui.ShowWindow(win, 0)
'''

use_sample=True #是否使用范例
design=2 #界面配色 0-13 推荐：2
#是使用PPT范例，否则读取数据

import tkinter as tk
import ttkbootstrap as tkb

#界面设计


stylename=['cyborg', 'journal', 
'darkly', 'flatly', 'solar', 
'minty', 'litera', 'united', 
'pulse', 'cosmo', 'lumen', 'yeti', 
'superhero', 'sandstone']
style = tkb.Style()
style = tkb.Style(theme=stylename[design])
TOP6 = style.master


# 操作主窗口
root = tk.Tk()
root.title("ERP 企业资源管理系统                                                                                                               by 21013124 JOEYZONG256") #窗口标题
root.iconbitmap("logo.jpg") #企业图标
root.geometry("810x470") #窗口大小
root.resizable(False, False) #窗口大小不可改变
#root.config(bg="blue") #背景颜色

temppasser=[0]

#BOM菜单
BOMmenu=tk.LabelFrame(height=450,width=250,text="BOM物料选单")#菜单框架
BOMmenu.place(x=10,y=0)
BOM=[]

def _isin_BOM(name):
    for i in range(len(BOM)):
        if(name==BOM[i][1]):
            return True
    return False

'''
    BOM[i]=[物料号,物料名称,单位,[工序库存，资材库存],
            [损耗率,作业提前期,[[子物料，子物料数量]]],
            [配料损耗率,配料提前期,供应商损耗率,供应商提前期]]
    BOM[i][4]=[] 表示无法生产/无相关信息
    BOM[i][5]=[] 表示无法采购/无相关信息
'''
BOMselected=None#当前选择的BOM表行

from tkinter import messagebox

def _showmaterial(index):
    p=BOM[index]
    route="生产"
    if(p[4][1]==0):
        route="采购"
    return p[0]+"||"+p[1]+"||"+p[2]+"||"+route

def add_material():
    material = material_entry.get()#获取输入的名称
    #if (_isin_BOM(material)==False):
     #   messagebox.showwarning("警告", "物料表中没有此物料")
     #   return
    if(material=="物料"):
        messagebox.showwarning("警告", "物料名称不能为\"物料\"")
        return
    if material:#判空
        for i in range(len(BOM)):
            if(BOM[i][1]==material):
                messagebox.showwarning("警告", "请给同名的不同物料不同名字")
                return
        BOM.append(["未编号",material,"个",[0,0],[0,0,[]],[0,0,0,0]])
        materials_listbox.insert(tk.END, _showmaterial(len(BOM)-1))
        material_entry.delete(0, tk.END)
        save()
        print("添加物料到主BOM表：")
        print(BOM[-1])
        loadBOM()
    else:
        messagebox.showwarning("警告", "请输入物料名称！")
    return

def remove_material():
    selected_index = materials_listbox.curselection()
    if selected_index:
        print("从主BOM表中删除：")
        materials_listbox.delete(selected_index)
        for num in selected_index:
            print(BOM[num])
            del BOM[num]
        loadBOM()
        #print(BOM)
        

# 输入框和按钮

label_material_1=tk.Label(text="物料名称:")
label_material_1.place_configure(x=20,y=30)

material_entry = tk.Entry(root)
material_entry.place_configure(x=95,y=30)

add_button = tk.Button(root, text="添加物料", command=add_material)
add_button.place_configure(x=20,y=60)

remove_button = tk.Button(root, text="删除物料", command=remove_material)
remove_button.place_configure(x=100,y=60)

#原材料列表框
materials_listbox = tk.Listbox(root,height=18,width=31)
materials_listbox.place_configure(x=20,y=110)                                                                                                                                                                                                                                                                                                                                                                                                                                                           

def loadBOM():
    materials_listbox.delete(0,tk.END)
    for i in range(len(BOM)):
        materials_listbox.insert(tk.END, _showmaterial(i))
    calculate()
    print("已更新主BOM表")

#Minfo——————————————————————————————————————————————————
smtable=[[]]

Minfomenu=tk.LabelFrame(height=450,width=250,text="BOM物料信息")#菜单框架
Minfomenu.place(x=280,y=0)

mNo=tk.Label(text="物料编号:")
mNo.place_configure(x=290,y=30)

mNo_entry = tk.Entry(root)
mNo_entry.place_configure(x=365,y=30)

mName=tk.Label(text="物料名称:")
mName.place_configure(x=290,y=60)

mName_entry = tk.Entry(root)
mName_entry.place_configure(x=365,y=60)

sm=tk.Label(text="子料名称:                       数量:")
sm.place_configure(x=290,y=90)

sm_entry = tk.Entry(root,width=8)
sm_entry.place_configure(x=365,y=90)

sm_num_entry = tk.Entry(root,width=5)
sm_num_entry.place_configure(x=470,y=90)


#子物料调整按钮

def add_submaterial():
    new_sm_name=sm_entry.get()
    new_sm_num=sm_num_entry.get()
    if (_isin_BOM(new_sm_name)==False):
        messagebox.showwarning("警告", "物料表中没有此物料")
        return
    if(new_sm_name and new_sm_num):
        smtable[0].append([new_sm_name,int(new_sm_num)])
        submaterials_listbox.insert(tk.END, new_sm_name+"||"+new_sm_num)
        sm_entry.delete(0, tk.END)
        sm_num_entry.delete(0, tk.END)
        print("子物料缓冲区更新：")
        print(smtable[0])
    else:
        messagebox.showwarning("警告", "请输入子物料名称和数量！")
    return

def remove_submaterial():
    selected_index = submaterials_listbox.curselection()
    if selected_index:
        del smtable[0][list(selected_index)[0]]
        print("子物料缓冲区更新：")
        print(smtable[0])
        submaterials_listbox.delete(list(selected_index)[0])

smadd_button = tk.Button(root, text="添加子物料", command=add_submaterial,width=14)
smadd_button.place_configure(x=290,y=220)

smremove_button = tk.Button(root, text="删除子物料", command=remove_submaterial,width=14)
smremove_button.place_configure(x=400,y=220)

#子物料列表框
submaterials_listbox = tk.Listbox(root,height=5,width=31)
submaterials_listbox.place_configure(x=290,y=120)                                                                                                                                                                                                                                                                                                                                                                                                                                                  

mnum_manufact=tk.Label(text="工序储量:")
mnum_manufact.place_configure(x=290,y=260)

mnum_manufact_entry = tk.Entry(root)
mnum_manufact_entry.place_configure(x=365,y=260)

mnum_warehouse=tk.Label(text="资材储量:")
mnum_warehouse.place_configure(x=290,y=290)

mnum_warehouse_entry = tk.Entry(root)
mnum_warehouse_entry.place_configure(x=365,y=290)

mlt_worktime=tk.Label(text="作业提前期:                    损耗:")
mlt_worktime.place_configure(x=290,y=320)

mlt_worktime_entry = tk.Entry(root,width=7)
mlt_worktime_entry.place_configure(x=370,y=320)

mlt_worktime_loss_entry = tk.Entry(root,width=4)
mlt_worktime_loss_entry.place_configure(x=470,y=320)

mlt_ingretime=tk.Label(text="配料提前期:                    损耗:")
mlt_ingretime.place_configure(x=290,y=350)

mlt_ingretime_loss_entry = tk.Entry(root,width=4)
mlt_ingretime_loss_entry.place_configure(x=470,y=350)

mlt_ingretime_entry = tk.Entry(root,width=7)
mlt_ingretime_entry.place_configure(x=370,y=350)

mlt_providetime=tk.Label(text="供应商提前期:                 损耗:")
mlt_providetime.place_configure(x=290,y=380)

mlt_providetime_entry = tk.Entry(root,width=7)
mlt_providetime_entry.place_configure(x=370,y=380)

mlt_providetime_loss_entry = tk.Entry(root,width=4)
mlt_providetime_loss_entry.place_configure(x=470,y=380)

def saveinfo():
    BOMselected=temppasser[0]
    BOM[BOMselected][0]=mNo_entry.get()
    BOM[BOMselected][1]=mName_entry.get()
    BOM[BOMselected][3][0]=int(mnum_manufact_entry.get())
    BOM[BOMselected][3][1]=int(mnum_warehouse_entry.get())
    BOM[BOMselected][5][1]=int(mlt_ingretime_entry.get())
    BOM[BOMselected][5][0]=float(mlt_ingretime_loss_entry.get())
    BOM[BOMselected][5][3]=int(mlt_providetime_entry.get())
    BOM[BOMselected][5][2]=float(mlt_providetime_loss_entry.get())
    BOM[BOMselected][4][1]=int(mlt_worktime_entry.get())
    BOM[BOMselected][4][0]=float(mlt_worktime_loss_entry.get())
    BOM[BOMselected][4][2]=smtable[0]
    print(BOM[BOMselected])
    save()
    loadBOM()
    return

msave_botton= tk.Button(root, text="保存物料信息", command=saveinfo,width=30)
msave_botton.place_configure(x=290,y=410)

#连接两表的按钮


def info_material():
    #重置输入框为选择信息
    BOMselected=list(materials_listbox.curselection())[0]
    print("从主BOM表中提取信息：")
    print(BOM[BOMselected])
    temppasser[0]=BOMselected
    mNo_entry.delete(0,tk.END)
    mName_entry.delete(0,tk.END)
    sm_entry.delete(0,tk.END)
    sm_num_entry.delete(0,tk.END)
    mnum_manufact_entry.delete(0,tk.END)
    mnum_warehouse_entry.delete(0,tk.END)
    mlt_ingretime_entry.delete(0,tk.END)
    mlt_ingretime_loss_entry.delete(0,tk.END)
    mlt_providetime_entry.delete(0,tk.END)
    mlt_providetime_loss_entry.delete(0,tk.END)
    mlt_worktime_entry.delete(0,tk.END)
    mlt_worktime_loss_entry.delete(0,tk.END)
    mNo_entry.insert(0,BOM[BOMselected][0])
    mName_entry.insert(0,BOM[BOMselected][1])
    mnum_manufact_entry.insert(0,BOM[BOMselected][3][0])
    mnum_warehouse_entry.insert(0,BOM[BOMselected][3][1])
    mlt_ingretime_entry.insert(0,BOM[BOMselected][5][1])
    mlt_ingretime_loss_entry.insert(0,BOM[BOMselected][5][0])
    mlt_providetime_entry.insert(0,BOM[BOMselected][5][3])
    mlt_providetime_loss_entry.insert(0,BOM[BOMselected][5][2])
    mlt_worktime_entry.insert(0,BOM[BOMselected][4][1])
    mlt_worktime_loss_entry.insert(0,BOM[BOMselected][4][0])
    #print(BOM[BOMselected][1])
    
    #子物料输入框
    submaterials_listbox.delete(0,tk.END)
    for i in range(len(BOM[BOMselected][4][2])):
        submaterials_listbox.insert(tk.END,BOM[BOMselected][4][2][i][0]+"||"+str(BOM[BOMselected][4][2][i][1]))
        
    #子物料缓冲区更新 
    print("子物料缓冲区更新：")
    smtable[0]=BOM[BOMselected][4][2]
    print(smtable[0])
    return


chose_botton = tk.Button(root, text="选择物料", command=info_material)
chose_botton.place_configure(x=180,y=60)

#MPS菜单————————————————————————————————————————————————————————
MPS=[]

MPSmenu=tk.LabelFrame(height=260,width=250,text="MPS主生产计划")#菜单框架
MPSmenu.place(x=550,y=0)

"""
MPS=[[产品名称，开始时间，需求数量]]
"""

mpsmName=tk.Label(text="产品名称:")
mpsmName.place_configure(x=560,y=30)

mpsmName_entry = tk.Entry(root)
mpsmName_entry.place_configure(x=635,y=30)

mpsmDate=tk.Label(text="完工日期:")
mpsmDate.place_configure(x=560,y=60)

mpsmDate_entry = tk.Entry(root)
mpsmDate_entry.place_configure(x=635,y=60)

mpsmNum=tk.Label(text="产品数量:")
mpsmNum.place_configure(x=560,y=90)

mpsmNum_entry = tk.Entry(root)
mpsmNum_entry.place_configure(x=635,y=90)

mps_listbox = tk.Listbox(root,height=5,width=31)
mps_listbox.place_configure(x=560,y=120)

def loadMPS():
    mps_listbox.delete(0,tk.END)
    for i in range(len(MPS)):
        mps_listbox.insert(tk.END, MPS[i][0]+"||"+MPS[i][1]+"||"+MPS[i][2])
    calculate()
    print("已更新主MPS表")

def add_mps():
    mpsmDate=mpsmDate_entry.get()
    mpsmName=mpsmName_entry.get()
    mpsmNum=mpsmNum_entry.get()
    if (_isin_BOM(mpsmName)==False):
        messagebox.showwarning("警告", "物料表中没有此物料")
        return
    if(mpsmDate and mpsmName and mpsmNum):
        mps_listbox.insert(tk.END,mpsmName+"||"+mpsmDate+"||"+mpsmNum)
        mpsmDate_entry.delete(0, tk.END)
        mpsmName_entry.delete(0, tk.END)
        mpsmNum_entry.delete(0, tk.END)
        MPS.append([mpsmName,mpsmDate,mpsmNum])
        save()
        loadMPS()
    else:
        messagebox.showwarning("警告", "请输入产品具体信息名称！")
    return

def remove_mps():
    selected_indexmps = mps_listbox.curselection()
    #print(selected_indexmps)
    if selected_indexmps:
        mps_listbox.delete(selected_indexmps)
        del MPS[list(selected_indexmps)[0]]
    loadMPS()

smadd_button = tk.Button(root, text="添加到MPS", command=add_mps,width=14)
smadd_button.place_configure(x=560,y=220)

smremove_button = tk.Button(root, text="从MPS删除", command=remove_mps,width=14)
smremove_button.place_configure(x=670,y=220)

#Command——————————————————————————————————————————————————-————-——
Command=tk.LabelFrame(height=190,width=250,text="企业日程表")#菜单框架
Command.place(x=550,y=260)

command_listbox = tk.Listbox(root,height=8,width=31)
command_listbox.place_configure(x=560,y=285) 

import copy

def get_material(name):
    for i in range(len(BOM)):
        if(BOM[i][1]==name):
            return BOM[i]
    messagebox.showwarning("警告", "物料表中缺少子物料")
    return None

def calculate():
    """
    BOM[i]=[物料号,物料名称,单位,[工序库存，资材库存],
            [损耗率,作业提前期,[[子物料，子物料数量]]],
            [配料损耗率,配料提前期,供应商损耗率,供应商提前期]]
    MPS=[[产品名称,开始时间,需求数量]]
    """
    
    b=copy.deepcopy(BOM)
    
    graph=[]
    
    #生成材料的有向无环图（边）
    for i in range(len(b)):
        for j in range(len(b[i][4][2])):
            graph.append([b[i][1],b[i][4][2][j][0]])
            
    #拓扑排序
    sortnode=[]#按照拓扑排序从高级到初级排列物料
    while(graph!=[]):
        for i in range(len(b)):
            flag=0
            for j in range(len(graph)):
                if(b[i][1]==graph[j][1]): #检查节点是否存在入度
                    flag=1 #存在入度
                    break
            if(flag!=1):#如果节点不存在入度
                j=0
                while(j<len(graph)):
                    if(b[i][1]==graph[j][0]):
                        del graph[j] #删除该节点的出度
                    else:j+=1
            sortnode.append(b[i][1])
    
    
    #提前期计算函数
    import datetime as dt
    def novel_time(txt,days):
        txt=txt.split("-")
        a=dt.date(int(txt[0]),int(txt[1]),int(txt[2]))
        return str(a-dt.timedelta(days))
        
    #按照MPS使用DFS得到一个生成森林
    
    treenode=[]#[[唯一节点号,名称,日期,需求量,[路径节点号,.]]]
    uniqueno=[0] #唯一节点号流水
    
    #dfs算法主体
    def dfs(name,date,num,route):
        temp=get_material(name)#获取当前材料的BOM信息
        if(temp[4][1]==0):#判断采购还是生产
            num=int(float(num)*(1+temp[5][0])*(1+temp[5][2])+0.99) #采购计算需求货物量
        else:num=int(float(num)*(1+temp[4][0])) #生产计算需求货物量
        treenode.append([uniqueno[0],name,date,num,copy.deepcopy(route)]) #结果保存到表
        route.append(uniqueno)#递 路径数据
        for i in range(len(temp[4][2])):
            uniqueno[0]+=1
            dfs(temp[4][2][i][0],novel_time(date, temp[4][1]),(num*temp[4][2][i][1]),route)
        del route[-1]#归 路径数据
    
    #对每一个MPS元素生成一棵树
    for i in range(len(MPS)):
        dfs(MPS[i][0],MPS[i][1],MPS[i][2],[])
        
    #把森林的所有节点按照时间排序
    def time(txt):
        txt=txt.split("-")
        a=dt.date(int(txt[0]),int(txt[1]),int(txt[2]))
        return a
    
    def _is_before(time1,time2):#time1 before time2
        time1=time(time1)
        time2=time(time2)
        a=time1-time2
        if(a==a.__abs__()):
            return False
        return True
    
    for i in range(len(treenode)):
        mindate=treenode[i][2]
        minnodenum=[i]
        for j in range(i,len(treenode)):
            if(_is_before(treenode[j][2], mindate)):
                mindate=treenode[j][2]
                minnodenum[0]=j
        temp=treenode[i]
        treenode[i]=treenode[minnodenum[0]]
        treenode[minnodenum[0]]=temp
    
    #获取仓库列表：
    warehouse=[]#[工库，资库]
    for i in range(len(sortnode)):
        warehouse.append([sortnode[i]]+copy.copy(get_material(sortnode[i])[3]))
    
    #开始生产ERP计划
    command=[]
    
    #分配仓储流程 按照拓扑排序从高级到初级的物料按照需求时间先后取货
    for i in range(len(sortnode)):
        j=0
        while(j<len(treenode)):#[[唯一节点号,名称,日期,需求量,[路径节点号,.]]]
            if(sortnode[i]==treenode[j][1]):
                if(treenode[j][3]<=warehouse[i][1]+warehouse[i][2]):#如果仓库材料足够
                    if(treenode[j][3]<=warehouse[i][1]):#如果工序仓库材料足够
                        warehouse[i][1]-=treenode[j][3]#从工序仓库取材料
                    else:
                        command.append([str(novel_time(treenode[j][2], get_material(treenode[j][1])[5][1])),"从资材仓库中取物料"+treenode[j][1]+str((treenode[j][3]-warehouse[i][1]))+"件到工序仓库"])
                        warehouse[i][2]-=treenode[j][3]-warehouse[i][1]#从资材仓库取材料
                        warehouse[i][1]==0
                    #它和所有途径它的子进程都取消
                    unj=treenode[j][0]
                    del treenode[j]
                    t=0
                    while(t<len(treenode)):
                        if(unj in treenode[t][4]):
                            del treenode[t]
                            if(t<j):
                                j-=1
                        else:t+=1
                elif(treenode[j][3]>warehouse[i][1]+warehouse[i][2]):
                    treenode[j][3]-=warehouse[i][1]+warehouse[i][2]
                    if(warehouse[i][1]!=0):
                        print(get_material(treenode[j][1])[4][1])
                        command.append([str(novel_time(treenode[j][2], get_material(treenode[j][1])[5][1])),"从资材仓库中取物料"+treenode[j][1]+str((warehouse[i][2]))+"件到工序仓库"])
                    break
            else:
                j+=1
                break
    
    #合并相同的采购或生产
    i=0
    while(i<len(treenode)):
        j=i+1
        while(j<len(treenode)):
            if(treenode[i][1]==treenode[j][1] and treenode[i][2]==treenode[j][2]):#[[唯一节点号,名称,日期,需求量,[路径节点号,.]]]
                treenode[i][3]+=treenode[j][3]
                del treenode[j]
            else:
                j+=1
        i+=1
    
    #采购和生产流程
    for i in range(len(treenode)):
        item=get_material(treenode[i][1])
        if(item[4][1]==0):#采购
            ntime=novel_time(treenode[i][2], item[5][1]+item[5][3])
            command.append([ntime,"采购"+treenode[i][1]+str(treenode[i][3])+"件到资材仓库"])
            ntime=novel_time(treenode[i][2], item[5][1])
            command.append([ntime,"从资材仓库中取物料"+treenode[i][1]+str(treenode[i][3])+"件到工序仓库"])
        if(item[4][1]!=0):#生产
            ntime=novel_time(treenode[i][2], item[4][1])
            command.append([ntime,"车间生产"+treenode[i][1]+str(treenode[i][3])+"件"])
    
    #交付流程
    for i in range(len(MPS)):
        command.append([MPS[i][1],"交付"+MPS[i][0]+str(MPS[i][2])+"件"])
    
    #把流程按照日期排序
    for i in range(len(command)):
        mindate=command[i][0]
        minnodenum=[i]
        for j in range(i,len(command)):
            if(_is_before(command[j][0], mindate)):
                mindate=command[j][0]
                minnodenum[0]=j
        temp=command[i]
        command[i]=command[minnodenum[0]]
        command[minnodenum[0]]=temp
    
    #展示流程
    command_listbox.delete(0,tk.END)
    for i in range(len(command)):
        command_listbox.insert(tk.END, command[i])

#数据保存及读取——————————————————————————————————————————————————————
import pickle

def save():
    # 将数据保存到文件中
    with open('data.pkl', 'wb') as f:
        pickle.dump([BOM,MPS], f)
    print("已将更改保存到data文件")
   
# 从文件中读取列表
def read():
    with open('data.pkl', 'rb') as f:
        return pickle.load(f)
    print("从文件中读取BOM表和MPS表")

if(use_sample):

    BOM=[
         #["mno","mname","munit",["ware_prod","ware_house"],
         #["dis_work","alt_work",[]],["dis_mat","alt_mat","dis_prov","alt_prov"]],
         ["20000","眼镜","副",[0,0],[0,1,[["镜框",1],["镜片",2],["螺钉",2]]],[0,0,0,0]],
         ["20100","镜框","副",[0,0],[0,1,[["镜架",1],["镜腿",2],["鼻托",2],["螺钉",4]]],[0,0,0,0]],
         ["20110","镜架","个",[0,0],[0,0,[]],[0,1,0,20]],
         ["20120","镜腿","个",[10,20],[0,0,[]],[0,1,0,10]],
         ["20110","鼻托","个",[0,0],[0,0,[]],[0,1,0,18]],
         ["20110","螺钉","个",[10,50],[0,0,[]],[0.1,1,0,10]],
         ["20110","镜片","片",[0,0],[0,0,[]],[0,1,0,20]]]
    
    MPS=[["眼镜","2023-10-14","10"],
         ["镜框","2023-10-10","20"]]

else:
    
    loadin=read()
    BOM=loadin[0]
    MPS=loadin[1]
    
loadBOM()
loadMPS()

# 启动主循环
root.mainloop()

import os
os.system('pause')
