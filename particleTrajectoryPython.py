import random
import math
import surfgen
import FelecVdw
import functions
import MoreFuns

if __name__ == '__main__':
    #CHECK hydrodynamic function values - comp. Fortran
    #Check mean and std. dev of random numbers
    grid1 = 1515    #rows of the big surface
    grid2 = 1515    #cols of the big surface
    grid_size = 101     # according to particle and patches sizes
    griddp = 101.0
    percent = 0.25      #positive percent   
    a = 500e-9
    cols = grid2
    deb = 3e-9
    fiSphere = -0.025
    fiSurface = -0.025
    fiPillar = 0.05
    depth = 1e-9
    dt = 1e-5
    shear = 25 
    mu = 0.001
    kB = 1.3806503e-23
    T = 298.15
    nn = mu*a*math.pi
    NTimeSteps = 2500 
    isumtot = 0 
    max_dist = 10e-6
    delta = 1e-9
    Nparticles = 2 
    
    hor =[ [0 for j in range(1)] for i in range(NTimeSteps)]   
    ver =[ [0 for j in range(1)] for i in range(NTimeSteps)]  
    Vx =[ [0 for j in range(1)] for i in range(NTimeSteps+1)]  
    Vz =[ [0 for j in range(1)] for i in range(NTimeSteps+1)]  
       
    #fid22 = open('SurfaceHeterog.txt', 'w')    
    #! GENERATING BIG SURFACE
    hetsurf = surfgen.surfgene(grid1, grid2, percent)
    #print>> fid22, hetsurf
    #fid22.close()
    #print len(hetsurf[0]), len(hetsurf)
    #should be 1001, 101
    
    #Generating the random numbers that will determine the locations
    #In this case, use 1 big surface
    fid44 = open('RandomLocations.txt','w')
    numbers = range(51,1466)
    k = 510 #quantity of locations = quantity of particles 
    #k should be equal to Nparticles
    chosenNum = random.sample(numbers,k)
    locations = [0 for mm in range(k)]
    #saving the chosen numbers into the array locations
    for i in range(k):
        locations[i] = chosenNum[i]
        print>> fid44, chosenNum[i], locations[i]
    fid44.close()
    
    fid28 = open('condition.txt', 'w')
    
    for kk in range(Nparticles):
        
        #To be initialized for EACH particle
        condition = 0 
        time = 0 
        hdist = 0.0
        vdist = 40e-9
        
        #DEFINING hetsurf1 = part of big surface to be used
        #first_row = mid-50 
        #last_row = mid+50 (for range, use 'mid+50+1')
        #hetsurf1 = [hetsurf[i] for i in range(grid_size)]   
        mid = locations[kk]
        print mid
        if kk== 0:
            fid23 = open('RandomNum0001.txt', 'w')  
            fid233 = open('RandomNum0002.txt', 'w') 
            fid26 = open('HorDisp1.txt', 'w')  
            fid27 = open('VerDisp1.txt', 'w') 
        if kk== 1:
            fid23 = open('RandomNum0003.txt', 'w')  
            fid233 = open('RandomNum0004.txt', 'w') 
            fid26 = open('HorDisp2.txt', 'w')  
            fid27 = open('VerDisp2.txt', 'w')            
        hetsurf1 = [hetsurf[i] for i in range(mid-50, mid+50+1)]
        
        while (condition==0):
        #for s in range(0, 120):
            hor[time] = hdist/a
            ver[time] = vdist/a
            saveTime = dt*(time-1)
            print>> fid26, hor[time]
            print>> fid27, ver[time]
            time = time + 1
            h = vdist
            Ft, Tt, Fr, Tr = functions.hydro_functions(h,a)
            Df = Tt*Fr - Ft*Tr
        
            lambda2, jii = MoreFuns.LambdaJi_functions(h, a)
            #lambda2 = 2.1957
            #ji=1.1384
        
            Fs = 6*nn*(a+h)*shear*(1+ 9*a/(16*(a+h)))
            Ts = 4*nn*a*a*(1-(3/16))*(math.pow((a/(a+h)),3))*shear
        
            #define Mobility Matrix
            MobM = [ [0 for j in range(6)] for i in range(6)] 
            MobM[0][0] = Tr/(6*math.pi*mu*a*Df)
            MobM[1][1] = 1/(6*math.pi*mu*a*lambda2)
            MobM[2][2] = Tr/(6*math.pi*mu*a*Df)
            MobM[3][2] = Fr/(8*math.pi*mu*(math.pow(a,2))*Df)
            MobM[5][0] = (-Fr)/(8*math.pi*mu*(math.pow(a,2))*Df)
            MobM[0][5] = (-Tt)/(6*math.pi*mu*(math.pow(a,2))*Df)
            MobM[2][3] = Tt/(6*math.pi*mu*(math.pow(a,2))*Df)
            MobM[3][3] = Ft/(8*math.pi*mu*(math.pow(a,3))*Df)
            MobM[4][4] = 1/(8*math.pi*mu*(math.pow(a,3))*jii)
            MobM[5][5] = Ft/(8*math.pi*mu*(math.pow(a,3))*Df)
        
            #Define vector of forces
            ForceVec = [ [0 for j in range(1)] for i in range(6)] 
          
            ForElecVdw = FelecVdw.FelecVdw1 (hdist, vdist, hetsurf1,a,grid_size, griddp,cols, deb, fiSphere, fiSurface, fiPillar, depth)    
            FBrx = 0
            FBry = 0
            nr1 = random.uniform(-1,1)      
            nr2 = random.uniform(-1,1)
            print>> fid23, nr1
            print>> fid233, nr2   
            #Brownian force in the normal direction of (z)        
            FBry = (nr1*kB*T)/a
            #Brownian force in the direction of flow(x)
            FBrx = (nr2*kB*T)/a

            ForceVec[0][0] = Fs + FBrx
            ForceVec[1][0] = ForElecVdw + FBry 
            #!ForElecVdw is Felec+Fvdw and FBry is the Brownian force in y (normal direction)
            ForceVec[5][0] = Ts
            Output = [ [0 for j in range(1)] for i in range(6)] 
            for i in range(6):
                Output[i][0] = MobM[i][0]*ForceVec[0][0]+MobM[i][1]*ForceVec[1][0]+MobM[i][2]*ForceVec[2][0]+MobM[i][3]*ForceVec[3][0]+MobM[i][4]*ForceVec[4][0]+MobM[i][5]*ForceVec[5][0]
    
            Vx[time] = Output[0][0]
            Vz[time] = Output[1][0]
            
            hdist = hdist+ dt*Vx[time]
            vdist = vdist+ dt*Vz[time]
        
            if(vdist<=delta):
                condition = 1 #!particle is arrested
                isumtot = isumtot + 1

            if(hdist>= max_dist):
                condition = 2

            if(time>=NTimeSteps):
                condition = 3
    
        print>> fid28, condition, 'why stopped'
        #CLOSE ALL files of variables I wanted to save
        fid23.close()    
        fid233.close()
        fid26.close()
        fid27.close()
       
    print>> fid28, isumtot, 'total adhered'
    fid28.close()
                        
