#!/usr/bin/env python3
"""
Text to Image with OCR Extraction

This script generates an image with user-specified text and then extracts
the text using OCR (Optical Character Recognition).

Usage:
    python text_ocr.py <text> <filename>

Example:
    python text_ocr.py "Hello from GitHub Copilot!" test.png
"""

import sys
import os
from PIL import Image, ImageDraw, ImageFont
import pytesseract


def generate_image_with_text(text, filename):
    """
    Generate an image with specified text on a white background.
    
    Args:
        text (str): The text to embed in the image
        filename (str): The filename for the generated image
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Image dimensions and settings
        width = 800
        height = 200
        background_color = 'white'
        text_color = 'black'
        
        # Create a new image with white background
        image = Image.new('RGB', (width, height), background_color)
        draw = ImageDraw.Draw(image)
        
        # Try to use a larger font if available, fallback to default
        try:
            font_size = 36
            font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', font_size)
        except (OSError, IOError):
            # Fallback to default font if specific font not found
            try:
                font = ImageFont.load_default()
            except Exception:
                font = None
        
        # Calculate text position to center it
        if font:
            # Get text bounding box
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        else:
            # Rough estimation for default font
            text_width = len(text) * 10
            text_height = 20
        
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        # Draw the text on the image
        draw.text((x, y), text, fill=text_color, font=font)
        
        # Save the image
        image.save(filename)
        return True
        
    except Exception as e:
        print(f"Error generating image: {e}", file=sys.stderr)
        return False


def extract_text_from_image(filename):
    """
    Extract text from an image using OCR.
    
    Args:
        filename (str): The filename of the image to process
        
    Returns:
        str: Extracted text, or None if extraction failed
    """
    try:
        # Check if file exists
        if not os.path.isfile(filename):
            print(f"Error: Image file '{filename}' not found", file=sys.stderr)
            return None
            
        # Open the image and extract text using pytesseract
        image = Image.open(filename)
        extracted_text = pytesseract.image_to_string(image)
        
        # Clean up the extracted text (remove extra whitespace)
        extracted_text = extracted_text.strip()
        
        return extracted_text
        
    except Exception as e:
        print(f"Error extracting text from image: {e}", file=sys.stderr)
        return None


def main():
    """Main function to handle command-line arguments and execute the workflow."""
    
    # Check for correct number of arguments
    if len(sys.argv) != 3:
        print("Error: Missing arguments", file=sys.stderr)
        print("Usage: python text_ocr.py <text> <filename>", file=sys.stderr)
        print("Example: python text_ocr.py \"Hello from GitHub Copilot!\" test.png", file=sys.stderr)
        sys.exit(1)
    
    text_to_embed = sys.argv[1]
    image_filename = sys.argv[2]
    
    # Validate arguments
    if not text_to_embed.strip():
        print("Error: Text cannot be empty", file=sys.stderr)
        sys.exit(1)
    
    if not image_filename.strip():
        print("Error: Filename cannot be empty", file=sys.stderr)
        sys.exit(1)
    
    # Generate the image with text
    print(f"Generating image with text: '{text_to_embed}'")
    if not generate_image_with_text(text_to_embed, image_filename):
        print("Error: Failed to generate image", file=sys.stderr)
        sys.exit(1)
    
    print(f"Generated image: {image_filename}")
    
    # Extract text from the generated image using OCR
    print("Extracting text using OCR...")
    extracted_text = extract_text_from_image(image_filename)
    
    if extracted_text is None:
        print("Error: Failed to extract text from image", file=sys.stderr)
        sys.exit(1)
    
    # Display the results
    print("Extracted Text:")
    print("----------------")
    print(extracted_text)


if __name__ == "__main__":
    main()