co_dic={range(0,4400):'#0091ff', range(4400,9400):'#00ff48', range(9400,12400):'yellow', range(12400,15400):'orange', range(15400,1000000):'red'}
o3_dic={range(0,60):'#0091ff', range(60,100):'#00ff48', range(100,140):'yellow', range(140,180):'orange', range(180,1000000):'red'}
pm2_5_dic={range(0,10):'#0091ff', range(10,25):'#00ff48', range(25,50):'yellow', range(50,75):'orange', range(75,1000000):'red'}
pm10_dic={range(0,20):'#0091ff', range(20,50):'#00ff48', range(50,100):'yellow', range(100,200):'orange', range(200,1000000):'red'}
no2_dic={range(0,40):'#0091ff', range(40,70):'#00ff48', range(70,150):'yellow', range(150,200):'orange', range(200,1000000):'red'}
so2_dic={range(0,20):'#0091ff', range(20,80):'#00ff48', range(80,250):'yellow', range(250,350):'orange', range(350,1000000):'red'}

def co_col(arg):
    for i in co_dic:
        if arg in i:
            return (co_dic[i])

def o3_col(arg):
    for i in o3_dic:
        if arg in i:
            return (o3_dic[i])

def pm2_5_col(arg):
    for i in pm2_5_dic:
        if arg in i:
            return (pm2_5_dic[i])

def pm10_col(arg):
    for i in pm10_dic:
        if arg in i:
            return (pm10_dic[i])

def no2_col(arg):
    for i in no2_dic:
        if arg in i:
            return (no2_dic[i])

def so2_col(arg):
    for i in so2_dic:
        if arg in i:
            return (so2_dic[i])

