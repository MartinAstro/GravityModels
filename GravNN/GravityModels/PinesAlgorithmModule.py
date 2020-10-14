import numpy as np
from numba import jit, prange, njit

@njit 
def getK(x):
    return 1.0 if (x == 0) else 2.0

@njit 
def compute_n_matrices(N):
    n1 = np.ones((N+2, N+2))*np.nan
    n2 = np.ones((N+2, N+2))*np.nan
    n1q = np.ones((N+2, N+2))*np.nan
    n2q = np.ones((N+2, N+2))*np.nan

    for l in range(0, N+2):
        for m in range(0, l+1):
            if (l >= m + 2):
                n1[l][m] = np.sqrt(((2.0*l+1.0)*(2.0*l-1.0))/((l-m)*(l+m)))
                n2[l][m] = np.sqrt(((l+m-1.0)*(2.0*l+1.0)*(l-m-1.0))/((l+m)*(l-m)*(2.0*l-3.0)))
            if (l < N+1):
                if (m < l): # this may need to also ensure that l < N+1 
                    n1q[l][m] = np.sqrt(((l-m)*getK(m)*(l+m+1.0))/getK(m+1))
                n2q[l][m] = np.sqrt(((l+m+2.0)*(l+m+1.0)*(2.0*l+1.0)*getK(m))/((2.0*l+3.0)*getK(m+1.0)))
    return n1, n2, n1q, n2q

@njit 
def compute_acc(positions, N, mu, a, n1, n2, n1q, n2q, cbar, sbar):
    acc = np.zeros(positions.shape)
    for i in range(0, int(len(positions)/3)):
        r = np.linalg.norm(positions[3*i:3*(i+1)])
        [s, t, u] = positions[3*i:3*(i+1)]/r

        rE = np.zeros((N+2,))
        iM = np.zeros((N+2,))

        rhol = np.zeros((N+2,))

        aBar = np.zeros((N+2, N+2))
        aBar[0,0] = 1.0

        rho = a/r
        rhol[0] = mu/r
        rhol[1] = rhol[0]*rho

        for l in range(1, N+2):
            aBar[l][l] = np.sqrt(((2.0*l+1.0)*getK(l))/((2.0*l*getK(l-1))))*aBar[l-1][l-1]
            aBar[l][l-1] = np.sqrt((2.0*l)*getK(l-1)/getK(l))*aBar[l][l]*u
        
        for m in range(0, N+2):
            for l in range(m+2, N+2):
                aBar[l][m] = u*n1[l][m]*aBar[l-1][m] - n2[l][m]*aBar[l-2][m]
            rE[m] = 1.0 if m == 0 else s*rE[m-1] - t*iM[m-1]
            iM[m] = 0.0 if m == 0 else s*iM[m-1] + t*rE[m-1]
        
        a1, a2, a3, a4 = 0.0, 0.0, 0.0, 0.0
        for l in range(1, N+1):
            rhol[l+1] = rho*rhol[l]
            sum_a1, sum_a2, sum_a3, sum_a4 = 0.0, 0.0, 0.0, 0.0
            for m in range(0, l+1):
                D = cbar[l][m]*rE[m] + sbar[l][m]*iM[m]
                E = 0.0 if m == 0 else cbar[l][m]*rE[m-1] + sbar[l][m]*iM[m-1]
                F = 0.0 if m == 0 else sbar[l][m]*rE[m-1] - cbar[l][m]*iM[m-1]

                sum_a1 += m*aBar[l][m]*E
                sum_a2 += m*aBar[l][m]*F

                if m < l:
                    sum_a3 += n1q[l][m]*aBar[l][m+1]*D
                sum_a4 += n2q[l][m]*aBar[l+1][m+1]*D
            a1 += rhol[l+1]/a*sum_a1
            a2 += rhol[l+1]/a*sum_a2
            a3 += rhol[l+1]/a*sum_a3
            a4 -= rhol[l+1]/a*sum_a4
        a4 -= rhol[1]/a

        acc[3*i:3*(i+1)] = (np.array([a1, a2, a3]) + np.array([s,t,u])*a4)#.tolist()
    return acc

@njit(parallel=True, cache=True) 
def compute_acc_parallel(positions, N, mu, a, n1, n2, n1q, n2q, cbar, sbar):
    acc = np.zeros(positions.shape)
    for i in prange(0, int(len(positions)/3)):
        acc[3*i:3*(i+1)] = compute_acc_thread(positions[3*i:3*(i+1)], N, mu, a, n1, n2, n1q, n2q, cbar, sbar)

@njit(cache=True)
def compute_acc_thread(position, N, mu, a, n1, n2, n1q, n2q, cbar, sbar):
    acc = np.zeros(position.shape)
    r = np.linalg.norm(position)
    [s, t, u] = position/r

    rE = np.zeros((N+2,))
    iM = np.zeros((N+2,))

    rhol = np.zeros((N+2,))

    aBar = np.zeros((N+2, N+2))
    aBar[0,0] = 1.0

    rho = a/r
    rhol[0] = mu/r
    rhol[1] = rhol[0]*rho

    for l in range(1, N+2):
        aBar[l][l] = np.sqrt(((2.0*l+1.0)*getK(l))/((2.0*l*getK(l-1))))*aBar[l-1][l-1]
        aBar[l][l-1] = np.sqrt((2.0*l)*getK(l-1)/getK(l))*aBar[l][l]*u
    
    for m in range(0, N+2):
        for l in range(m+2, N+2):
            aBar[l][m] = u*n1[l][m]*aBar[l-1][m] - n2[l][m]*aBar[l-2][m]
        rE[m] = 1.0 if m == 0 else s*rE[m-1] - t*iM[m-1]
        iM[m] = 0.0 if m == 0 else s*iM[m-1] + t*rE[m-1]
    
    a1, a2, a3, a4 = 0.0, 0.0, 0.0, 0.0
    for l in range(1, N+1):
        rhol[l+1] = rho*rhol[l]
        sum_a1, sum_a2, sum_a3, sum_a4 = 0.0, 0.0, 0.0, 0.0
        for m in range(0, l+1):
            D = cbar[l][m]*rE[m] + sbar[l][m]*iM[m]
            E = 0.0 if m == 0 else cbar[l][m]*rE[m-1] + sbar[l][m]*iM[m-1]
            F = 0.0 if m == 0 else sbar[l][m]*rE[m-1] - cbar[l][m]*iM[m-1]

            sum_a1 += m*aBar[l][m]*E
            sum_a2 += m*aBar[l][m]*F

            if m < l:
                sum_a3 += n1q[l][m]*aBar[l][m+1]*D
            sum_a4 += n2q[l][m]*aBar[l+1][m+1]*D
        a1 += rhol[l+1]/a*sum_a1
        a2 += rhol[l+1]/a*sum_a2
        a3 += rhol[l+1]/a*sum_a3
        a4 -= rhol[l+1]/a*sum_a4
    a4 -= rhol[1]/a

    return (np.array([a1, a2, a3]) + np.array([s,t,u])*a4)#.tolist()