# #coil height width measurment
# import cv2
# import numpy as np
# from PIL import Image, ImageEnhance

# # Calibration values
# mmp_w = 0.9796  # mm per pixel (width)
# mmp_h = 0.9725  # mm per pixel (height)

# def gamma_correction(image, gamma=0.5):
#     """Apply gamma correction to enhance brightness/darkness."""
#     inv_gamma = 1.0 / gamma
#     table = np.array([(i / 255.0) ** inv_gamma * 255 for i in np.arange(256)]).astype("uint8")
#     return cv2.LUT(image, table)

# def blur_and_bilateral_filter(image):
#     blurred = cv2.GaussianBlur(image, (7, 7), 0)
#     return cv2.bilateralFilter(blurred, 7, 75, 75)

# def enhance_contrast_opencv_image(image):
#     pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
#     enhancer = ImageEnhance.Contrast(pil_image)
#     enhanced = enhancer.enhance(3.0)
#     return cv2.cvtColor(np.array(enhanced), cv2.COLOR_RGB2BGR)

# def measure_and_draw_contours(image, output_path="result.png", min_size=100, max_distance_ratio=0.2):
#     #image = cv2.imread(image_path)
#     if image is None:
#         print("Image not found.")
#         return

#     height, width = image.shape[:2]
#     image_center = (width // 2, height // 2)

#     # Preprocessing
#     blurred = blur_and_bilateral_filter(image)
#     blurred = enhance_contrast_opencv_image(blurred)
#     gamma_blurred = gamma_correction(blurred)
#     gray = cv2.cvtColor(gamma_blurred, cv2.COLOR_BGR2GRAY)
#     thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#                                    cv2.THRESH_BINARY, 21, 7)

#     cv2.imshow("Thresholded", cv2.resize(thresh, (800, 800)))
#     cv2.waitKey(0)

#     contours, _ = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
#     max_distance = max_distance_ratio * np.sqrt(width ** 2 + height ** 2)
#     valid_contours = []

#     for cnt in contours:
#         rect = cv2.minAreaRect(cnt)
#         (cx, cy), (w, h), angle = rect

#         if w < min_size or h < min_size:
#             continue
#         if abs(w - h) < 100 or h > 1000:
#             continue
#         if abs(w - h) < 20:
#             continue
#         distance = np.sqrt((cx - image_center[0]) ** 2 + (cy - image_center[1]) ** 2)
#         if distance > max_distance:
#             continue

#         valid_contours.append((cnt, rect))

#     if len(valid_contours) > 1:
#         def is_inside(inner, outer):
#             M = cv2.moments(inner)
#             if M["m00"] == 0:
#                 return False
#             cx = int(M["m10"] / M["m00"])
#             cy = int(M["m01"] / M["m00"])
#             return cv2.pointPolygonTest(outer, (cx, cy), False) >= 0

#         final_candidates = []
#         for i, (cnt1, rect1) in enumerate(valid_contours):
#             has_inside = False
#             for j, (cnt2, _) in enumerate(valid_contours):
#                 if i != j and is_inside(cnt2, cnt1):
#                     has_inside = True
#                     break
#             if not has_inside:
#                 final_candidates.append((cnt1, rect1))

#         if final_candidates:
#             valid_contours = [final_candidates[0]]
#         else:
#             valid_contours = [valid_contours[0]]

#     for cnt, rect in valid_contours:
#         (cx, cy), (w, h), angle = rect
#         box = cv2.boxPoints(rect)
#         box = np.int0(box)
#         cv2.drawContours(image, [box], 0, (0, 255, 0), 2)

#         # Identify and sort edges by length
#         edge_lengths = []
#         for i in range(4):
#             pt1 = box[i]
#             pt2 = box[(i + 1) % 4]
#             length = np.linalg.norm(pt1 - pt2)
#             edge_lengths.append((length, pt1, pt2))
#         edge_lengths = sorted(edge_lengths, key=lambda x: -x[0])  # Descending

#         # Width is the longest edge
#         width_length, w_pt1, w_pt2 = edge_lengths[0]

#         # Midpoints of the two longest (width) edges
#         long_edges = edge_lengths[:2]
#         mid1 = ((long_edges[0][1][0] + long_edges[0][2][0]) // 2, (long_edges[0][1][1] + long_edges[0][2][1]) // 2)
#         mid2 = ((long_edges[1][1][0] + long_edges[1][2][0]) // 2, (long_edges[1][1][1] + long_edges[1][2][1]) // 2)

#         # Draw width line
#         cv2.line(image, tuple(w_pt1), tuple(w_pt2), (180, 0, 255), 2)
#         mid_w = ((w_pt1[0] + w_pt2[0]) // 2, (w_pt1[1] + w_pt2[1]) // 2)
#         width_mm=int(width_length * mmp_w)
#         cv2.putText(image, f"Width_{width_mm}", mid_w, cv2.FONT_HERSHEY_SIMPLEX, 1.5, (180, 0, 255), 3)

#         # Draw height line between centers of width edges
#         cv2.line(image, mid1, mid2, (255, 0, 0), 2)
#         height_length = np.linalg.norm(np.array(mid1) - np.array(mid2))
#         mid_h = ((mid1[0] + mid2[0]) // 2, (mid1[1] + mid2[1]) // 2)
#         height_mm=int(height_length * mmp_h)
#         cv2.putText(image, f"Height_{height_mm}", mid_h, cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 3)

#     # cv2.imshow("Measured Contours", cv2.resize(image, (800, 800)))
#     # cv2.imwrite(output_path, image)
#     # cv2.waitKey(0)
#     # cv2.destroyAllWindows()
#     return image,width_mm,height_mm
# # Example usage
# #measure_and_draw_contours(r"D:\celibration_coil\left\1Image__2025-06-30__15-42-31.bmp")
# # measure_and_draw_contours(r'D:\celibration_coil\left\2Image__2025-06-30__15-43-50.bmp')




###############################more optmize version for height width and countor############################
import cv2
import numpy as np
from PIL import Image, ImageEnhance

# width=210
# height=297
# mmp_w=0.6885 #210/305
# mmp_h=0.6796 #297/437


###manual measurment
# width=337
# height=780
mmp_w=0.9796#337/344 #0.9626 #337/348
mmp_h=0.9725#780/802   #0.9798 #780/796

def gamma_correction(image, gamma=0.5):#1.5
    """Apply gamma correction to enhance brightness/darkness.
    gamma < 1.0 → Makes the image brighter
    gamma > 1.0 → Makes the image darker
    """
    inv_gamma = 1.0 / gamma
    table = np.array([(i / 255.0) ** inv_gamma * 255 for i in np.arange(256)]).astype("uint8")
    return cv2.LUT(image, table)

def blur_and_bilateral_filter(image):
    blurred = cv2.GaussianBlur(image, (7, 7), 0)
    return cv2.bilateralFilter(blurred, 7, 75, 75)

def enhance_contrast_opencv_image(image):
    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    enhancer = ImageEnhance.Contrast(pil_image)
    enhanced = enhancer.enhance(3.0)
    return cv2.cvtColor(np.array(enhanced), cv2.COLOR_RGB2BGR)

def measure_and_draw_contours(image_path, output_path="result.png", min_size=100, max_distance_ratio=0.2):
    image = cv2.imread(image_path)
    if image is None:
        print("Image not found.")
        return
    height, width = image.shape[:2]
    image_center = (width // 2, height // 2)
    
    blurred=blur_and_bilateral_filter(image)
    blurred=enhance_contrast_opencv_image(blurred)
    gamma_blurred=gamma_correction(blurred)
    gray = cv2.cvtColor(gamma_blurred, cv2.COLOR_BGR2GRAY)
    thresh=cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                 cv2.THRESH_BINARY, 21, 7)
    #gray = cv2.cvtColor(gamma_blurred, cv2.COLOR_BGR2GRAY)
    #_, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    #_, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.imshow("thr",cv2.resize(thresh,(800,800)))
    cv2.waitKey(0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    max_distance = max_distance_ratio * np.sqrt(width ** 2 + height ** 2)
    valid_contours = []

    for idx, cnt in enumerate(contours):
        rect = cv2.minAreaRect(cnt)
        (cx, cy), (w, h), angle = rect

        if w < min_size or h < min_size:
            continue
        if abs(w - h) < 100 or h > 1000:
            continue
        if abs(w - h) < 20:
            continue
        distance = np.sqrt((cx - image_center[0]) ** 2 + (cy - image_center[1]) ** 2)
        if distance > max_distance:
            continue

        valid_contours.append((cnt, rect))

    if len(valid_contours) > 1:
        def is_inside(inner, outer):
            M = cv2.moments(inner)
            if M["m00"] == 0:
                return False
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            return cv2.pointPolygonTest(outer, (cx, cy), False) >= 0

        final_candidates = []
        for i, (cnt1, rect1) in enumerate(valid_contours):
            has_inside = False
            for j, (cnt2, _) in enumerate(valid_contours):
                if i != j and is_inside(cnt2, cnt1):
                    has_inside = True
                    break
            if not has_inside:
                final_candidates.append((cnt1, rect1))

        if final_candidates:
            valid_contours = [final_candidates[0]]
        else:
            valid_contours = [valid_contours[0]]

    for cnt, rect in valid_contours:
        (cx, cy), (w, h), angle = rect
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(image, [box], 0, (0, 255, 0), 2)

        # Identify edge lengths and match width/height
        edge_lengths = []
        for i in range(4):
            pt1 = box[i]
            pt2 = box[(i + 1) % 4]
            length = np.linalg.norm(pt1 - pt2)
            edge_lengths.append((length, pt1, pt2))

        # Sort by length (longer = width, shorter = height)
        edge_lengths = sorted(edge_lengths, key=lambda x: -x[0])  # Descending

        # First is width (longer), second is height (shorter)
        width_length, w_pt1, w_pt2 = edge_lengths[0]
        height_length, h_pt1, h_pt2 = edge_lengths[2]  # use third to avoid duplicate of width

        # Draw width line
        cv2.line(image, tuple(w_pt1), tuple(w_pt2), (180, 0, 255), 2)
        mid_w = ((w_pt1[0] + w_pt2[0]) // 2, (w_pt1[1] + w_pt2[1]) // 2)
        cv2.putText(image, f"Width_{int(width_length*mmp_w)}", mid_w, cv2.FONT_HERSHEY_SIMPLEX, 1.5, (180, 0, 255), 3)

        # Draw height line
        cv2.line(image, tuple(h_pt1), tuple(h_pt2), (255, 0, 0), 2)
        mid_h = ((h_pt1[0] + h_pt2[0]) // 2, (h_pt1[1] + h_pt2[1]) // 2)
        cv2.putText(image, f"Height_{int(height_length*mmp_h)}", mid_h, cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 3)

    cv2.imshow("Filtered Contours", cv2.resize(image, (800, 800)))
    cv2.imwrite(output_path, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
#measure_and_draw_contours(r"D:\celibration_coil\left\1Image__2025-06-30__15-42-31.bmp")
#measure_and_draw_contours(r'D:\celibration_coil\left\2Image__2025-06-30__15-43-50.bmp')
#r'D:\celibration_coil\left\2Image__2025-06-30__15-43-50.bmp'







# import cv2
# import numpy as np

# def measure_and_draw_contours(image_path, output_path="result.png", min_size=100, max_distance_ratio=0.2):
#     image = cv2.imread(image_path)
#     if image is None:
#         print("Image not found.")
#         return

#     height, width = image.shape[:2]
#     image_center = (width // 2, height // 2)
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     blurred = cv2.GaussianBlur(gray, (5, 5), 0)
#     _, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
#     contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

#     max_distance = max_distance_ratio * np.sqrt(width ** 2 + height ** 2)
#     valid_contours = []

#     for idx, cnt in enumerate(contours):
#         rect = cv2.minAreaRect(cnt)
#         (cx, cy), (w, h), angle = rect

#         if w < min_size or h < min_size:
#             continue
#         if abs(w - h) < 100 or h > 1000:
#             continue
#         if abs(w - h) < 20:
#             continue
#         distance = np.sqrt((cx - image_center[0]) ** 2 + (cy - image_center[1]) ** 2)
#         if distance > max_distance:
#             continue

#         valid_contours.append((cnt, rect))

#     if len(valid_contours) > 1:
#         def is_inside(inner, outer):
#             M = cv2.moments(inner)
#             if M["m00"] == 0:
#                 return False
#             cx = int(M["m10"] / M["m00"])
#             cy = int(M["m01"] / M["m00"])
#             return cv2.pointPolygonTest(outer, (cx, cy), False) >= 0

#         final_candidates = []
#         for i, (cnt1, rect1) in enumerate(valid_contours):
#             has_inside = False
#             for j, (cnt2, _) in enumerate(valid_contours):
#                 if i != j and is_inside(cnt2, cnt1):
#                     has_inside = True
#                     break
#             if not has_inside:
#                 final_candidates.append((cnt1, rect1))

#         if final_candidates:
#             valid_contours = [final_candidates[0]]  # Keep only one
#         else:
#             valid_contours = [valid_contours[0]]  # Fallback

#     for cnt, rect in valid_contours:
#         (cx, cy), (w, h), angle = rect
#         box = cv2.boxPoints(rect)
#         box = np.int0(box)
#         cv2.drawContours(image, [box], 0, (0, 255, 0), 2)

#         # Sort box points for consistent width/height line drawing
#         box = sorted(box, key=lambda p: (p[1], p[0]))  # top-to-bottom, then left-to-right
#         p1, p2, p3, p4 = box

#         # Calculate midpoints for drawing lines
#         mid_top = ((p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2)
#         mid_bottom = ((p3[0] + p4[0]) // 2, (p3[1] + p4[1]) // 2)
#         mid_left = ((p1[0] + p4[0]) // 2, (p1[1] + p4[1]) // 2)
#         mid_right = ((p2[0] + p3[0]) // 2, (p2[1] + p3[1]) // 2)
#         ##
#         if w > h:
#             w, h = h, w
#         ##
#         # Draw height line
#         cv2.line(image, mid_top, mid_bottom, (255, 0, 0), 2)
#         cv2.putText(image, f"Height_{int(h)}", (mid_top[0] + 10, mid_top[1]), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 4)

#         # Draw width line
#         cv2.line(image, mid_left, mid_right, (0, 0, 255), 2)
#         cv2.putText(image, f"Width_{int(w)}", (mid_left[0], mid_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)

#         # Draw label with size
#         # label = f"{int(w)}x{int(h)}"
#         # cv2.putText(image, label, (int(cx), int(cy)), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 4)

#     cv2.imshow("Filtered Contours", cv2.resize(image, (800, 800)))
#     cv2.imwrite(output_path, image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

# # Example usage
# #measure_and_draw_contours(r"D:\celibration_coil\left\2Image__2025-06-30__15-43-50.bmp")
# measure_and_draw_contours(r"D:\celibration_coil\left\1Image__2025-06-30__15-42-31.bmp")


########################### minAreaRect ###############################
import cv2
import numpy as np

def measure_and_draw_contours(image_path, output_path="result.png", min_size=100, max_distance_ratio=0.2):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print("Image not found.")
        return

    height, width = image.shape[:2]
    image_center = (width // 2, height // 2)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply thresholding
    _, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Find contours (both internal and external)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)# cv2.RETR_EXTERNAL
    max_distance = max_distance_ratio * np.sqrt(width**2 + height**2)
    print("max_distance : ",max_distance)

    for cnt in contours:
        # Get minimum area rotated rectangle
        rect = cv2.minAreaRect(cnt)
        (cx, cy), (w, h), angle = rect
        #Filter out very small or degenerate contours
        if w < min_size or h < min_size:
            continue
        print(" height and width : ",rect[1])
        if abs(w - h)<100 or h>1000:
            continue

        # Ignore square-like contours (optional)
        if abs(w - h) < 20:  # allow small tolerance
            continue
        # Compute distance to image center
        distance = np.sqrt((cx - image_center[0])**2 + (cy - image_center[1])**2)
        print("distance : ",distance)
        if distance > max_distance:
            continue

        # Draw the rotated rectangle
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        color = (0, 255, 0)
        cv2.drawContours(image, [box], 0, color, 2)

        # Label with size
        label = f"{int(w)}x{int(h)}"
        cv2.putText(image, label, (int(cx), int(cy)), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)

    # Show and save result
    cv2.imshow("Filtered External Contours", cv2.resize(image, (640, 640)))
    cv2.imwrite(output_path, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
#measure_and_draw_contours(r"D:\celibration_coil\left\1Image__2025-06-30__15-42-31.bmp")
#measure_and_draw_contours(r"D:\celibration_coil\left\2Image__2025-06-30__15-43-50.bmp")



########################### boundingRect ###############################

import cv2
import numpy as np

def measure_and_draw_contours(image_path, output_path="result.png", min_size=100, max_distance_ratio=0.2):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print("Image not found.")
        return

    height, width = image.shape[:2]
    image_center = (width // 2, height // 2)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply thresholding
    _, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Find contours (both internal and external)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    if hierarchy is None:
        print("No contours found.")
        return

    max_distance = max_distance_ratio * np.sqrt(width**2 + height**2)

    for i, cnt in enumerate(contours):
        x, y, w, h = cv2.boundingRect(cnt)

        # Filter out small contours
        if w < min_size or h < min_size or (w==h):
            continue

        # Compute centroid of the contour
        M = cv2.moments(cnt)
        if M["m00"] == 0:
            continue
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])

        # Compute distance to image center
        distance = np.sqrt((cx - image_center[0])**2 + (cy - image_center[1])**2)
        if distance > max_distance:
            continue  # Skip contours too far from center

        # Choose color based on hierarchy
        if hierarchy[0][i][3] == -1:
            color = (0, 255, 0)  # External - Green
        else:
            color = (0, 0, 255)  # Internal - Red
            continue
        # Draw contour
        cv2.drawContours(image, [cnt], -1, color, 2)
        cv2.rectangle(image, (x, y), (x + w, y + h), color, 1)
        label = f"{w}x{h}"
        cv2.putText(image, label, (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 3)

    # Show and save result
    cv2.imshow("Filtered Contours", cv2.resize(image,(640,640)))
    cv2.imwrite(output_path, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


#measure_and_draw_contours(r"D:\celibration_coil\left\2Image__2025-06-30__15-43-50.bmp")
