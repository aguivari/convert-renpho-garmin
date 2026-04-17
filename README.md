# convert-renpho-garmin
Convert RENPHO Scales export CSV with body measurements to GARMIN FIT

## Rationale
Garmin Connect has a very strict CSV file formatting which can accept Some of the CSV exported data
from the Renpho App.

Specifically, this is the file formati it accepts:

```text
Body
Date,Weight,BMI,Fat
2026/04/06,82.4,27.5,30.4
```

However, only these 3 metrics are accepted, and with no time of measurement, only date.

This shows correctly in Garmin Connect showing the three metrics, but with a default time of 0:00 GMT
converterd to the local timezone of the user.

This python script scans the full RENPHO export with all metrics, similar to:

```text
Date, Time, Weight(kg),BMI,Body Fat(%),Skeletal Muscle(%),Fat-Free Mass(kg),Subcutaneous Fat(%),Visceral Fat,Body Water(%),Muscle Mass(kg),Bone Mass(kg),Protein (%),BMR(kcal),Metabolic Age,Optimal Weight(kg),Target to optimal weight(kg),Target to optimal fat mass(kg),Target to optimal muscle mass(kg),Body Type,Remarks
17/04/2026,10:01:59,85.90,28.7,30.5,44.7,59.70,26.9,12,50.2,56.69,3.01,15.9,1670,53,--, --, --, --, --, --
```
And generates a valid FIT file which can be imported to Garmin Connect

The code does some quick comparison of Gender (CLI parameter), body fat percentage and skeletal muscle percentage to give
a "Physique Rating" (1 to 9) as described  [here](https://tanita.eu/understanding-your-measurements/physique-rating)

the Following metrics are available to Garmin Connect after the import:
- weight
- percent_fat
-	percent_hydration
-	visceral_fat_rating
- muscle_mass
-	bone_mass
-	metabolic_age
-	bmi
-	physique_rating

A compatible field for the BMR as calculated by the RENPHO scale, so I left it out.

Garmin Connect shows a "Caloric Intake" as not available ("--"), possibly these are 
the same metric with different names.

## Calling the script

The code uses Pandas and the FIT sdk. install these two requirements with

```bash
$ pip install -r requirements.txt
(output of pip)
```

```bash
$ python convert-renpho-garmin RENPHO\ Health-Username.csv metrics.fit
FIT file written as '/Users/username/Downloads/metrics.fit'
```

The script requires 2 arguments, with a third optional:
- CSV source filename
- FIT destination filename
- Optional gender (male/female), default male

The generated file can then be imported to Garmin Connect.






