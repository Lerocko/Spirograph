"""Spirograph Generator
This program generates and visualizes hypotrochoid patterns (spirographs) based on user-defined parameters.
Users can input the radii of the fixed and rolling circles, as well as the distance from the center of the rolling circle to the drawing point.
The program animates the drawing process and allows users to save the resulting spirograph as an image file.
Author: Lerocko Mendoza Zamora
Date: 2025-10-11"""


#Libraries
import numpy as np
import matplotlib.pyplot as plt
import math
import os


#Auxilary functions
""" Handle keyboard interrupts gracefully and scale parameters if needed. """

def handle_interrupt():
    """ Handle keyboard interrupt (Ctrl+C) gracefully by asking the user if they want to exit. """
    print()
    try:
        # Prompt user for confirmation to exit
        while True:
            choice = input("Are you sure you want to exit? (y/n): ").strip().lower()
            if choice in ["y", "yes"]:
                print("Exiting program. Goodbye!")
                exit()
            elif choice in ["n", "no"]:
                print("Resuming program...\n")
                return
            else:
                print("Please answer with 'y' or 'n'.")
    # If another interrupt occurs during the prompt, exit immediately
    except KeyboardInterrupt:
        print("\nExiting program. Goodbye!")
        exit()

def check_and_scale_parameters(R, r, d):
    """ Scale parameters if one or more are too small to avoid floating point precision issues. """
    min_value = min([val for val in [R, r, d] if val > 0]) # find the smallest positive value
    
    # determine scaling factor and modify parameters
    if min_value < 1:
        n = -int(math.floor(math.log10(min_value))) + 1 # number of decimal places to shift
        scale_factor = 10 ** n
        return R * scale_factor, r * scale_factor, d * scale_factor, scale_factor # return scaled values and scale factor
    # no scaling needed
    else:
        return R, r, d, 1 # no scaling needed


#In and output functions
""" Get user input, answer yes/no questions, and save the spirograph figure with error handling. """

def get_user_input():
    """ Get user input for the spirograph parameters with error handling. """
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
        except KeyboardInterrupt:
            handle_interrupt()
            continue

def answer_yes_no(prompt):
    """ Prompt the user with a yes/no question and return True for yes and False for no. """
    while True:
        try:
            answer = input(prompt).strip().lower()
        except KeyboardInterrupt:
            handle_interrupt()
            continue
        if answer in ['y', 'yes']:
            return True
        elif answer in ['n', 'no']:
            return False
        else:
            print("Please answer with 'y' or 'n'.")

def save_spirofig(fig):
    """ Prompt the user to save the spirograph figure with error handling. """
    while True:
        try:
            filename = input("Enter filename to save the spirograph (or press Enter to skip saving): ").strip()

            if filename == "":
                print("File not saved.")
                break
            
            # Check and append appropriate file extension
            name, ext = os.path.splitext(filename)
            
            # If no extension is provided, ask the user to specify one
            if not ext:
                ext_choice = input("Please specify the format to save (.png/.jpg/.jpeg): ").strip().lower()
                
                # Default to .png if the input is invalid
                if ext_choice not in [".png", ".jpg", ".jpeg"]:
                    print("Invalid format specified. It will be saved as .png by default.")
                    ext_choice = ".png"
                    print(f"\nSpirograph will be saved as {name + ext_choice}")
                filename = name + ext_choice
                
            # If an extension is provided, validate it
            else:
                if ext.lower() not in [".png", ".jpg", ".jpeg"]:
                    print("Unsupported file format. Please use .png, .jpg, or .jpeg.")
                    continue
            
            # Save the figure
            fig.savefig(filename, dpi=300)
            print(f"\nSpirograph has been successfully saved as: {filename}")
            break

        # Handle exceptions during file saving
        except Exception as e:
            print(f"Error saving file: {e}. Please try again.")
        except KeyboardInterrupt:
            handle_interrupt()
            continue


#Calculation and logic functions
""" Generate spirograph points based on user-defined parameters. """
def generate_points(R = 220, r = 65, d = 110, scale_factor = 1): # default example parameters
    """ Generate the (x, y) points of the spirograph based on the given parameters. """
    # Scale parameters if they are too small
    if R < 1 or r < 1 or d < 1:
        R, r, d, scale_factor = check_and_scale_parameters(R, r, d)
    
    # Calculate points
    k = r / R
    l = d / r
    numerator = round(R - r) # rounding numerator to avoid floating point issues
    denominator = round(r) # rounding denominator to avoid floating point issues
    g = math.gcd(numerator, denominator) # greatest common divisor
    q = (denominator // g) # number of rotations
    q = min(q, 50) # limit to 50 rotations for practicality
    xs, ys = [], []
    
    # Generate points
    for theta in range(0, 360 * q, 5):
        theta_rad = np.radians(theta)

        # Hypotrochoid equations
        x = R*((1-k)*np.cos(theta_rad) + l*k*np.cos(((1-k)/k)*theta_rad)) 
        y = R*((1-k)*np.sin(theta_rad) - l*k*np.sin(((1-k)/k)*theta_rad))
        # Scale down points for plotting
        xs.append(x/scale_factor)
        ys.append(y/scale_factor)
    return xs, ys, scale_factor


#Visualization functions
""" Draw and animate the spirograph using matplotlib. """
def draw_spirograph(xs, ys, scale_factor=1):
    # Set up the plot
    plt.ion() # turn on interactive mode
    fig, ax = plt.subplots(figsize=(8, 8)) # create a square figure
    ax.set_aspect('equal') # equal scaling
    ax.set_xlim(min(xs)-(10/scale_factor), max(xs)+(10/scale_factor)) # set limits with some padding
    ax.set_ylim(min(ys)-(10/scale_factor), max(ys)+(10/scale_factor)) # set limits with some padding
    ax.set_title('Hypotrochoid') # title
    line, = ax.plot([], [], color='blue') # initialize line object
    
    # Animate the drawing        
    for i in range(len(xs)):
        line.set_data(xs[:i], ys[:i])
        plt.pause(0.001)
    plt.ioff() # turn off interactive mode
    plt.show() # keep the plot open after animation
    plt.close(fig) # close the figure to prevent memory leaks
    return fig


#Main function
""" Main function to run the spirograph generator program. """
def main():
    # Welcome message
    print("Welcome to the Spirograph Generator!")
    print("You can create beautiful hypotrochoid patterns by specifying the parameters.")
    
    # Show example spirograph
    if answer_yes_no("\nWould you like to see an example spirograph first? (y/n): ") == True:
        print("\nLet's see an example spirograph first.")
        xs, ys, scale_factor = generate_points()
        fig = draw_spirograph(xs, ys, scale_factor)
    
    # Main loop for user interaction
    while True:
        R, r, d = get_user_input()
        xs, ys, scale_factor = generate_points(R, r, d)
        fig = draw_spirograph(xs, ys, scale_factor)
        save_spirofig(fig)
        
        # Ask if the user wants to draw another spirograph
        if not answer_yes_no("Do you want to draw another spirograph? (y/n): "):
            print("Thank you for using the Spirograph Generator. Goodbye!")
            break


#Ejecution guard
if __name__ == "__main__":
    main()
 
                