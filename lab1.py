import sys

L1 = 2.5E-04
L2 = 2.5E-04
C1 = 2.5E-11
C2 = 5.0E-11
Ccb = 1.0E-9
R2 = 250.0

Q10 = 2.5E-10
Q20 = 0.0
I10 = 0.0
I20 = 0.0

Tmin = 0.0
Tmax = 3.0E-04
N = 1000000

A11 = 1 / (L1 * C1) + 1 / (L1 * Ccb)
A12 = 1 / (L1 * Ccb)
A21 = 1 / (L2 * Ccb)
A22 = 1 / (L2 * C2) + 1 / (L2 * C2)
A23 = R2 / L2

FILE_NAME = 'output.out'

def f1(i1):
    return i1

def f2(q1, q2):
    return -A11 * q1 + A12 * q2

def f3(i2):
    return i2

def f4(q1, q2, i2):
    return A21 * q1 - A22 * q2 - A23 * i2

def rk4(tmin=Tmin, tmax=Tmax, n=N, q10=Q10, q20=Q20, i10=I10, i20=I20):
    h = (tmax - tmin) / n
    vt = [0] * (n + 1)
    vq1 = [0] * (n + 1)
    vq2 = [0] * (n + 1)
    vi1 = [0] * (n + 1)
    vi2 = [0] * (n + 1)
    vur2 = [0] * (n + 1)
    vt[0] = t = tmin
    vq1[0] = q1 = q10
    vq2[0] = q2 = q20
    vi1[0] = i1 = i10
    vi2[0] = i2 = i20
    vur2[0] = i2 * R2
    for i in range(1, n + 1):
        k1 = h * f1(i1)
        l1 = h * f2(q1, q2)
        m1 = h * f3(i2)
        n1 = h * f4(q1, q2, i2)

        k2 = h * f1(i1 + l1/2)
        l2 = h * f2(q1 + k1/2, q2 + m1/2)
        m2 = h * f3(i2 + n1/2)
        n2 = h * f4(q1 + k1/2, q2 + m1/2, i2 + n1/2)

        k3 = h * f1(i1 + l2/2)
        l3 = h * f2(q1 + k2/2, q2 + m2/2)
        m3 = h * f3(i2 + n2/2)
        n3 = h * f4(q1 + k2/2, q2 + m2/2, i2 + n2/2)

        k4 = h * f1(i1 + l3)
        l4 = h * f2(q1 + k3, q2 + m3)
        m4 = h * f3(i2 + n3)
        n4 = h * f4(q1 + k3, q2 + m3, i2 + n3)

        vq1[i] = q1 = q1 + (k1 + 2 * k2 + 2 * k3 + k4) / 6
        vq2[i] = q2 = q2 + (m1 + 2 * m2 + 2 * m3 + m4) / 6
        vi1[i] = i1 = i1 + (l1 + 2 * l2 + 2 * l3 + l4) / 6
        vi2[i] = i2 = i2 + (n1 + 2 * n2 + 2 * n3 + n4) / 6

        vur2[i] = i2 * R2
        vt[i] = t = t + h
    return vt, vq1, vq2, vi1, vi2, vur2

def plot_results(vt, vq1, vq2, vi1, vi2, vur2):
    import matplotlib.pyplot as plt

    f1 = plt.figure(1)
    f1.suptitle('Q1')
    plt.xlabel('t')
    plt.ylabel('Q')
    plt.plot(vt, vq1, color='green')

    f2 = plt.figure(2)
    f2.suptitle('Q2')
    plt.xlabel('t')
    plt.ylabel('Q')
    plt.plot(vt, vq2, color='blue')

    f3 = plt.figure(3)
    f3.suptitle('I1')
    plt.xlabel('t')
    plt.ylabel('I')
    plt.plot(vt, vi1, color='red')

    f4 = plt.figure(4)
    f4.suptitle('I2')
    plt.xlabel('t')
    plt.ylabel('I')
    plt.plot(vt, vi2, color='yellow')

    f5 = plt.figure(5)
    f5.suptitle('Ur2')
    plt.xlabel('t')
    plt.ylabel('U')
    plt.plot(vt, vur2, color='brown')

    plt.show()
    return True

if __name__ == '__main__':
    if '--plot' in sys.argv:
        import csv

        with open(FILE_NAME, 'r') as f:
            reader = csv.reader(f, delimiter=' ')
            vt, vq1, vq2, vi1, vi2, vur2 = list(zip(*reader))
            plot_results(vt, vq1, vq2, vi1, vi2, vur2)
    else:
        vt, vq1, vq2, vi1, vi2, vur2 = rk4()

        with open(FILE_NAME, 'w') as f:
            for t, q1, q2, i1, i2, ur2 in list(zip(vt, vq1, vq2, vi1, vi2, vur2))[::100]:
                f.write("%0.10f %0.20f %0.20f %0.20f %0.20f %0.20f\n" % (t, q1, q2, i1, i2, ur2))
