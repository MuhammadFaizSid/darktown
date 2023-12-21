from PIL import Image, ImageFilter, ImageDraw, ImageFont
import datetime
from datetime import datetime

im = Image.new('RGB', (600, 400), ("#0c0d15"))

draw = ImageDraw.Draw(im)
draw.rectangle((20, 20, 580, 380), fill=("#0c0d15"), outline=("#00e5ff"),  width=3)
draw.rectangle((30, 30, 570, 370), fill=("#0c0d15"), outline=("#00e5ff"), width=3)
head_font = ImageFont.truetype("Fonts//Algerian Regular.ttf", 42)
draw.text((300, 83), "DARK TOWN", ("#ffffff"), font=head_font, anchor="ms")
draw.line((390, 313, 540, 313), fill="#ffffff", width=2)

global_font_semi_bold =  ImageFont.truetype("Fonts//MavenPro-SemiBold.ttf", 20)
global_font_medium = ImageFont.truetype("Fonts//MavenPro-Medium.ttf", 20)
global_font_comfortaa =  ImageFont.truetype("Fonts//Comfortaa-Medium.ttf", 18)

draw.text((75, 135), "Full Name:", ("#ffffff"), font=global_font_semi_bold, anchor="ls")
draw.text((215, 135), "Faiz Siddiqui", ("#ffffff"), font=global_font_medium, anchor="ls")
draw.line((215, 138, 430, 138), fill="#ffffff", width=2)

draw.text((75, 180), "Amount:", ("#ffffff"), font=global_font_semi_bold, anchor="ls")
draw.text((215, 180), "125500", ("#ffffff"), font=global_font_medium, anchor="ls")
draw.line((215, 183, 430, 183), fill="#ffffff", width=2)

draw.text((75, 230), "Booking Unit:", ("#ffffff"), font=global_font_semi_bold, anchor="ls")
draw.text((215, 230), "DHA", ("#ffffff"), font=global_font_medium, anchor="ls")
draw.line((215, 233, 430, 233), fill="#ffffff", width=2)

draw.text((75, 280), "CNIC No:", ("#ffffff"), font=global_font_semi_bold, anchor="ls")
draw.text((215, 280), "29383928529548", ("#ffffff"), font=global_font_medium, anchor="ls")
draw.line((215, 283, 430, 283), fill="#ffffff", width=2)

date_font =  ImageFont.truetype("Fonts//Comfortaa-Medium.ttf", 15)

draw.text((45, 355), "Date:", ("#ffffff"), font=date_font, anchor="ls")
draw.text((92, 355), "Fri Feb 13 20:21:12 2021", ("#ffffff"), font=date_font, anchor="ls")

draw.text((465, 335), "Admin", ("#ffffff"), font=global_font_comfortaa, anchor="ms")
draw.text((465, 360), "9380948998983333", ("#ffffff"),font=global_font_comfortaa, anchor="ms")

receipt_name = f"Receipt issued at {datetime.today().strftime('%Y-%m-%d-%H:%M')}"
im.save(f'C:\\Users\\Muhammad Faiz\\Desktop\\{receipt_name}.png')

img = Image.open(f'C:\\Users\\Muhammad Faiz\\Desktop\\{receipt_name}.png')
img.show()
