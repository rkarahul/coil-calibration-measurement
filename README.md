# Coil Calibration & Measurement

This project measures **coil dimensions (height and width)** from images using OpenCV.  
It uses calibration (mm per pixel) to convert pixel distances into real-world millimeter values.

---

## Features
- Preprocessing: Gaussian blur, bilateral filter, gamma correction, contrast enhancement
- Contour detection and filtering
- Coil bounding box extraction
- Pixel → millimeter conversion using calibration values
- Annotated output image with measured height & width

---

## Calibration
You must calibrate once using a known reference (e.g., A4 sheet or 15 cm scale).  
Calculate:

```
mmp_w = real_width_mm / measured_width_px  
mmp_h = real_height_mm / measured_height_px
```

Then update these values in the script.

---

## Usage
```bash
python coil_measure.py
```

Example in code:
```python
measure_and_draw_contours("left/1Image__2025-06-30__15-42-31.bmp")
measure_and_draw_contours("left/2Image__2025-06-30__15-43-50.bmp")
```

---

## Output
- Annotated image with width & height in millimeters  
- Printed measurement values

### Example Result
<img width="2448" height="2048" alt="rahul" src="https://github.com/user-attachments/assets/2703ffe1-f85b-428a-8c77-457d8954a1db" />
<img width="2448" height="2048" alt="result" src="https://github.com/user-attachments/assets/be124a01-894a-4867-97db-a2ea0090e551" />



---

## Requirements
- Python 3.8+
- OpenCV
- Pillow
- NumPy
