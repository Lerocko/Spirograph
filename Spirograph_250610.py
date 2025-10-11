import numpy as np
import matplotlib.pyplot as plt
import math
import os

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
    return fig

def get_user_input():
    while True:
        try:
            R = float(input("Enter the radius of the fixed circle (R): "))
            r = float(input("Enter the radius of the rolling circle (r): "))
            d = float(input("Enter the distance from the center of the rolling circle to the drawing point (d): "))
            if R <= 0 or r <= 0 or d <= 0:
                print("Please enter only positive values for R and r, and d.")
                continue
            return R, r, d
        except ValueError:
            print("Invalid input. Please enter numeric values.")
        
def generate_points(R = 220, r = 65, d = 110, scale_factor = 1):
    if R < 1 or r < 1 or d < 1:
        R, r, d, scale_factor = check_and_scale_parameters(R, r, d)
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
        xs.append(x/scale_factor)
        ys.append(y/scale_factor)
    return xs, ys

def check_and_scale_parameters(R, r, d):
    """ Scale parameters if one or more are too small to avoid floating point precision issues. """
    min_value = min([val for val in [R, r, d] if val > 0]) # find the smallest positive value
    if min_value < 1:
        n = -int(math.floor(math.log10(min_value))) + 1 # number of decimal places to shift
        scale_factor = 10 ** n
        return R * scale_factor, r * scale_factor, d * scale_factor, scale_factor # return scaled values and scale factor
    else:
        return R, r, d, 1 # no scaling needed

def save_spirofig(fig):
    while True:
        try:
            filename = input("Enter filename to save the spirograph (or press Enter to skip saving): ").strip()

            if filename == "":
                print("File not saved.")
                break

            name, ext = os.path.splitext(filename)
            
            if not ext:
                ext_choice = input("Please specify the format to save (.png/.jpg/.jpeg): ").strip().lower()
                if ext_choice not in [".png", ".jpg", ".jpeg"]:
                    ext_choice = ".png"
                filename = name + ext_choice
            else:
                if ext.lower() not in [".png", ".jpg", ".jpeg"]:
                    print("Unsupported file format. Please use .png, .jpg, or .jpeg.")
                    continue
            
            fig.savefig(filename, dpi=300)
            print(f"Spirograph saved as {filename}")
            break
        except Exception as e:
            print(f"Error saving file: {e}. Please try again.")
     
def answer_yes_no(prompt):
    while True:
        try:
            answer = input(prompt).strip().lower()
        except KeyboardInterrupt:
            print("\nExiting program. Goodbye!")
            return False
        if answer in ['y', 'yes']:
            return True
        elif answer in ['n', 'no']:
            return False
        else:
            print("Please answer with 'y' or 'n'.")

def main():
    print("Welcome to the Spirograph Generator!")
    print("\nYou can create beautiful hypotrochoid patterns by specifying the parameters.")
    
    if answer_yes_no("\nWould you like to see an example spirograph first? (y/n): ") == True:
        print("\nLet's see an example spirograph first.")
        xs, ys = generate_points()
        fig = draw_spirograph(xs, ys)
    
    while True:
        R, r, d = get_user_input()
        xs, ys = generate_points(R, r, d)
        fig = draw_spirograph(xs, ys)
        save_spirofig(fig)
        
        if not answer_yes_no("Do you want to draw another spirograph? (y/n): "):
            print("Thank you for using the Spirograph Generator. Goodbye!")
            break
               
            
      
if __name__ == "__main__":
    while True:
        try:
            main()
            break
        except KeyboardInterrupt:
            print()  # salto de línea limpio
            if answer_yes_no("Are you sure you want to exit? (y/n): "):
                print("Exiting program. Goodbye!")
                break
            else:
                print("Resuming program...\n")
                continue