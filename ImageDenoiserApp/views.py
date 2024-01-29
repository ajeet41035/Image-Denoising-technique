from django.shortcuts import render, redirect
from .models import ImageModel
import cv2
import numpy as np
from PIL import Image
import io
import base64

image_i = 0

def upload_image(request):
    if request.method == "POST":
        if "image" in request.FILES:
            image = request.FILES["image"]

            # Read the image data from the request
            image_data = image.read()

            # Encode the binary image data as a base64-encoded string
            image_data_base64 = base64.b64encode(image_data).decode("utf-8")

            # Store the base64-encoded image data in the session
            request.session["uploaded_image_id"] = image_data_base64

        return render(request, "applyFilter.html")
    return render(request, "upload.html")



def apply_mean_filter(request):
    if "uploaded_image_id" in request.session:
        # Retrieve the uploaded image data from the session
        image_data_base64 = request.session["uploaded_image_id"]

        # Decode the base64-encoded image data to bytes
        uploaded_image_data = base64.b64decode(image_data_base64.encode("utf-8"))

        # Read and convert the image data to a NumPy array
        img_np = np.array(Image.open(io.BytesIO(uploaded_image_data)))

        # Ensure the image is in RGB mode
        img_rgb = Image.fromarray(img_np).convert("RGB")

        # Apply mean filtering
        kernel_size = 7  # You can adjust the kernel size as needed
        filtered_img = cv2.blur(np.array(img_rgb), (kernel_size, kernel_size))

        # Convert the filtered NumPy array back to an image
        filtered_image = Image.fromarray(filtered_img)

        # Save the filtered image to a BytesIO buffer
        filtered_buffer = io.BytesIO()
        filtered_image.save(
            filtered_buffer, format="JPEG"
        )  # You can change the format to PNG if needed
        filtered_image_data = filtered_buffer.getvalue()

        # Convert bytes to a serializable format (e.g., base64 encode)
        filtered_image_data_base64 = base64.b64encode(filtered_image_data).decode(
            "utf-8"
        )
        return render(
            request,
            "meanFilter.html",
            {"mean_filtered_image_data": filtered_image_data_base64},
        )
    return render(request, "applyFilter.html")


def apply_median_filter(request):
    if "uploaded_image_id" in request.session:
        # Retrieve the uploaded image data from the session
        image_data_base64 = request.session["uploaded_image_id"]

        # Decode the base64-encoded image data to bytes
        uploaded_image_data = base64.b64decode(image_data_base64.encode("utf-8"))

        # Read and convert the image data to a NumPy array
        img_np = np.array(Image.open(io.BytesIO(uploaded_image_data)))

        # Ensure the image is in RGB mode
        img_rgb = Image.fromarray(img_np).convert("RGB")

        # Apply median filtering
        kernel_size = 1  # You can adjust the kernel size as needed
        filtered_img = cv2.medianBlur(np.array(img_rgb), kernel_size)

        # Convert the filtered NumPy array back to an image
        filtered_image = Image.fromarray(filtered_img)

        # Save the filtered image to a BytesIO buffer
        filtered_buffer = io.BytesIO()
        filtered_image.save(
            filtered_buffer, format="JPEG"
        )  # You can change the format to PNG if needed
        filtered_image_data = filtered_buffer.getvalue()

        # Convert bytes to a serializable format (e.g., base64 encode)
        filtered_image_data_base64 = base64.b64encode(filtered_image_data).decode(
            "utf-8"
        )
        return render(
            request,
            "medianFilter.html",
            {"median_filtered_image_data": filtered_image_data_base64},
        )

    return render(request, "applyFilter.html")


def apply_gaussian_filter(request):
    if "uploaded_image_id" in request.session:
        # Retrieve the uploaded image data from the session
        image_data_base64 = request.session["uploaded_image_id"]

        # Decode the base64-encoded image data to bytes
        uploaded_image_data = base64.b64decode(image_data_base64.encode("utf-8"))

        # Read and convert the image data to a NumPy array
        img_np = np.array(Image.open(io.BytesIO(uploaded_image_data)))

        # Ensure the image is in RGB mode
        img_rgb = Image.fromarray(img_np).convert("RGB")

        # Apply Gaussian filtering
        kernel_size = (7, 7)  # You can adjust the kernel size as needed
        sigma = 0  # You can adjust the sigma value as needed
        filtered_img = cv2.GaussianBlur(np.array(img_rgb), kernel_size, sigma)

        # Convert the filtered NumPy array back to an image
        filtered_image = Image.fromarray(filtered_img)

        # Save the filtered image to a BytesIO buffer
        filtered_buffer = io.BytesIO()
        filtered_image.save(
            filtered_buffer, format="JPEG"
        )  # You can change the format to PNG if needed
        filtered_image_data = filtered_buffer.getvalue()

        # Convert bytes to a serializable format (e.g., base64 encode)
        filtered_image_data_base64 = base64.b64encode(filtered_image_data).decode(
            "utf-8"
        )
        return render(
            request,
            "gaussianFilter.html",
            {"gaussian_filtered_image_data": filtered_image_data_base64},
        )
    return render(request, "applyFilter.html")
