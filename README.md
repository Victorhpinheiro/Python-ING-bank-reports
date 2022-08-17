# Python ING bank study

This project intend to create a small database with the everyday accounts of ING and run SQL queries to analyse it and tools to vizualize it.

# How to use it:

## With mock up data
- Run create a csv file using "create_csv_test.py" (you welcome to play with the config at the top of the file)
- certify that in the Source folder have a folder call input with the file conta.csv
- Run the main
- Check for erros in the console or the final report on the "Reports" folder

## Real Data
- Go to the ING everyday account that you want the reports and download the information in csv format
- Change the name to "conta.csv" and add inside a folder "Input" in the same directory as the source
- Run the main
- Check for erros in the console or the final report on the "Reports" folder

# Make your own categories!
Change the file "categories.py" list, regex and if function and match and do your own filter about your expenses :)

## Goals

Import ING bank files in CSV format

Create a SQLite database with the information and category

Do analyses of of the information

Vizualization

## Notes

Anyone is welcome to use it and adapt the categories_mapping.py files and play with the results and queries.

## Notes 2

I know I could use pandas for this. I am very familiar with it and already do those analyses using it :)

I want to practice my SQL best practices and interaction with database.
