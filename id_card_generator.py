import pandas as pd
import qrcode
from PIL import Image, ImageDraw, ImageFont
import os

def generate_id_cards(csv_file, template_file):
    # Read CSV file
    df = pd.read_csv(csv_file)
    
    # Load template image
    template = Image.open(template_file)
    
    # Create output directory if it doesn't exist
    if not os.path.exists('output'):
        os.makedirs('output')
    
    try:
        # Increased font size to 160 (5x of 32)
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 160)
    except OSError:
        # Fallback to default font if DejaVu Sans is not available
        font = ImageFont.load_default()
        print("Warning: Using default font as DejaVu Sans was not found")
    
    total_rows = len(df)
    print(f"Starting to generate {total_rows} ID cards...")
    
    # Process each row in CSV
    for index, row in df.iterrows():
        print(f"Processing card {index + 1} of {total_rows} for {row['Guest Name']}")
        
        # Create a copy of template
        card = template.copy()
        draw = ImageDraw.Draw(card)
        
        # Adjusted text positions for larger font
        draw.text((600, 1200), f"Name: {row['Guest Name']}", fill="black", font=font)
        draw.text((600, 1600), f"Centre: {row['Centre']}", fill="black", font=font)
        
        # Generate QR code with larger size and custom background color
        qr = qrcode.QRCode(version=1, box_size=50, border=5)
        qr.add_data(row['QR Code Data'])
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="#cde7f6")
        
        # Resize QR code to 1500x1500 (5x of 300)
        qr_image = qr_image.resize((2000, 2000))
        
        # You can adjust these x,y coordinates to position the QR code
        qr_x = template.width - 2300  # Decrease to move left, increase to move right
        qr_y = 800                    # Decrease to move up, increase to move down
        card.paste(qr_image, (qr_x, qr_y))
        
        # Save the card
        output_file = f"output/id_card_{index}.png"
        card.save(output_file)
        
        print(f"Successfully saved ID card for {row['Guest Name']}")
    
    print("All ID cards generated successfully!")

if __name__ == "__main__":
    generate_id_cards("data.csv", "ID Card Blank_pages-to-jpg-0001.jpg")
