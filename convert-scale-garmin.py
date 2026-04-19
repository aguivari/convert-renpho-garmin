import pandas as pd
from datetime import datetime, timezone
import os.path
import sys
from garmin_fit_sdk import Encoder, Profile

print(len(sys.argv), sys.argv)

if len(sys.argv) < 4: 
    print("Error: three arguments are expected, with an optional fourth (default male)")
    print("Usage: ", sys.argv[0], "<brand> <input_file.csv> <output_file.fit> [male/female]")
    print("<brand> can be eufy or renpho")
    sys.exit(1)

if len(sys.argv) == 5: # gender espeficied
    print("gender specified on command line: ",end='') 
    if sys.argv[4] == 'male':
        gender='male'
    else:
        gender='female'
    print(gender)
else:
    gender='male'
    print("no gender specified on command line, assuming male") 
    
input_file = sys.argv[2]
output_file = sys.argv[3]
brand=sys.argv[1]

# import support function for correct brand
if brand == "renpho":
    from brands.renpho import process_row
elif brand == "eufy":
    from brands.eufy import process_row
else:
    print(f"Unknown brand {brand}")
    exit(1)

if not os.path.isfile(input_file):
    print(f"Error: file {input_file} not found!")
    exit(1)
    
if os.path.isfile(output_file):
    print(f"file {output_file} exists and will be overwritten!")

# Load data
df = pd.read_csv(input_file, skipinitialspace=True)
df.columns = [c.strip() for c in df.columns]

# Initialize FIT Encoder
encoder = Encoder()
# FIT File header info
encoder.write_mesg({
    'mesg_num': Profile['mesg_num']['FILE_ID'],
    'type': 'weight',
    'manufacturer': 'development',
    'product': 1,
    'serial_number': 12345678,
    'time_created': datetime.now(timezone.utc)
})

# Process CSV lines
for _, row in df.iterrows():
    try:
        data=process_row(row,gender)
        encoder.write_mesg({
            'mesg_num': Profile['mesg_num']['WEIGHT_SCALE'],
            'timestamp': data['timestamp'],
            'weight': data['weight'],
            'percent_fat': data['percent_fat'],
            'percent_hydration': data['percent_hydration'],
            'visceral_fat_rating': data['visceral_fat_rating'],
            'muscle_mass': data['muscle_mass'],
            'bone_mass': data['bone_mass'],
            'metabolic_age': data['metabolic_age'],
            'bmi': data['bmi'],
            'physique_rating': data['physique_rating'],
        })
        
    except Exception as e:
        print(f"Error processing line: {e}")

# Close encoder and save file
uint8_array = encoder.close()
with open(output_file, 'wb') as f:
    f.write(uint8_array)

print(f"FIT file written as '{output_file}'")
