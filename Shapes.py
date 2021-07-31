# -*- coding: utf-8 -*-

import numpy as np

I_0 = np.zeros((4, 4), dtype = str)
I_1 = np.zeros((4, 4), dtype = str)
I_2 = np.zeros((4, 4), dtype = str)
I_3 = np.zeros((4, 4), dtype = str)
J_0 = np.zeros((4, 4), dtype = str)
J_1 = np.zeros((4, 4), dtype = str)
J_2 = np.zeros((4, 4), dtype = str)
J_3 = np.zeros((4, 4), dtype = str)
L_0 = np.zeros((4, 4), dtype = str)
L_1 = np.zeros((4, 4), dtype = str)
L_2 = np.zeros((4, 4), dtype = str)
L_3 = np.zeros((4, 4), dtype = str)
O = np.zeros((4, 4), dtype = str)
S_0 = np.zeros((4, 4), dtype = str)
S_1 = np.zeros((4, 4), dtype = str)
S_2 = np.zeros((4, 4), dtype = str)
S_3 = np.zeros((4, 4), dtype = str)
T_0 = np.zeros((4, 4), dtype = str)
T_1 = np.zeros((4, 4), dtype = str)
T_2 = np.zeros((4, 4), dtype = str)
T_3 = np.zeros((4, 4), dtype = str)
Z_0 = np.zeros((4, 4), dtype = str)
Z_1 = np.zeros((4, 4), dtype = str)
Z_2 = np.zeros((4, 4), dtype = str)
Z_3 = np.zeros((4, 4), dtype = str)

for i in range (4) :
    I_0[i][2] = '1'

I_1[2] = ['1']*4

for i in range (4) :
    I_2[i][1] = '1'

I_3[1] = ['1']*4

J_0[1][2] = J_0[2][2] = J_0[3][1:3] = '2'

J_1[1][1] = J_1[2][1:4] = '2'

J_2[1][2:4] = J_2[2][2] = J_2[3][2] = '2'

J_3[2][1:4] = J_3[3][3] = '2'

L_0[1][1] = L_0[2][1] = L_0[3][1:3] = '3'

L_1[2][0:3] = L_1[3][0] = '3'

L_2[1][0:2] = L_2[2][1] = L_2[3][1] = '3'

L_3[2][0:3] = L_3[1][2] = '3'

O[1][1:3] = O[2][1:3] = '4'

S_0[1][1] = S_0[2][1:3] = S_0[3][2] = '5'

S_1[2][1:3] = S_1[3][0:2] = '5'

S_2[1][0] = S_2[2][0:2] = S_2[3][1] = '5'

S_3[1][1:3] = S_3[2][0:2] = '5'

T_0[1][2] = T_0[2][1:3] = T_0[3][2] = '6'

T_1[1][2] = T_1[2][1:4] = '6'

T_2[1][2] = T_2[2][2:4] = T_2[3][2] = '6'

T_3[3][2] = T_3[2][1:4] = '6'

Z_0[1][2] = Z_0[2][1:3] = Z_0[3][1] = '7'

Z_1[2][0:2] = Z_1[3][1:3] = '7'

Z_2[1][1] = Z_2[2][0:2] = Z_2[3][0] = '7'

Z_3[1][0:2] = Z_3[2][1:3] = '7'

Shapes = [I_0, I_1, I_2, I_3, J_0, J_1, J_2, J_3, L_0, L_1, L_2, L_3, O, O, O, O, S_0, S_1, S_2, S_3, T_0, T_1, T_2, T_3, Z_0, Z_1, Z_2, Z_3]
