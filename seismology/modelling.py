import math


def calc_M(M0, Vs, dsigma, C):
    M = (2/3)*math.log(M0) - 10.7
    f0 = 4.9*10**6*Vs*(dsigma/M0)**(1/3)
    Sa = Sb = 1
    S = Sa * Sb
    E = C*M0*S
    return M

def main():
    print('modelling!')
    

if __name__ == '__main__':
    main()