import numpy as np
import cv2
import easyocr

def optimal_multiplier(crash_multipliers, k=1):
    average_multiplier = np.mean(crash_multipliers)
    standard_deviation = np.std(crash_multipliers)
    optimal_multiplier = average_multiplier + k * standard_deviation
    return optimal_multiplier

# Example usage:
crash_multipliers = [1.5, 2.0, 1.8, 3.0, 2.5, 1.2, 2.8]
k = 1  # Adjust this value based on your risk tolerance
print(optimal_multiplier(crash_multipliers, k))


def get_crash_multiplier(screenshot_path, lastresults_path):
    # Read the images
    screenshot = cv2.imread(screenshot_path)
    lastresults = cv2.imread(lastresults_path)

    # Convert images to grayscale
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    lastresults_gray = cv2.cvtColor(lastresults, cv2.COLOR_BGR2GRAY)

    # Apply template matching
    result = cv2.matchTemplate(screenshot_gray, lastresults_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # Get the coordinates of the top-left corner of the matched region
    top_left = max_loc
    bottom_right = (top_left[0] + lastresults.shape[1], top_left[1] + lastresults.shape[0])

    # Adjust coordinates to encompass the entire region
    top_left = (top_left[0] - 100, top_left[1] + 20)
    bottom_right = (bottom_right[0] + 100, bottom_right[1] + 300)

    # Draw a rectangle around the matched region (optional)
    cv2.rectangle(screenshot, top_left, bottom_right, (0, 255, 0), 2)

    # Extract the region of interest
    roi = screenshot[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

    # Convert the region of interest to grayscale
    roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # Perform OCR using EasyOCR
    reader = easyocr.Reader(['en'])
    results = reader.readtext(roi_gray)

    # Extract the text from the OCR results
    text = ' '.join([result[1] for result in results])

    # Display the result
    print(f"Extracted text: {text}")

    # Display the image with the rectangle (optional)
    cv2.imshow('Matched Image', screenshot)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Print the coordinates
    print(f"Top-left corner: {top_left}")
    print(f"Bottom-right corner: {bottom_right}")


# Example usage:
screenshot_path = 'ss.png'
lastresults_path = 'LASTRESULTS-detection.png'
get_crash_multiplier(screenshot_path, lastresults_path)
