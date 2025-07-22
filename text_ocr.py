#!/usr/bin/env python3
"""
Python program to generate an image with text and extract the text using OCR.
"""

import sys
import os
from PIL import Image, ImageDraw, ImageFont
import pytesseract


def generate_image_with_text(text, filename, width=800, height=200, font_size=36):
    """
    Generate an image with the specified text on a white background.
    
    Args:
        text (str): The text to embed in the image
        filename (str): The filename for the generated image
        width (int): Width of the image in pixels
        height (int): Height of the image in pixels
        font_size (int): Size of the font
        
    Raises:
        IOError: If there's an issue creating or saving the image
    """
    try:
        # Create a new image with white background
        image = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(image)
        
        # Try to use a default font, fallback to basic font if not available
        try:
            font = ImageFont.truetype("DejaVuSans.ttf", font_size)
        except (IOError, OSError):
            try:
                # Try another common font
                font = ImageFont.truetype("arial.ttf", font_size)
            except (IOError, OSError):
                # Fallback to default font
                font = ImageFont.load_default()
        
        # Calculate text position to center it
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        # Draw the text on the image
        draw.text((x, y), text, fill='black', font=font)
        
        # Save the image
        image.save(filename)
        print(f"Generated image: {filename}")
        
    except Exception as e:
        raise IOError(f"Failed to generate image: {e}")


def extract_text_from_image(filename):
    """
    Extract text from the image using OCR.
    
    Args:
        filename (str): The filename of the image to process
        
    Returns:
        str: The extracted text
        
    Raises:
        IOError: If there's an issue reading the image
        RuntimeError: If OCR processing fails
    """
    try:
        # Check if file exists
        if not os.path.exists(filename):
            raise IOError(f"Image file not found: {filename}")
        
        # Open and process the image
        image = Image.open(filename)
        
        # Extract text using pytesseract
        extracted_text = pytesseract.image_to_string(image).strip()
        
        return extracted_text
        
    except IOError as e:
        raise IOError(f"Failed to read image file: {e}")
    except Exception as e:
        raise RuntimeError(f"OCR processing failed: {e}")


def main():
    """
    Main function to handle command line arguments and coordinate the operations.
    """
    # Check command line arguments
    if len(sys.argv) != 3:
        print("Usage: python text_ocr.py <text> <filename>", file=sys.stderr)
        print("Example: python text_ocr.py \"Hello from Claude Code!\" test.png", file=sys.stderr)
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
    
    try:
        # Generate image with text
        generate_image_with_text(text_to_embed, image_filename)
        
        # Extract text using OCR
        extracted_text = extract_text_from_image(image_filename)
        
        # Display results
        print("Extracted Text:")
        print("-" * 16)
        print(extracted_text if extracted_text else "(No text detected)")
        
    except IOError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()