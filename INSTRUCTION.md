# DataCleanUp

This project help to clean up by remove duplication in the data and reorder the order based on record date

It firstly extract the data from the pdf file use DocumentAI 

Preprocess the data to {"page":x, "text":x} structure 

Then use the OpenAI API to create a reference for the data

Then use the reference to clean up the data

Then reorder the data based on the record date

Then save the data to a json file

### setup
pip install -r requirements.txt
set up the environment variable, use the .env.example file as a template
You will need GCP set up and OpenAI set up



### Run the script
python submission.py --path-to-case-pdf ./data/inpatient_record.pdf

it will create a cleaned_data.txt which contains a cleaned up data.
