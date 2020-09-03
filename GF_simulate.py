import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

###Input the initial conditions:
while True:
    print('How many normal pulses do you have?\n')
    normal_pulses = input()
    normal_pulses = int(normal_pulses)

    print('How many SC pulses do you have?\n')
    sc_pulses = input()
    sc_pulses = int(sc_pulses)

    print('How many fire-god tickets do you have?\n')
    fg_tickets = input()
    fg_tickets = int(fg_tickets)

    if normal_pulses >= 0 and sc_pulses >= 0 and fg_tickets >= 0:
        normal_pulses = normal_pulses + 31*2
        sc_pulses = sc_pulses + 4
        fg_tickets = fg_tickets + 2
        print('This month, you have ' + str(normal_pulses) + ' normal pulses, ' + str(sc_pulses) + ' SC pulses and ' + str(fg_tickets) + ' fire-god tickets.\n')
        
        break
    else:
        print('Error!!Please type positive numbers or zero....')
        continue


init_sc_pulses = [sc_pulses]
init_fg_tickets = [fg_tickets]


keep = [10,20,30,40]

print("How many times of experiments do you want?\n")
exp_times = input()
exp_times = int(exp_times)

print("Let's do the calculation.... ")

###Simulation part:
captured = []
catch_times = 0
refresh_times = 1
normal_pulses = normal_pulses + sc_pulses - keep[1] #Want to keep 30 sc_pulses.
init_normal_pulses = [normal_pulses]

num_of_one_star = 60
num_of_two_star = 39
num_of_boss = 1
boss = ["Boss"]
two_stars = ["Two_star" for x in range(num_of_two_star)]
one_stars = ["One_star" for x in range(num_of_one_star)]
pool = boss + two_stars + one_stars


def generate_stage(pool, stage):
    for i in range(3):
        delta = np.random.choice(pool, 1)
        pool.remove(delta[0])
        stage.append(delta[0])
    return stage

def refresh(stage):
    for i in stage:
        pool.append(i)
    stage.clear()
    generate_stage(pool, stage)
    return stage
    

stage = []
boss_captured = []

for exp in range(exp_times):
    
#    print(str(exp))
    
    generate_stage(pool, stage)
   
    
    while ((normal_pulses > 0) and (len(pool) > 0)):
        if ((stage.count("One_star") >0) or (stage.count("Boss") > 0)):
            for element in stage:
                if (element == "One_star") and (normal_pulses > 0):
                    stage.remove("One_star")
                    captured.append("One_star")
                    normal_pulses = normal_pulses - 1
                    catch_times += 1
                    if catch_times == 6:
                        catch_times = 0
                        if refresh_times == 0:
                            refresh_times += 1
                
                
                
                elif (element == "Boss") and (normal_pulses > 0):
                    dual = np.random.binomial(1, 0.25)
                    if dual == 1:
                        stage.remove("Boss")
                        captured.append("Boss")
                        catch_times += 1
                        if catch_times == 6:
                            catch_times = 0
                            if refresh_times == 0:
                                refresh_times += 1
                    
#                        print("Boss has been captured!!")
                    
                    else:
                        stage.remove("Boss")
                        pool.append("Boss")
                        catch_times += 1
                        if catch_times == 6:
                            catch_times = 0
                            if refresh_times == 0:
                                refresh_times += 1
                    
#                        print("Boss has escaped!!")
                    normal_pulses = normal_pulses - 1
            
                elif (element == "Two_star") and (normal_pulses > 0):
                    if refresh_times == 0:
                        dual = np.random.binomial(1, 0.5)
                        if dual == 1:
                            stage.remove("Two_star")
                            captured.append("Two_star")
                            catch_times += 1
                            if catch_times == 6:
                                catch_times = 0
                                if refresh_times == 0:
                                    refresh_times += 1
                        
                        
                        else:
                            stage.remove("Two_star")
                            pool.append("Two_star")
                            catch_times += 1
                            if catch_times == 6:
                                catch_times = 0
                                if refresh_times == 0:
                                    refresh_times += 1
                        
                        normal_pulses = normal_pulses - 1
            
                if len(stage) < 3:
                    replaced = np.random.choice(pool, 1)
                    stage.append(replaced[0])
                    pool.remove(replaced[0])
       
            
        elif (stage.count("Two_star") == 3):
            if refresh_times > 0:
                refresh(stage)           
                refresh_times = refresh_times - 1
                continue
        
            elif (refresh_times == 0) and (normal_pulses > 0):
                dual = np.random.binomial(1, 0.5)
                if dual == 1:
                    stage.remove("Two_star")
                    captured.append("Two_star")
                
                else:
                    stage.remove("Two_star")
                    pool.append("Two_star")
                
                normal_pulses = normal_pulses - 1
                replaced = np.random.choice(pool, 1)
                stage.append(replaced[0])
                pool.remove(replaced[0])
                catch_times += 1
                if catch_times == 6:
                    catch_times = 0
                    if refresh_times == 0:
                        refresh_times += 1  
     
    
                 
#        print('stage:', stage)
#        print("catch_times: ", catch_times)
#        print('refresh_times', refresh_times)
#        print('normal_pulses:', normal_pulses)

    if captured.count("Boss") > 0:
        boss_captured.append(1)
            
    elif captured.count("Boss") == 0:
        boss_captured.append(0)
        
        
    pool.extend(captured)
    pool.extend(stage)
    captured.clear()
    stage.clear()
        
    normal_pulses = init_normal_pulses[0]
    refresh_times = 1
    catch_times = 0
#    print("This turn is finished. Do the experiment again!!")
    
        
        

print("captured probability: ",(sum(boss_captured)/exp_times)*100, "%")






#print('final normal_pulses:', normal_pulses)
#print('captured:', captured)
#print('pool:', pool)
#print('len(pool):', len(pool))
#print('len(captured):', len(captured))
#print('capured boss:', captured.count("Boss"))
#print("captured two stars", captured.count("Two_star"))














