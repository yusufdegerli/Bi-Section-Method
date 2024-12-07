def makingRoot(root):
    """
    The round(root) function rounds the root to the nearest integer.
    The expression abs(root - round(root)) < 1e-5 checks that the difference
    of the root to the rounded integer is very small (up to 5 digits).
    If the difference is very small, we determine that this root is actually
    an integer and we want to print it as an integer.
    """
    if abs(root - round(root)) < 1e-5:
        return str(int(round(root)))
    elif abs(root) < 1e-5:
        return "0"
    else:
        return f"{root:.5f}".rstrip('0').rstrip('.')

def resForX(coefficients, x):
    """
    Convert between different positional numeral systems (Horner's method)
    """
    res = 0  # Initialize the res
    for i, coeff in enumerate(coefficients[::-1]):   # Iterate over the coefficients in reverse order
        if i > 0:   # Skipping the constant
            res += coeff * (x ** i)  # Multiply the coefficient by x raised to the power of the index value of the coefficient
        else:
            res += coeff  # Add the constant term to the res
    return res  # Return the res

def bSectionRF(coefficients, a, b, c=1e-6, max_iterations=100): # c is the tolerance value, max_iterations is the maximum number of iterations
    """
    Using bi-section method and find the root of polynomial
    Evaluating the polynomial at the left and the right endpoint
    """
    fa = resForX(coefficients, a)
    fb = resForX(coefficients, b)

    if fa * fb > 0:    # Checking same sign
        raise ValueError(f"There is no root in these funcs. fa: {fa}, fb: {fb}") # Raise an error if the endpoints have the same sign

    itCnt = 1  # Start iteration count from 1. I did this because the iteration count can be at least 1 in the worst case if bisecting the interval is possible
    while (b - a) / 2 > c and itCnt < max_iterations: # Check if the interval is greater than the tolerance value and the iteration count is less than the maximum number of iterations
        midPoint = (a + b) / 2     # Calculate the middle point of the interval
        fMidPoint = resForX(coefficients, midPoint)  # Evaluate the polynomial at the middle point

        """Checking if the middle point is a root or left endpoint have a different signs"""
        if fMidPoint == 0:
            break
        elif fMidPoint * fa < 0:
            b = midPoint 
        else:
            a = midPoint 

        itCnt += 1  # Incrementing duration count : itCnt

    rootVal = (a + b) / 2  # Calculate the root value
    return rootVal, itCnt  # Return the root value and the iteration count

# Function to format the equation in a readable form
def makingPolynom(coefficients):
    """Creates a polynomial with the given coefficients as a string in a mathematical format."""
    termList = [] # termList, an empty list, is used to store the polynomial terms.
    for i, coeff in enumerate(coefficients[::-1]):
        if coeff == 0 and i != 0:  # Skip zero coefficients except the constant term
            continue
        elif i == 0:  
            termList.append(f"{int(coeff)}")
            if coeff > 0:
                termList.append("+")
        elif i == 1:
            if coeff < 0:
                termList.append(f"{'' if coeff == -1 else int(coeff)}x")
            else:
                termList.append(f"{'+' if coeff > 1 else ''}x")
        else:
            termList.append(f"{'' if coeff == -1 else int(coeff)}x**{i}")
    
    # Join and clean up the equation format
    result = ''.join(termList[::-1]).rstrip('+')
    return result


# Function to scan the file and return the coefficients of the polynomials
def inputCtl(fileName):
    """Initialize the coefficient values and reading the 'input'.txt file"""
    coefficient_values = {} 
    try:
        with open(fileName, "r") as file:   # Openning file only 'r' = read mode
            for line_number, line in enumerate(file, start=1):
                try:
                    key, values = line.strip().split("=")   # Splitting the line into key and values with split func.
                    coefficients = list(map(float, values.split(',')))   # Split the values into a list of coefficients
                    coefficient_values[key] = coefficients    # Add the coefficients to the coefficient values dictionary
                except (ValueError, IndexError):    # Catching errors
                    print(f"Error! Line: {line_number} in the file. Skipping the line: {line})")
    except FileNotFoundError: 
        print(f"Error: File '{fileName}' not found. Exiting...")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)} Exiting...")
    
    return coefficient_values   # Returning what we want to input.txt file (coefficent values)

def calculatingRoot(coefficients, first_a_value, first_b_value, interval_adjustment):
    """
    This loop tries to use Bisection to find the root of a polynomial and performs an 
    operation until the root is found.
    This loop passes through the polyVals dictionary.
    This dictionary contains a mapping between polynomial names and coefficients.
    For each polynomial, a root calculation is performed.
    """

    a = first_a_value
    b = first_b_value
    while True:
        try:
            root_of_equation, iteration_count = bSectionRF(coefficients, a, b) # Trying to execute bSectionRF. If it can't it will be throwing error message
            break
        except ValueError:
            a_localizer = resForX(coefficients, a)
            b_localizer = resForX(coefficients, b)
            if a_localizer * b_localizer > 0:
                a += interval_adjustment
                b += interval_adjustment
            else:
                if a_localizer == 0:
                    break
                elif b_localizer == 0:
                    a = b
                    break
                elif a_localizer * b_localizer < 0:
                    break
    return root_of_equation, iteration_count, a, b

def checkingInformation(polyVals):
    outputFormatLine = []

    for key, coefficients in polyVals.items():
        outputFormatLine.append(f"The roots of {key}:")
        
        root1, iterations1, a1, b1 = calculatingRoot(coefficients, -1, 1, -1)
        outputFormatLine.append(f"Interval: {a1:.1f}-{b1:.1f}")
        outputFormatLine.append(f"Iteration={iterations1}")
        outputFormatLine.append(f"x1={makingRoot(root1)}")
        
        root2, iterations2, a2, b2 = calculatingRoot(coefficients, 1, 2, 1)
        outputFormatLine.append(f"Interval: {a2:.1f}-{b2:.1f}")
        outputFormatLine.append(f"Iteration={iterations2}")
        outputFormatLine.append(f"x2={makingRoot(root2)}")
    return outputFormatLine

def writingOutput(polyVals, outputFormatLine):
    """
    Open the file (or create a new file).
    Write the names and coefficients of the polynomials in the file.
    The output (outputFormatLine) with roots and related information is added to the file.
    The file is closed and the writing process is completed.
    """
    with open("output.txt", "w") as output_file:
        output_file.write("Given equations:\n")
        for key, equation in polyVals.items():
            output_file.write(f"{key}= {makingPolynom(equation)}\n")

        output_file.write("\n".join(outputFormatLine))

def main():
    polyVals = inputCtl("input.txt")
    outputFormatLine = checkingInformation(polyVals)
    
    writingOutput(polyVals, outputFormatLine)


# Calling main function
if __name__ == "__main__":
    main()