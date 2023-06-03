import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
plt.rcParams['font.sans-serif']=['SimHei'] #将plt的语言设置为中文
#童老师《钢结构与钢-混凝土组合结构设计方法》
def caculate_hd_tong(V,M,D,fc):
    hd_tong = V/D/0.8/fc+np.sqrt(2*V**2/D**2/(0.8*fc)**2+4*M/D/0.8/fc)
    return round(hd_tong, 2)
#《钢标》
def caculate_hd_gangbiao(V,M,D,fc):
    for d in np.arange(0.01,5,0.01):
        fc_ca = V/D/d+2*M/D/d**2+1/2*np.sqrt((2*V/D/d+4*M/D/d**2)**2+4*V**2/D**2/d**2)
        if fc_ca<=0.8*fc:
            hd_gangbiao = d
            break
    return round(hd_gangbiao, 2)
#《高钢规》
def calculate_column_Mp(D, t, fy, fck):
    As = (D**2-(D-2*t)**2)*np.pi/4
    Ac = (D-2*t)**2*np.pi/4
    asc = As/Ac
    theta = asc*fy/fck
    B = 0.176*fy/213+0.974
    C = -0.104*fck/14.4+0.031
    fsc = (1.212+B*theta+C*theta**2)*fck
    gama_m = 1.2  #圆形规范为1.2，这里将Mp提高以考虑不利
    Wp = np.pi*(D/2)**3/4
    Mp = gama_m*Wp*fsc/10**6
    return Mp
def caculate_hd_gaogui(fck_base,fck_c,fy,D,t,l):
    Mp = calculate_column_Mp(D, t, fy, fck_c)
    factor_a  = 1.2
    for d in np.arange(0.01,5,0.01):
        Mp_ca = fck_base*D*l*(np.sqrt((2*l+d)**2+d**2)-(2*l+d))
        if Mp_ca>=factor_a*Mp:
            hd_gaogui = d
            break
    return round(hd_gaogui, 2)
def fy_code(fy_Cstrength,fy_dic,t):
    t_boundary = [16,40,63,80]
    if t<=t_boundary[0]:
        fy = fy_dic[fy_Cstrength][0]
    elif t<=t_boundary[1]:   
        fy = fy_dic[fy_Cstrength][1]
    elif t<=t_boundary[2]:      
        fy = fy_dic[fy_Cstrength][2]    
    elif t<=t_boundary[3]:      
        fy = fy_dic[fy_Cstrength][3]    
    else:
        print("材料不在规范范围内")
    return fy
fck_dic = {"C15":10.0,"C20":13.4,"C25":16.7,"C30":20.1,"C35":23.4,
           "C40":26.8,"C45":29.6,"C50":32.4,"C55":35.5,"C60":38.5,
           "C65":41.5,"C70":44.5,"C75":47.4,"C80":50.2}
fy_dic = {"Q235":[235,225,215,215,215],"Q355":[345,335,325,315,305],
          "Q390":[390,370,350,330,330],"Q420":[420,400,380,360,360],
          "Q460":[460,440,420,400,400]}
# Input parameters
 
D_target = st.number_input('请输入圆管直径D', min_value=600, max_value=2000, value=1400, step=100)
t = st.number_input('请输入圆钢管厚度t', min_value=10, max_value=80, value=55, step=5)
fck_Cstrength = st.selectbox('请选择柱子混凝土抗压强度标准值fck', options=["C15","C20","C25","C30","C35","C40","C45","C50","C55","C60","C65","C70","C75","C80"], index=7)
fy_Cstrength = st.selectbox('请选择钢材屈服强度fy', options=["Q235","Q355","Q390","Q420","Q460"], index=3)
fck_Bstrength = st.selectbox('请选择基础混凝土抗压强度标准值fck', options=["C15","C20","C25","C30","C35","C40","C45","C50","C55","C60","C65","C70","C75","C80"], index=7)
length = st.number_input('请输入底层高度', min_value=3, max_value=20, value=10, step=1)

# D_target = 1400  #圆管直径
# t = 55 #圆钢管厚度
# fck_Cstrength = "C50"
# fck_Bstrength = "C50"
# fy_Cstrength = "Q420"
# length = 10 #底层高度

fck_c = fck_dic[fck_Cstrength]  #柱子混凝土抗压强度标准值
fck_base = fck_dic[fck_Bstrength]  #基础柱子混凝土抗压强度标准值
fy = fy_code(fy_Cstrength,fy_dic,t)    #钢材屈服强度
l = 2/3*length   #2/3的层高
Mp = calculate_column_Mp(D_target, t, fy, fck_c)  #按钢管混凝土规范5.1.6计算的极限弯矩值
Vu = Mp/l
   
hd_tong = caculate_hd_tong(Vu,Mp,D_target,fck_base)
hd_gangbiao = caculate_hd_gangbiao(Vu,Mp,D_target,fck_base)
hd_gaogui = caculate_hd_gaogui(fck_base,fck_c,fy,D_target,t,l)
hd_target = max(hd_tong,hd_gangbiao,hd_gaogui)
st.write(f"圆钢管柱的最小埋深为{hd_target}m")

hd_tong_list = []
hd_gangbiao_list = []
hd_gaogui_list = []
for D in np.arange(600,2000,100):
    Mp = calculate_column_Mp(D, t, fy, fck_c)  #按钢管混凝土规范5.1.6计算的极限弯矩值
    Vu = Mp/l   
    hd_tong = caculate_hd_tong(Vu,Mp,D,fck_base)
    hd_tong_list.append(hd_tong)
    hd_gangbiao = caculate_hd_gangbiao(Vu,Mp,D,fck_base)
    hd_gangbiao_list.append(hd_gangbiao)
    hd_gaogui = caculate_hd_gaogui(fck_base,fck_c,fy,D,t,l)
    hd_gaogui_list.append(hd_gaogui) 
fig, ax = plt.subplots()
ax.plot(np.arange(600,2000,100),hd_tong_list,label='《钢结构与钢-混凝土组合结构设计方法》')
ax.plot(np.arange(600,2000,100),hd_gangbiao_list,label='《钢标》')
ax.plot(np.arange(600,2000,100),hd_gaogui_list,label='《高钢规》')
ax.scatter(D_target,hd_target,c='r',marker='o')
ax.text(D_target,hd_target, f"({D_target},{hd_target})", fontsize=12, ha='left', va='bottom')
ax.legend()
ax.set_xlabel('D/mm')
ax.set_ylabel('hd/m')
ax.set_title('柱脚埋深hd-直径D曲线')
ax.text(1200, hd_gaogui_list[1], f'Dx{t}mm圆钢管混凝土柱\n混凝土{fck_Cstrength}钢材强度{fy_Cstrength}\n底层层高{length}m\n基础混凝土{fck_Bstrength}', fontsize=12, ha='left', va='bottom')
st.pyplot(fig)




