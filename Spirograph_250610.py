import numpy as np
import matplotlib.pyplot as plt
import math

def draw_spirograph(xs, ys):
    plt.ion()
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect('equal')
    ax.set_xlim(min(xs)-10, max(xs)+10)
    ax.set_ylim(min(ys)-10, max(ys)+10)
    ax.set_title('Hypotrochoid')
    line, = ax.plot([], [], color='blue')
            
    for i in range(len(xs)):
        line.set_data(xs[:i], ys[:i])
        plt.pause(0.001)
    plt.ioff()
    plt.show()
    plt.close(fig)

def get_user_input():
    while True:
        try:
            R = float(input("Enter the radius of the fixed circle (R): "))
            r = float(input("Enter the radius of the rolling circle (r): "))
            d = float(input("Enter the distance from the center of the rolling circle to the drawing point (d): "))
            if R <= 0 or r <= 0 or d < 0:
                print("Please enter positive values for R and r, and non-negative value for d.")
                continue
            return R, r, d
        except ValueError:
            print("Invalid input. Please enter numeric values.")

def generate_points(R = 220, r = 65, d = 110):
    k = r / R
    l = d / r
    numerator = round(R - r) # rounding numerator to avoid floating point issues
    denominator = round(r) # rounding denominator to avoid floating point issues
    g = math.gcd(numerator, denominator) # greatest common divisor
    q = (denominator // g) # number of rotations
    q = min(q, 50) # limit to 50 rotations for practicality
    xs, ys = [], []
    for theta in range(0, 360 * q, 5):
        theta_rad = np.radians(theta)
        x = R*((1-k)*np.cos(theta_rad) + l*k*np.cos(((1-k)/k)*theta_rad))
        y = R*((1-k)*np.sin(theta_rad) - l*k*np.sin(((1-k)/k)*theta_rad))
        xs.append(x)
        ys.append(y)
    return xs, ys

def main():
    xs, ys = generate_points()
    draw_spirograph(xs, ys)
    while True:
        R, r, d = get_user_input()
        xs, ys = generate_points(R, r, d)
        draw_spirograph(xs, ys)
        try:
            cont = input("Do you want to draw another spirograph? (y/n): ").strip().lower()
            if cont != 'y':
                break
        except EOFError:
            break
                
        
if __name__ == "__main__":
    main()