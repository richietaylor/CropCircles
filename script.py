import scipy.optimize as opt
import numpy as np
import pandas as pd


def calculate_segment_area_from_height(radius, height):
    """
    Calculate the area of the segment given the radius of the circle and the height of the arc.

    Parameters:
    radius (float): The radius of the circle.
    height (float): The height of the arc.

    Returns:
    float: The area of the segment in square meters.
    """
    # Function to solve for theta
    def height_eq(theta):
        return radius * (1 - np.cos(theta / 2)) - height

    # Initial guess for theta
    theta_initial_guess = 2.0

    # Solve for theta
    theta_solution = opt.fsolve(height_eq, theta_initial_guess)[0]

    # Calculate the area of the segment
    area = (radius**2 / 2) * (theta_solution - np.sin(theta_solution))

    return area


def calculate_arc_height(radius, area):
    """
    Calculate the height of the arc (segment height) given the radius of the circle and the area of the segment.

    Parameters:
    radius (float): The radius of the circle.
    area (float): The area of the segment.

    Returns:
    tuple: A tuple containing the central angle (theta) in radians and the height of the arc (h) in meters.
    """
    def segment_area_eq(theta):
        return (radius**2 / 2) * (theta - np.sin(theta)) - area

    # Initial guess for theta
    theta_initial_guess = 2.0

    # Solve for theta
    theta_solution = opt.fsolve(segment_area_eq, theta_initial_guess)[0]

    # Calculate the height of the arc
    h = radius * (1 - np.cos(theta_solution / 2))

    return theta_solution, h

def calculate_All(radius, increment):
    data = []
    area = 0
    prev = 0
    difference = 0
    total = 0
    count = 1
    while True:
        
        area += increment
        theta, height = calculate_arc_height(radius, area)
        difference = height - prev
        if (difference < 0 or difference < 15):
            break
        # Append data to list
        data.append({
            "Cut": count,
            "Area (m^2)": round(area),
            "Distance from Circumference (m)": round(height),
            "Distance from last point (m)": round(difference)
        })
        prev = height
        count += 1

    remaining = (radius * 2 - prev)
    leftOver = calculate_segment_area_from_height(radius, remaining)
    data.append({
        "Cut": "Final",
        "Area (m^2)": "Left Over (m^2)",
        "Distance from Circumference (m)": round(leftOver),
        "Distance from last point (m)": round(leftOver)
    })
    
    return data




print("-----------------------------------\nWELCOME BUZZ\n-----------------------------------")

# 338.6
radius = float(input("Radius: "))
# 40000
increment = float(input("Area: "))
# print(f"Radius :{radius}\nArea Increment:{increment}")



# Create a DataFrame to store all results
all_data = []

for x in range(5):
    data = calculate_All(radius, increment + 5000 * x)
    all_data.extend(data)
    all_data.append({
        "Cut": "------",
        "Area (m^2)": "----------",
        "Distance from Circumference (m)": "----------",
        "Distance from last point (m)": "----------"
    })

# Convert the list of data to a DataFrame
df = pd.DataFrame(all_data)

# Save the DataFrame to an Excel file
df.to_excel(f"output_{radius}_{increment}.xlsx", index=False)

print("Success!")
