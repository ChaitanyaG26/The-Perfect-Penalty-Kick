# The-Perfect-Penalty-Kick
A physics simulation taking in environmental conditions to output the minimum possible velocity (and other appropriate variables) returning in a goal.

You may run the program at https://www.glowscript.org/#/user/cg%5fphysics/folder/MyPrograms/program/PenaltyKick,Sim/edit, which is my official glowscript. Click the button at the top.

The code itself is saved as sim-code.py and can be seen at the glowscript link above.

This specific version of the code utilizes:
1. Given inputs:

    a. The x-component of the wind velocity

    b. The y-component of the wind velocity

    c. The z-component of the wind velocity

    d. The time for the goalkeeper to reach the corner

    e. The leg mass

    f. The coefficient of restitution

    g. The distance the leg is dragged

    h. The initial speed of the foot before it is dragged

    i. Whether the projectile is airborne or earthbounded

    j. If it is airborne, whether it has top-/back-spin or left-/right-spin

3. A simulator testing the ideal angle left/right for the starting velocity

   // This is done through a program that gets the net force acting on the ball every given unit of time

    a. You start with the ball at a given velocity you want to test. Save its momentum
   
    b. Then, model a small change in time over which the velocity couldn't have changed much
   
        a. We will take the net force at the last instant
   
        b. Use that net force, multiply by dt, and add that to the most recent momentum
   
        c. Then, with the new momentum, divide by mass to get "average" velocity
   
        // Note, "average" is not the true average, but a close approximation over small dt
   
        d. Then multiply this velocity by dt and add it to the initial position vector
   
        e. Continue the simulation, updating the values along the way
   
5. A simulation of different speeds of the ball (with different angles above the horizontal for the airborne projectile), increasing slowly until a goal condition is reached
6. Output the ideal angle(s), ball velocity, and the required acceleration for the kicking appendage to reach the appropriate conditions above

// Note that since this was done on VPython, all the "test" simulations (yellow) and the "final" simulations are drawn (white) as the code works.
