# Example 1
Write a code to simulate a cantiliver beam. 
The left side of the beam is fixed (all DOF of U1, U2 and UR1) are equal to zero.
A concentrated force of F is applied on the right side of the beam in the tip. 
The lenth of the beam is 1000 mm.
The Young's
Use element size of 

# Guideline
Use macro manager and test your script.


## Solution
0- Do all the step of the simulation.
1- Save the macrom from macro manager in abaqus. 
2- Clean the code. 
 2-1 Seperate the functions (geometry, material, step, ...)
 2-2 Asing correct input to the function
 2-3 Write an instruction for each function. 
 2-4 Test the functions on Abaqus.
 
 
The macro has been saved by macro manager from abaqus. 
When you do the simulation in abaqus, remember the numbers that you inser for each 
task. Using these numbers, then you are able to extract the corresponding functions. 
For instance if you inser the Young's modulus of E=200e3, you can find this number in script
and you can extract thisfrunction from the script. 


