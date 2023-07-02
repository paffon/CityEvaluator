# City Evaluator
Omri Niri, v1.0

---

## Run
1. Adjust your preferences in CityEvaluator/config/director.json: copy the value from *costs* or *remaining* into *what to calculate*
2. Adjust your salary and the upper/lower bounds on your shopping habits.
3. Run this:
```
python CityEvaluator/modules/main.py
```

## Add a new city
1. Open CityEvaluator/data
2. Add a folder for the country. In it, add a folder called "cities" (if doesn't exist already)
3. In that folder place txt files for each city you want to add.
4. The data in the txt file for each city should be copied directly from *numbeo.com*. for example, here is the data page for [Malaga, ES](https://www.numbeo.com/cost-of-living/in/Malaga).
5. Copy everything from the "restaurant icon" until the end of the categorical data.
6. Pasta directly into the txt file for the city.
7. Open CityEvaluator/data/countries_income_tax_data.json
8. Make sure that the country is included here, and that the city is included in the country's cities list.

## Add a new country

1. Open CityEvaluator/data/countries_income_tax_data.json
2. Add a key for the new country.
3. Add all necessary detail, especially the tax brackets.

Tax brackets example for [Latvia](https://taxsummaries.pwc.com/latvia/individual/taxes-on-personal-income):

"Personal income tax rates
Latvia has a progressive PIT system. Unless the law provides for a different rate, the progressive rate is based on the level of annual income as follows:

A rate of 20% applies to income up to EUR 20,004.
Any portion of income between EUR 20,004 and EUR 78,100 attracts a rate of 23%.
Any income over EUR 78,100 attracts a rate of 31%."

Becomes:
```
"Latvia": {
	  "country_code": "LV",
	  "tax brackets": {
		  "amount brackets":     [0, 20004, 78100],
		  "percentage brackets": [0.2, 0.23, 0.31]
		},
		"cities": ["Riga"]
    }
```