import random
import math
from math import sqrt

glb_x = 200
glb_y = 140
x_frame = 1000
y_frame = 700


class Item(object):
    def tick(self,b,a):
        pass
    def setu(self,b):
        pass
    def isFood(self):
        return False
    def isHive(self):
        return False
    def isBeacon(self):
        return False

class Beacon(Item):
    def __init__(self,x,y,ant,num,go):
        self.n = 0
        self.go = go
        self.time = num
        self.x = x
        self.y = y
        self.iden = ant.iden
        self.li = set([])
        self.li.add(tuple([ant.iden,0]))

    def add(self,x):
        self.li.add(tuple([x.iden,self.n]))

    def inList(self,x):
        for item in self.li:
            if item is not None and item[0] == x.iden:
                return True
        return False

    def isBeacon(self):
        return True

    def extend(self):
        self.time += 10

    def remove(self,x):
        rem = []
        for item in self.li:
            if item[0]==x.iden:
                rem.append(item)
        for item in rem:   
            self.li.remove(item)

    
    def tick(self,a):
        self.time -= 1
        self.n += 1
        rem = []
        for item in self.li:
            #removes recent ant visits
            if abs(item[1]-self.n)>15: #not none?
                rem.append(item)
        for item in rem:
            self.li.remove(item)
        
        if self.time==0:
            a[self.x][self.y] = None
            

class Food(Item):

    def __init__(self,x,y,value):
        self.x = x
        self.y = y
        self.value = value
    
    def isFood(self):
        return True



#NOT THAT GOOD AT CONINUING ESTABLISHED ROUTE
#ALSO BUG WHERE THEY GET STUCK, TOO MANY BEACONS
class Agent(Item):

    def __init__(self, x, y, dx, dy, color, energy, iden):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.color = color
        self.energy = energy
        self.seen = False
        self.back = False
        self.food = 0
        self.xdist = 0
        self.ydist = 0
        self.bc = 0
        self.iden = iden

        self.tester = 0


    def color(self):
        return self.color

    def setu(self,b):
        self.seen = False

    def randmove(self,b):
        ant = self
        x = -1
        y = -1

        go = True

        #could loop forever problem
        while go:
            if random.random()>.1 and not (ant.x==ant.dx and ant.y==ant.dy):
                #continue on old route
                #x direction
                if ant.x-ant.dx > 0:
                    if ant.x == glb_x-1:
                        x = glb_x - 2
                    else:
                        x = ant.x + 1

                elif ant.x-ant.dx < 0:
                    if ant.x == 0:
                        x = 1
                    else:
                        x = ant.x - 1
                else:
                    x = ant.x

                #y direction
                if ant.y-ant.dy > 0:
                    if ant.y == glb_y-1:
                        y = glb_y - 2
                    else:
                        y = ant.y + 1

                elif ant.y-ant.dy < 0:
                    if ant.y == 0:
                        y = 1
                    else:
                        y = ant.y - 1
                else:
                    y = ant.y

            else:
                #new route random
                randx = random.randint(1,3)
                randy = random.randint(1,3)

                if randx == 3:
                    if ant.x == glb_x-1:
                        x = glb_x-2
                    else:
                        x = ant.x + 1
                elif randx == 1:
                    if ant.x == 0:
                        x = 1
                    else:
                        x = ant.x - 1
                else:
                    x = ant.x

                if randy == 3:
                    if ant.y == glb_y-1:
                        y = glb_y-2
                    else:
                        y = ant.y + 1
                elif randy == 1:
                    if ant.y == 0:
                        y = 1
                    else:
                        y = ant.y - 1
                else:
                    y = ant.y

            if b.map[x][y] is None:
                #move there if empty
                self.xdist += x-ant.x
                self.ydist += y-ant.y

                b.map[ant.x][ant.y] = None
                ant.dx = ant.x
                ant.dy = ant.y
                ant.x = x
                ant.y = y
                b.map[x][y] = ant
                go = False


    def smartmove(self,b):
        #smartmove should choose a diff move is chosen path is blocked
        x = -1
        y = -1
        if self.back:
            if self.xdist>0:
                x = self.x - 1
            elif self.xdist<0:
                x = self.x + 1
            else:
                x = self.x
            if self.ydist>0:
                y = self.y - 1
            elif self.ydist<0:
                y = self.y + 1
            else:
                y = self.y
        else:
            if random.random()>.5:
                if self.xdist>0 and self.x<glb_x-1:
                    x = self.x + 1
                elif self.xdist<0 and self.x>0:
                    x = self.x - 1
                else:
                    x = self.x
                if self.ydist>0 and self.y<glb_y-1:
                    y = self.y + 1
                elif self.ydist<0 and self.y>0:
                    y = self.y - 1
                else:
                    y = self.y
            #so that they can go straight out as well (not diagonal)
            else:
                if abs(self.xdist)>abs(self.ydist):
                    y = self.y
                    if self.xdist>0 and self.x<glb_x-1:
                        x = self.x + 1
                    elif self.xdist<0 and self.x>0:
                        x = self.x - 1
                    else:
                        x = self.x
                elif abs(self.xdist)<abs(self.ydist):
                    x = self.x
                    if self.ydist>0 and self.y<glb_y-1:
                        y = self.y + 1
                    elif self.ydist<0 and self.y>0:
                        y = self.y - 1
                    else:
                        y = self.y
                else:
                    if random.random()>.5:
                        y = self.y
                        if self.xdist>0 and self.x<glb_x-1:
                            x = self.x + 1
                        elif self.xdist<0 and self.x>0:
                            x = self.x - 1
                        else:
                            x = self.x
                    else:
                        x = self.x
                        if self.ydist>0 and self.y<glb_y-1:
                            y = self.y + 1
                        elif self.ydist<0 and self.y>0:
                            y = self.y - 1
                        else:
                            y = self.y
                    
                    

        if b.map[x][y] is None:

            ant = self
            
            self.xdist += x-ant.x
            self.ydist += y-ant.y

            b.map[ant.x][ant.y] = None
            ant.dx = ant.x
            ant.dy = ant.y
            ant.x = x
            ant.y = y
            b.map[x][y] = ant

        else:
            self.randmove(b)

    def beacon(self,b,a):
        ant = self
        beac = None
        bdist = 1000

        #INCREASED VIEW RANGE (NOTE THIS IS DIFF) (others too)
        for i in xrange(-10,11):
            for j in xrange(-10,11):
                if i+self.x>=0 and i+self.x<glb_x and j+self.y>=0 and j+self.y<glb_y:
                    if a[i+self.x][j+self.y] is not None:
                        if a[i+self.x][j+self.y].isBeacon() and not a[i+self.x][j+self.y].inList(self) and (beac is None or sqrt(i**2+j**2)<bdist):#CLOSEST
                            beac = a[i+self.x][j+self.y]
                            bdist = sqrt(i**2+j**2)

        #NEEDS SOME WORK (ESPECIALLY WITH THE BEAC.GO AND IDENTITY DEAL FOR BACK AND FORWARD)
        if beac is None or (self.x==self.dx and self.y==self.dy) or \
           (beac is not None and beac.inList(self)) or (beac.go==False and not self.back):


            #^^^ or random.random>.99: <-maybe add randomness

            print self.tester
            self.tester += 1
            
            if random.random()>.1:
                self.randmove(b)
            else:
                #FIX THIS TOO 
                #if (self.x<2*glb_x/3 and self.y<2*glb_y/3 and self.x>glb_x/3 and self.y>glb_y/3):#MAYBE ADD BACK -> or self.back:
                #    self.smartmove(b)
                #else:
                    self.randmove(b)

        else:
            xd = beac.x-self.x
            yd = beac.y-self.y
            
            if abs(xd)<2 and abs(yd)<2:
                beac.add(self)
                beac.extend()
                
            else:
                x = -1
                y = -1
                if xd>0:
                    x = self.x+1
                elif xd==0:
                    x = self.x
                else:
                    x = self.x-1
                    
                if yd>0:
                    y = self.y+1
                elif yd==0:
                    y = self.y
                else:
                    y = self.y-1
                        
                ## choose a new move otherwise
                if b.map[x][y] is None:
                    
                    self.xdist += x-ant.x
                    self.ydist += y-ant.y
                    
                    b.map[self.x][self.y] = None
                    self.dx = ant.x
                    self.dy = ant.y
                    self.x = x
                    self.y = y
                    b.map[x][y] = self
                    
    def bring(self,b,a):
        
        ant = self
        

        # BEACONING CAN BE ADDED TO TICK PROBABLY (REMOVE HERE LATER)
        self.bc += 1
        if self.bc==3:
            a[self.x][self.y] = Beacon(self.x,self.y,self,200,True)
            self.bc = 0
        #


        hive = None

        #changed numb
        for i in xrange(-10,11):
            for j in xrange(-10,11):
                if i+self.x>=0 and i+self.x<glb_x and j+self.y>=0 and j+self.y<glb_y:
                    if b.map[i+self.x][j+self.y] is not None and b.map[i+self.x][j+self.y].isHive():
                        hive = b.map[i+self.x][j+self.y]


        if self.energy<100 and self.food>0:
            print "eat reserve"
            self.food -= 1
            self.energy += 100
            if self.food==1:
                self.back = False

        if hive is None:

            #FIX (UNCOMMENT)
            #once beacon is fixed can always beacon
            #if random.random()>.99:
            #    self.randmove(b)
            #elif random.random()>.99:
            #    self.smartmove(b)
            #else:
                self.beacon(b,a)

        else:
            xd = hive.x-self.x
            yd = hive.y-self.y
            
            if abs(xd)<2 and abs(yd)<2:
                if self.energy<50 and hive.food>0:
                    hive.food -= 1
                    self.energy = 100
                else:
                    hive.food += self.food
                    self.food = 0
                    self.back = False

                beac = None
                bdist = 10000

                #changes numbers
                for i in xrange(-10,11):
                    for j in xrange(-10,11):
                        if i+self.x>=0 and i+self.x<glb_x and j+self.y>=0 and j+self.y<glb_y:
                            if a[i+self.x][j+self.y] is not None:
                                if a[i+self.x][j+self.y].isBeacon() and (beac is None or sqrt(i**2+j**2)<bdist):
                                    beac = a[i+self.x][j+self.y]
                                    bdist = sqrt(i**2+j**2)

                if beac is not None and beac.inList(self):
                    beac.remove(self)

  

                    
            else:
                x = -1
                y = -1
                if xd>0:
                    x = self.x+1
                elif xd==0:
                    x = self.x
                else:
                    x = self.x-1

                if yd>0:
                    y = self.y+1
                elif yd==0:
                    y = self.y
                else:
                    y = self.y-1

                ## choose a new move otherwise
                if b.map[x][y] is None:

                    self.xdist += x-ant.x
                    self.ydist += y-ant.y

                    b.map[self.x][self.y] = None
                    self.dx = ant.x
                    self.dy = ant.y
                    self.x = x
                    self.y = y
                    b.map[x][y] = self
    

    ##PROBABLY NEEDS EDITS
    def dire(self,b,a):
        print "dire"
        ant = self
        
        if self.food>0:
            self.food -= 1
            self.energy += 100
            return
    
        food = None
        fdist = 10000

        # numb change
        for i in xrange(-10,11):
            for j in xrange(-10,11):
                if i+self.x>=0 and i+self.x<glb_x and j+self.y>=0 and j+self.y<glb_y:
                    if b.map[i+self.x][j+self.y] is not None:
                        if b.map[i+self.x][j+self.y].isFood() and (food is None or sqrt(i**2+j**2)<fdist):
                            food = b.map[i+self.x][j+self.y]
                            fdist = sqrt(i**2+j**2)

        hive = None

        # numb change
        for i in xrange(-10,11):
            for j in xrange(-10,11):
                if i+self.x>=0 and i+self.x<glb_x and j+self.y>=0 and j+self.y<glb_y:
                    if b.map[i+self.x][j+self.y] is not None and b.map[i+self.x][j+self.y].isHive():
                        hive = b.map[i+self.x][j+self.y]
                        

        if food is None and hive is None:

            #FIX LATER (UNCOMMENT)
            #if random.random()>.99:
            #   self.randmove(b)
            #elif random.random()>.99:
            #    self.smartmove(b)
            #else:
            #    self.beacon(b,a)
            self.randmove(b)

            return
        elif food is not None and hive is None:
            run = food
        elif food is None and hive is not None:
            run = hive
        else:
            run = food

        xd = run.x-self.x
        yd = run.y-self.y
                
        if abs(xd)<2 and abs(yd)<2:
            if run.isFood():
                run.value -= 1
                if run.value==0:
                    b.map[run.x][run.y] = None
                self.energy += 100
                print "eat block"
            else:
                if run.food>0:
                    run.food -= 1
                    self.energy = 100
                else:
                    self.randmove(b)
                
        else:
            x = -1
            y = -1
            if xd>0:
                x = self.x+1
            elif xd==0:
                x = self.x
            else:
                x = self.x-1
                
                if yd>0:
                    y = self.y+1
                elif yd==0:
                    y = self.y
                else:
                    y = self.y-1
                    
                ## choose a new move otherwise
                if b.map[x][y] is None:

                    self.xdist += x-ant.x
                    self.ydist += y-ant.y

                    b.map[self.x][self.y] = None
                    self.dx = ant.x
                    self.dy = ant.y
                    self.x = x
                    self.y = y
                    b.map[x][y] = self
                

            

            
        
    

    def tick(self,b,a):
        if self.seen:
            return
        ant = self
        ant.energy -= 1
        if ant.energy==0:
            b.map[ant.x][ant.y] = None
            print "death"
            return
        if ant.energy<40:
            self.dire(b,a)
            self.seen = True
            return

        if self.back:
            self.bring(b,a)
            self.seen = True
            return

        ##<beacon whole time
        self.bc += 1
        if self.bc==3:
            a[self.x][self.y] = Beacon(self.x,self.y,self,200,False)
            self.bc = 0
        #<

        
        food = None
        fdist = 10000
        beac = None
        bdist = 10000

        #changed numbers
        for i in xrange(-10,11):
            for j in xrange(-10,11):
                if i+self.x>=0 and i+self.x<glb_x and j+self.y>=0 and j+self.y<glb_y:
                    if b.map[i+self.x][j+self.y] is not None:
                        if b.map[i+self.x][j+self.y].isFood() and (food is None or sqrt(i**2+j**2)<fdist):
                            food = b.map[i+self.x][j+self.y]
                            fdist = sqrt(i**2+j**2)

            

        if food is None:

            #FIX (UNCOMMENT)
            #once beacon is fixed can always beacon
            #if random.random()>.99:
            #    self.randmove(b)
            #elif random.random()>.99:
            #    self.smartmove(b)
            #else:
                self.beacon(b,a)    

        else:



            
            xd = food.x-self.x
            yd = food.y-self.y

            if abs(xd)<2 and abs(yd)<2:
                food.value -= 1
                if food.value==0:
                    b.map[food.x][food.y] = None
                if self.energy<100:
                    self.energy += 100
                    print "eat block"
                else:
                    self.food += 1
                    if self.food>4:
                        self.back = True



                beac = None
                bdist = 10000

                #changes numbers
                for i in xrange(-10,11):
                    for j in xrange(-10,11):
                        if i+self.x>=0 and i+self.x<glb_x and j+self.y>=0 and j+self.y<glb_y:
                            if a[i+self.x][j+self.y] is not None:
                                if a[i+self.x][j+self.y].isBeacon() and (beac is None or sqrt(i**2+j**2)<bdist):
                                    beac = a[i+self.x][j+self.y]
                                    bdist = sqrt(i**2+j**2)

                if beac is not None and beac.inList(self):
                    beac.remove(self)

                        
            else:
                x = -1
                y = -1
                if xd>0:
                    x = self.x+1
                elif xd==0:
                    x = self.x
                else:
                    x = self.x-1

                if yd>0:
                    y = self.y+1
                elif yd==0:
                    y = self.y
                else:
                    y = self.y-1

                if b.map[x][y] is None:

                    self.xdist += x-ant.x
                    self.ydist += y-ant.y

                    b.map[self.x][self.y] = None
                    self.dx = ant.x
                    self.dy = ant.y
                    self.x = x
                    self.y = y
                    b.map[x][y] = self

        self.seen = True

class Hive(Item):

    def __init__(self, x, y, num):
        self.x = x
        self.y = y
        self.food = 0
        self.num = num
        self.seen = False
        self.time = 0
        self.rep = 100
        self.iden = 0
    
    def isHive(self):
        return True

    def setu(self,b):
        self.seen = False

    def addFood(self,f):
        self.food += f

    def tick(self,b,a):
        if self.seen:
            return
        self.rep = 100 - self.food/25
        if self.rep<1:
            self.rep=1
        if self.num>0 or self.time%(self.rep)==0:
            self.num -= 1
            go = True
            while go:
                xrand = random.randint(-5,5)
                yrand = random.randint(-5,5)
                if self.x+xrand<0 or self.x+xrand>=glb_x or self.y+yrand<0 or self.y+yrand>=glb_y:
                    pass
                elif b.map[self.x+xrand][self.y+yrand] is not None:
                    pass
                else:
                    b.map[self.x+xrand][self.y+yrand] = Agent(self.x+xrand,self.y+yrand,self.x+xrand,\
                                                              self.y+yrand,True,300,self.iden)
                    self.iden += 1
                    go = False
        self.seen = True
        self.time += 1


                    

    def eatFood(self,f):
        if self.food-f<0:
            return 0
        else:
            self.food -= f
            return f
