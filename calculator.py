import matplotlib.pyplot as plt
import numpy as np

# Here's the abbr and the order of skills, I will use these orders in all the array about skill
# Skill_abbr={'BJ':'JianYingNingShen','YL':'YunLongji','XN':'XuanNingJian','YH':'YuHeYao','XZ':'XuanZhenJian','JQ':'HongMengJianQi'}

def coeff_cal():
    '''
    This function calculate the coefficient of the damage of every skill. The order of skill follow the annotation above
    '''
    skill_cnt = 7
    finalAttack = [310,221,161,119,103]
    skillDamage = [[246,184,142,112,101],
                   [132,99,76,60,54],
                   [94,70,53,41,37],
                   [104,77,59,47,42],
                   [64,46,34,26,23],
                   [47,35,27,21,19],
                   [1057,788,607,480,447]]

    coeff = []

    for cnt in range(skill_cnt):
        temp = np.polyfit(finalAttack,skillDamage[cnt],1)
        # print(temp)
        coeff.append(temp[1]/temp[0])
    # print(coeff)
    # plt.plot(finalAttack,skillDamage[6])
    # plt.show()

    # ZhuangJing = [159,148,144,133,122,111,105,93,83,74,60]
    # BJ = [19.8,18.4,17.9,16.6,15.2,13.8,13.1,11.6,10.4,9.2,7.5]
    # YL = [16.4,15.3,14.9,13.7,12.6,11.5,10.8,9.6,8.6,7.7,6.2]

    # print(np.polyfit(ZhuangJing,BJ,1))
    # print(np.polyfit(ZhuangJing,YL,1))
    
    BJ_coeff =0.124
    YL_coeff=0.103
    return(coeff,BJ_coeff,YL_coeff)
    
skill_cnt = 7
coeff,BJ_coeff,YL_coeff = coeff_cal()
oldHarm = [230687,154009,48974,24458,15914,30796,27618]
oldDPS =  1379
oldZhuangJing = 267
newZhuangJing = 267+36
OldAttackCoeff = 478
NewAttackCoeff = 478-36
transferDOT = 0#0 show harm with dot.1 show harm without dot
Attack = 228
oldFinalAttack = Attack*(1+OldAttackCoeff/1000)
newFinalAttack = Attack*(1+NewAttackCoeff/1000)


newHarm = []
newHarm.append(oldHarm[0]*(newFinalAttack+coeff[0])/(oldFinalAttack+coeff[0])*(1+newZhuangJing*BJ_coeff/100)/(1+oldZhuangJing*BJ_coeff/100)) 
newHarm.append(oldHarm[1]*(newFinalAttack+coeff[1])/(oldFinalAttack+coeff[1])*(1+newZhuangJing*YL_coeff/100)/(1+oldZhuangJing*YL_coeff/100)) 

for cnt in range(2,skill_cnt):
  newHarm.append(oldHarm[cnt]*(newFinalAttack+coeff[cnt])/(oldFinalAttack+coeff[cnt]))
# Transfer if needed
if transferDOT > 0:
    DoubleRate = 0.502
    DoubleHarm = 0.6
    newHarm[5] = newHarm[1] / (1+DoubleRate*DoubleHarm) * 0.1 * DoubleHarm
newDPS = oldDPS * sum(newHarm) / sum(oldHarm)
print(newHarm)
print(newDPS)

expectsum = oldZhuangJing + OldAttackCoeff
maxDPS = 0
expectZhuangJing = 0
expectAttackCoeff = 0
maxharm = []
DPSarray = []
for x in range(1,expectsum):
    newZhuangJing = x
    NewAttackCoeff = expectsum - x
    newFinalAttack = Attack*(1+NewAttackCoeff/1000)
    newHarm = []
    newHarm.append(oldHarm[0]*(newFinalAttack+coeff[0])/(oldFinalAttack+coeff[0])*(1+newZhuangJing*BJ_coeff/100)/(1+oldZhuangJing*BJ_coeff/100)) 
    newHarm.append(oldHarm[1]*(newFinalAttack+coeff[1])/(oldFinalAttack+coeff[1])*(1+newZhuangJing*YL_coeff/100)/(1+oldZhuangJing*YL_coeff/100)) 

    for cnt in range(2,skill_cnt):
      newHarm.append(oldHarm[cnt]*(newFinalAttack+coeff[cnt])/(oldFinalAttack+coeff[cnt]))
    newDPS = oldDPS * sum(newHarm) / sum(oldHarm)
    DPSarray.append(newDPS)
    if newDPS > maxDPS:
        maxDPS = newDPS
        expectZhuangJing = newZhuangJing
        expectAttackCoeff = NewAttackCoeff
        maxharm = newHarm
print('expectZhuangJing: %d'%(expectZhuangJing))
print('expectAttackCoeff: %d'%(expectAttackCoeff))
print('maxDPS: %f'%(maxDPS))
print(maxharm)
plt.plot(range(1,expectsum),DPSarray)
plt.show()

