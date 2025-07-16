#!/usr/bin/env python3
"""
Python script to generate an image with text and extract the text using OCR.
"""

import sys
import os
from PIL import Image, ImageDraw, ImageFont
import pytesseract


def generate_image_with_text(text, filename):
    """
    Generate an image with the specified text on a white background.
    
    Args:
        text (str): The text to embed in the image
        filename (str): The filename for the generated image
        
    Returns:
        PIL.Image: The generated image object
        
    Raises:
        Exception: If image generation fails
    """
    try:
        # Create a white background image
        width, height = 800, 200
        image = Image.new('RGB', (width, height), color='white')
        
        # Get drawing context
        draw = ImageDraw.Draw(image)
        
        # Try to use a default font, fall back to built-in if not available
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
        except (OSError, IOError):
            try:
                font = ImageFont.load_default()
            except Exception:
                font = None
        
        # Calculate text position to center it
        if font:
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        else:
            # Fallback estimation for default font
            text_width = len(text) * 10
            text_height = 20
        
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        # Draw the text in black
        draw.text((x, y), text, fill='black', font=font)
        
        # Save the image
        image.save(filename)
        
        return image
        
    except Exception as e:
        raise Exception(f"Image generation failed: {str(e)}")


def extract_text_from_image(image_path):
    """
    Extract text from an image using OCR.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        str: The extracted text
        
    Raises:
        Exception: If OCR processing fails
    """
    try:
        # Open the image
        image = Image.open(image_path)
        
        # Use pytesseract to extract text
        extracted_text = pytesseract.image_to_string(image).strip()
        
        return extracted_text
        
    except Exception as e:
        raise Exception(f"OCR processing failed: {str(e)}")


def main():
    """
    Main function to handle command-line arguments and orchestrate the process.
    """
    # Check command-line arguments
    if len(sys.argv) != 3:
        print("Error: Missing arguments", file=sys.stderr)
        print("Usage: python text_ocr.py <text> <filename>", file=sys.stderr)
        print("Example: python text_ocr.py \"Hello from Claude Code!\" test.png", file=sys.stderr)
        sys.exit(1)
    
    text = sys.argv[1]
    filename = sys.argv[2]
    
    # Validate arguments
    if not text.strip():
        print("Error: Text argument cannot be empty", file=sys.stderr)
        sys.exit(1)
    
    if not filename.strip():
        print("Error: Filename argument cannot be empty", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Generate image with text
        image = generate_image_with_text(text, filename)
        print(f"Generated image: {filename}")
        
        # Extract text from the generated image
        extracted_text = extract_text_from_image(filename)
        
        # Print the extracted text
        print("Extracted Text:")
        print("----------------")
        print(extracted_text)
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()