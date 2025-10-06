import numpy as np
import matplotlib.pyplot as plt
import math

def generate_points(R = 250, r = 10, d = 5):
    k = r / R
    l = d / r
    numerator = round(R - r) # rounding numerator to avoid floating point issues
    denominator = round(r) # rounding denominator to avoid floating point issues
    g = math.gcd(numerator, denominator) # greatest common divisor
    q = denominator // g # number of rotations
    xs = []
    ys = []
    for theta in range(0, 360 * q, 5):
        theta_rad = np.radians(theta)
        x = R*((1-k)*np.cos(theta_rad) + l*k*np.cos(((1-k)/k)*theta_rad))
        y = R*((1-k)*np.sin(theta_rad) - l*k*np.sin(((1-k)/k)*theta_rad))
        xs.append(x)
        ys.append(y)
    return xs, ys

def main():
    xs, ys = generate_points()
    plt.figure(figsize=(8, 8))
    plt.plot(xs, ys)
    plt.axis('equal')
    plt.title('Hypotrochoid')
    plt.show()
        
        
if __name__ == "__main__":
    main()