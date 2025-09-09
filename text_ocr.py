#!/usr/bin/env python3
"""
Python program to generate an image with text and extract the text using OCR.

This script takes two command-line arguments:
1. A string of text to embed in the image
2. A filename for the generated image

It generates an image with a white background and black text using the Pillow library,
then runs OCR on the image using pytesseract and prints the extracted text.
"""

import sys
import os
from PIL import Image, ImageDraw, ImageFont
import pytesseract


def print_usage():
    """Print usage information."""
    print("Usage: python text_ocr.py <text> <output_filename>")
    print("Example: python text_ocr.py \"Hello from GitHub Copilot!\" test.png")


def generate_image_with_text(text, filename):
    """
    Generate an image with white background and black text.
    
    Args:
        text (str): The text to embed in the image
        filename (str): The output filename for the image
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Create image with white background
        # Size calculation: rough estimate based on text length
        width = max(400, len(text) * 15)  # Minimum width of 400px
        height = 100
        
        # Create image with white background
        image = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(image)
        
        # Try to use a default font, fallback to default if not available
        try:
            # Try to use a common system font for better text quality
            font = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf", size=24)
        except (OSError, IOError):
            try:
                # Fallback to liberation fonts
                font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", size=24)
            except (OSError, IOError):
                # Use default font as final fallback
                font = ImageFont.load_default()
        
        # Calculate text position to center it
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        # Draw text in black
        draw.text((x, y), text, fill='black', font=font)
        
        # Save the image
        image.save(filename)
        return True
        
    except Exception as e:
        print(f"Error generating image: {e}", file=sys.stderr)
        return False


def extract_text_with_ocr(filename):
    """
    Extract text from an image using OCR.
    
    Args:
        filename (str): The filename of the image to process
        
    Returns:
        str: The extracted text, or None if failed
    """
    try:
        # Check if file exists
        if not os.path.exists(filename):
            print(f"Error: Image file '{filename}' not found.", file=sys.stderr)
            return None
            
        # Open image and run OCR
        image = Image.open(filename)
        extracted_text = pytesseract.image_to_string(image).strip()
        return extracted_text
        
    except Exception as e:
        print(f"Error during OCR processing: {e}", file=sys.stderr)
        return None


def main():
    """Main function to handle command-line arguments and orchestrate the process."""
    # Check command-line arguments
    if len(sys.argv) != 3:
        print("Error: Incorrect number of arguments.", file=sys.stderr)
        print_usage()
        sys.exit(1)
    
    text_to_embed = sys.argv[1]
    output_filename = sys.argv[2]
    
    # Validate arguments
    if not text_to_embed:
        print("Error: Text cannot be empty.", file=sys.stderr)
        sys.exit(1)
    
    if not output_filename:
        print("Error: Output filename cannot be empty.", file=sys.stderr)
        sys.exit(1)
    
    # Generate image with text
    if not generate_image_with_text(text_to_embed, output_filename):
        print("Failed to generate image.", file=sys.stderr)
        sys.exit(1)
    
    print(f"Generated image: {output_filename}")
    
    # Extract text using OCR
    extracted_text = extract_text_with_ocr(output_filename)
    
    if extracted_text is None:
        print("Failed to extract text from image.", file=sys.stderr)
        sys.exit(1)
    
    # Print results
    print("Extracted Text:")
    print("----------------")
    print(extracted_text)


if __name__ == "__main__":
    main()