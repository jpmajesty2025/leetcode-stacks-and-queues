'''
We are given an array asteroids of integers representing asteroids in a row. The indices of the asteroid in the array 
represent their relative position in space.

For each asteroid, the absolute value represents its size, and the sign represents its direction (positive meaning right, 
negative meaning left). Each asteroid moves at the same speed.

Find out the state of the asteroids after all collisions. If two asteroids meet, the smaller one will explode. 
If both are the same size, both will explode. Two asteroids moving in the same direction will never meet.


'''

def asteroid_collision(asteroids: list[int]) -> list[int]:
    stack: list[int] = []
    for asteroid in asteroids:
        alive = True
        # A left-moving asteroid only collides with a right-moving one
        # already resting on top of the stack.
        while alive and stack and asteroid < 0 < stack[-1]:
            if stack[-1] < -asteroid:
                stack.pop()
            elif stack[-1] == -asteroid:
                stack.pop()
                alive = False
            else:
                alive = False
        if alive:
            stack.append(asteroid)
    return stack