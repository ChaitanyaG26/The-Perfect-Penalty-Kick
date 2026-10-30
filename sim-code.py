Web VPython 3.2

vx = float(input("What is the x-component of wind velocity [m/s]?"))
vy = float(input("What is the y-component of wind velocity [m/s]?"))
vz = float(input("What is the z-component of wind velocity [m/s]?"))

vair = vector(vx, vy, vz)

time = float(input("How long [s] does the goalkeeper take to reach the corners after contact?"))
legmass = float(input("What is the mass [kg] of the leg?"))
cr = float(input("What is the coefficient of restitution?"))
distance = float(input("What is the distance [m] the kicking appendage is dragged?"))
vli0 = float(input("What was the initial speed [m/s] of the foot before being dragged?"))
v0 = 23.5
Goal = False


progvar = 0
while progvar != 1 and progvar != 2:
    progvar = int(input("Scenario: 1. Airborne, or 2. Earthbounded?"))
    if progvar == 1:
        Mvar = 0
        while Mvar == 0:
          Mdec = int(input("Is the scenario: 1. Top-spin / Back-spin, or 2. Side-spin?"))
          if Mdec == 2:
            M = vector(0, 1, 0)
            Mvar += 1
          elif Mdec == 1:
            M = vector(0, 0, 1)
            Mvar += 1
          else:
            print("Please enter a value equal to 1 or 2.")
        
        ground = box(pos = vector(0,-0.25,0), size = vector(30,.5,2), color = color.green)
        goal = box(pos = vector(-3.5272,1.2192,0), size = vector(1,2.4384,7.3152), color = color.white)
        
        g = vector(0,-9.81,0)
        rho = 1.225
        R = 0.10795
        C = 0.275
        Cl = 0.325
        A = pi*(R**2)
        dt = 0.001
        r0 = vector(-15,0,0)
        
        def simulate(v0, Theta, IdAn, M, animate = False):
          theta = (pi*Theta)/180
          ball = sphere(pos = vector(r0), radius = 0.2159, color = color.yellow, make_trail = animate, visible = animate)
          ball.m = 0.430
          ball.p = ball.m*v0*vector(cos(theta),sin(theta),tan(IdAn))
          t = 0
        
          while ball.pos.x <= (r0.x + 10.9728):
            if animate:
              rate(250)
            ball.v = (ball.p / ball.m) - vair
            if mag(ball.v) == 0:
              vperp = vector(0,0,0)
              Fgd = ball.m*g
              Flift = vector(0,0,0)
            else:
              vperp = cross(norm(ball.v), M)
              Fgd = ball.m*g - (0.5*rho*A*C*(mag(ball.v)**2)*norm(ball.v))
              if mag(vperp) == 0:
                Flift = vector(0,0,0)
              else:
                Flift = (0.5*rho*A*Cl*(mag(ball.v)**2)*norm(vperp))
            Fnet = Fgd + Flift
            ball.p = ball.p + Fnet*dt
            ball.pos = ball.pos + ball.p*dt / ball.m
            t = t + dt
            if t > 10:
              ball.visible = False
              return [ball.pos, t, False]
        
          result = [vector(ball.pos), t, True]
          if not animate:
            ball.visible = False
          return result
        
        def findAngle(v0, IdAn, M):
          Angle = [-500, None, None]
          Theta = 25
        
          while Theta >= 0:
            result = simulate(v0, Theta, IdAn, M)
            if result[2]:
              if result[0].y <= 2.33045 and result[0].y >= 0.2159 and result[0].y >= Angle[0]:
                Angle = [result[0].y, Theta, result[1]]
            Theta -= 0.05
        
          return Angle
        
        while Goal == False:
          if Mdec == 2:
            M = vector(0, 1, 0)
          elif Mdec == 1:
            M = vector(0, 0, 1)
        
          result = simulate(v0, 15, 0, M)
        
          if not result[2]:
            v0 += 0.25
            if v0 > 100:
              break
            continue
        
          IdAn = atan((result[0].z + 3.54965)/(result[0].x + 15))
        
          if vz <= -5:
            IdAn -= 0.01
            IdAn -= abs(vz - 5)*0.001
            if Mdec == 1:
              IdAn -= 0.025
        
          IdAnLeft = -IdAn
          IdAngLeft = 180*IdAn/pi
        
          Angle = findAngle(v0, IdAnLeft, M)
        
          if Angle[1] == None:
            v0 += 0.25
            if v0 > 100:
              break
            continue
        
          IdAngLl = [IdAngLeft, Angle[1], Angle[2]]
        
          if Mdec == 2:
            M = vector(0, -1, 0)
          elif Mdec == 1:
            M = vector(0, 0, -1)
        
          result = simulate(v0, 15, 0, M)
        
          if not result[2]:
            v0 += 0.25
            if v0 > 100:
              break
            continue
        
          IdAn = atan((abs(result[0].z) + 3.54965)/(result[0].x + 15))
        
          if vz >= 5:
            IdAn -= 0.01
            IdAn -= abs(vz - 5)*0.001
            if Mdec == 1:
              IdAn -= 0.025
        
          IdAnRight = IdAn
          IdAngRight = 180*IdAn/pi
        
          Angle = findAngle(v0, IdAnRight, M)
        
          if Angle[1] == None:
            v0 += 0.25
            if v0 > 100:
              break
            continue
        
          IdAngLr = [IdAngRight, Angle[1], Angle[2]]
        
          if IdAngLl[2] < time and IdAngLr[2] < time:
            Goal = True
          else:
            v0 += 0.25
            if v0 > 100:
              break
        
        if Goal:
          if Mdec == 1:
            print("The first yellow projectile had top-spin.\n")
        
          if Mdec == 2:
            M = vector(0, 1, 0)
          elif Mdec == 1:
            M = vector(0, 0, 1)
        
          simulate(v0, IdAngLl[1], IdAnLeft, M, True)
        
          if Mdec == 2:
            M = vector(0, -1, 0)
          elif Mdec == 1:
            M = vector(0, 0, -1)
        
          simulate(v0, IdAngLr[1], IdAnRight, M, True)
        
          print("The optimal sideways angle, for the projectile on the left was:", IdAngLl[0], "degrees.")
          print("The optimal vertical angle, for the projectile on the left, was:", IdAngLl[1], "degrees.")
          print("It took:", IdAngLl[2], "seconds.")
          print("\nThe optimal sideways angle, for the projectile on the right, was:", IdAngLr[0], "degrees.")
          print("The optimal vertical angle, for the projectile on the right, was:", IdAngLr[1], "degrees.")
          print("It took:", IdAngLr[2], "seconds.")
          print("The optimal velocity, for this data set, was", v0, "meters per second.")
        
          if legmass > 0 and distance > 0 and (1 + cr) != 0:
            accel = ((((v0*(legmass + 0.430))/(legmass*(1 + cr)))**2)-(vli0**2))/(2*distance)
            print("\nThe kicking appendage must be dragged", distance, "meters at an acceleration of", accel, "meters per second squared.")
          else:
            print("The acceleration could not be calculated with the given inputs.")
        else:
          print("No valid solution was found within the velocity range.")

    elif progvar == 2:
        while Goal == False:
          ground = box(pos = vector(0,-0.25,0), size = vector(30,.5,2), color = color.green)
          goal = box(pos = vector(-3.5272,1.2192,0), size = vector(1,2.4384,7.3152), color = color.white)
          ball = sphere(pos = vector(-15,0,0), radius = 0.2159, color = color.white, make_trail = False)
          r0 = ball.pos
          g = vector(0,-9.81,0)
          ball.m = 0.430
          Theta = 0
          theta = (pi*Theta)/180
          ball.p = ball.m*v0*vector(cos(theta),sin(theta),0)
          rho = 1.225
          R = 0.10795
          C = 0.275
          Cl = 0.325
          
          M = vector(0, 1, 0)
          
          A = pi*(R**2)
          
          t = 0
          dt = 0.001
          
          while ball.pos.x <= (r0.x + 10.9728):
            rate(10000000)
            ball.v = (ball.p / ball.m) - (vair)
            vperp = cross(norm(ball.v), M)
            Ffd = (mag(ball.m*g*0.05)*-norm(ball.v)) - (0.5*rho*A*C*(mag(ball.v)**2)*norm(ball.v))
            Flift = (0.5*rho*A*Cl*(mag(ball.v)**2)*norm(vperp))
            Fnet = Ffd + Flift
            ball.p = ball.p + Fnet*dt
            ball.pos = ball.pos + ball.p*dt / ball.m
            t = t + dt
          
          IdAng = 180*(atan((ball.pos.z + 3.54965)/(ball.pos.x + 15)))/pi
          
          IdAn = atan((ball.pos.z + 3.54965)/(ball.pos.x + 15))
          
          if vz <= -5:
            IdAn -= 0.01
            IdAn -= abs(vz - 5)*0.001
          
          IdAngLl = [IdAng]
          
          ball3 = sphere(pos = vector(-15,0,0), radius = 0.2159, color = color.yellow, make_trail = False)
          ball3.m = 0.430
          Theta = 0
          theta = (pi*Theta)/180
          ball3.p = ball3.m*v0*vector(cos(theta),sin(theta),tan(-IdAn))
          
          t = 0
          
          while ball3.pos.x <= (r0.x + 10.9728):
            rate(100000)
            ball3.v = (ball3.p / ball3.m) - (vair)
            vperp = cross(norm(ball3.v), M)
            Ffd = (mag(ball3.m*g*0.05)*-norm(ball3.v)) - (0.5*rho*A*C*(mag(ball3.v)**2)*norm(ball3.v))
            Flift = (0.5*rho*A*Cl*(mag(ball3.v)**2)*norm(vperp))
            Fnet = Ffd + Flift
            ball3.p = ball3.p + Fnet*dt
            ball3.pos = ball3.pos + ball3.p*dt / ball3.m
            t = t + dt
            
          ball.pos = vector(r0)
          M = vector(0, -1, 0)
          
          IdAngLl = [IdAng, t]
          
          Theta = 0
          theta = (pi*Theta)/180
          ball.p = ball.m*v0*vector(cos(theta),sin(theta),0)
          
          while ball.pos.x <= (r0.x + 10.9728):
            rate(10000000)
            ball.v = (ball.p / ball.m) - (vair)
            vperp = cross(norm(ball.v), M)
            Ffd = (mag(ball.m*g*0.05)*-norm(ball.v)) - (0.5*rho*A*C*(mag(ball.v)**2)*norm(ball.v))
            Flift = (0.5*rho*A*Cl*(mag(ball.v)**2)*norm(vperp))
            Fnet = Ffd + Flift
            ball.p = ball.p + Fnet*dt
            ball.pos = ball.pos + ball.p*dt / ball.m
            t = t + dt
          
          IdAng = 180*(atan((abs(ball.pos.z) + 3.54965)/(ball.pos.x + 15)))/pi
          
          IdAn = atan((abs(ball.pos.z) + 3.54965)/(ball.pos.x + 15))
          
          if vz >= 5:
            IdAn -= 0.01
            IdAn -= abs(vz - 5)*0.001
          
          IdAngLr = [IdAng]
          
          ball3 = sphere(pos = vector(-15,0,0), radius = 0.2159, color = color.yellow, make_trail = False)
          ball3.m = 0.430
          Theta = 0
          theta = (pi*Theta)/180
          ball3.p = ball3.m*v0*vector(cos(theta),sin(theta),tan(IdAn))
          
          t = 0
          
          while ball3.pos.x <= (r0.x + 10.9728):
            rate(100000)
            ball3.v = (ball3.p / ball3.m) - (vair)
            vperp = cross(norm(ball3.v), M)
            Ffd = (mag(ball3.m*g*0.05)*-norm(ball3.v)) - (0.5*rho*A*C*(mag(ball3.v)**2)*norm(ball3.v))
            Flift = (0.5*rho*A*Cl*(mag(ball3.v)**2)*norm(vperp))
            Fnet = Ffd + Flift
            ball3.p = ball3.p + Fnet*dt
            ball3.pos = ball3.pos + ball3.p*dt / ball3.m
            t = t + dt
            
          ball.pos = vector(r0)
          
          IdAngLr = [IdAng, t]
          
          if IdAngLr[1] < time and IdAngLl[1] < time:
            Goal = True
          else:
            v0 += 0.125
        
        M = vector(0, 1, 0)
        IdAn = ((IdAngLl[0])*pi)/180
        
        ball3 = sphere(pos = vector(-15,0,0), radius = 0.2159, color = color.yellow, make_trail = True)
        ball3.m = 0.430
        Theta = 0
        theta = (pi*Theta)/180
        ball3.p = ball3.m*v0*vector(cos(theta),sin(theta),tan(-IdAn))
        
        while ball3.pos.x <= (r0.x + 10.9728):
          rate(100000)
          ball3.v = (ball3.p / ball3.m) - (vair)
          vperp = cross(norm(ball3.v), M)
          Ffd = (mag(ball3.m*g*0.05)*-norm(ball3.v)) - (0.5*rho*A*C*(mag(ball3.v)**2)*norm(ball3.v))
          Flift = (0.5*rho*A*Cl*(mag(ball3.v)**2)*norm(vperp))
          Fnet = Ffd + Flift
          ball3.p = ball3.p + Fnet*dt
          ball3.pos = ball3.pos + ball3.p*dt / ball3.m
          t = t + dt
          print("")
        
        M = vector(0, -1, 0)
        IdAn = ((IdAngLr[0])*pi)/180
        
        ball3 = sphere(pos = vector(-15,0,0), radius = 0.2159, color = color.yellow, make_trail = True)
        ball3.m = 0.430
        Theta = 0
        theta = (pi*Theta)/180
        ball3.p = ball3.m*v0*vector(cos(theta),sin(theta),tan(IdAn))
        
        while ball3.pos.x <= (r0.x + 10.9728):
          rate(100000)
          ball3.v = (ball3.p / ball3.m) - (vair)
          vperp = cross(norm(ball3.v), M)
          Ffd = (mag(ball3.m*g*0.05)*-norm(ball3.v)) - (0.5*rho*A*C*(mag(ball3.v)**2)*norm(ball3.v))
          Flift = (0.5*rho*A*Cl*(mag(ball3.v)**2)*norm(vperp))
          Fnet = Ffd + Flift
          ball3.p = ball3.p + Fnet*dt
          ball3.pos = ball3.pos + ball3.p*dt / ball3.m
          t = t + dt
          print("")
          
        print("The optimal sideways angle, for the projectile on the left was:", IdAngLl[0], "degrees.")
        print("It took:", IdAngLl[1], "seconds.")
        print("\nThe optimal sideways angle, for the projectile on the right, was:", IdAngLr[0], "degrees.")
        print("It took:", IdAngLr[1], "seconds.")
        print("The minimum required velocity is", v0, "meters per second.")
        
        accel = ((((v0*(legmass + 0.430))/(legmass*(1 + cr)))**2)-(vli0**2))/(2*distance)
        print("\nThe kicking appendage must be dragged", distance, "meters at an acceleration of", accel, "meters per second.")

    else:
        print("Please enter a valid integer, either 1 or 2.")

print("\nInitial conditions: 1. Wind velocity was <" + vx + ", " + vy + ", " + vz + "> m/s, 2. Dive-time was ", time + "s, 3. Leg mass was " + legmass, "kg, 4. Coefficient of Restitution was", cr + ", the kicking leg was dragged 5.", distance + "m for 6.", vli0 + "m/s")