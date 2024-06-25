import ast
import os

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


SYSTEM_PROMPT_TEMPLATE = """
You are a helpful data clean up assistant. You job is to help users to identify where to clean up within the medical data.

You are going to receive medical data for a patient as user input, the data will have the following format:
[{{'text': xxxxx, 'page': 1}}, {{'text': xxxxx, 'page': 2}}, ...]

Those data include patients visit (treatment) records, each of record is consisted of multiple pages. 
Record can be a Office vist record or examination report record. 
Look for 'Progress Note', Office visit as a sign of a new office visit record.
Look for Medical Examination term like MRI, CT, X-ray as a sign of a new report record.

Note:
The first date that's mentioned in every page is just a print date for fax, you can ignore it.

Your task is to clean up identify the page and content to clean up following the rules below:
1. There are sometimes duplicated information within different records or same record, 
you need to identify the content and page. for example personal information like name, address, phone number.
2. The order of record might not be the correct order, so I need you to reorder the records based on the visit date (latest come first).
Look for Office Visit (office record) or Date (report record) for reference of the visit date. But remember, one record might have multiple pages, and you have to reorder them as a group.
for example if page 4,5,6 is for a record happened after page 2,3. then I want you to reorder them to 4,5,6,2,3

Note:
The first page should always be the first page which is fax cover
When mark down the duplicated content, you should not mark down every occurrence, but leave the first occurrence and mark down the rest.

After you identify all the pages and content to clean up, you should return the list of the pages and content in the following json format without any explanation:
{{
    "pages_order": [new order of pages],
    "duplicated_content": [
        {{"page": page number, "content": content to clean up}},
    ]
}}
"""

class DataCleanup:
    def __init__(self, config=None):
        if config is None:
            config = {}
        api_key = os.environ.get("OPENAI_API_KEY")
        self.llm = ChatOpenAI(
            api_key=api_key,
            model="gpt-4-turbo",
            temperature=0,
            **config
        )

    def cleanup_data(self, data):
        prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT_TEMPLATE),
            ("user", "{input}")
        ])

        output_parser = StrOutputParser()
        chain = prompt | self.llm | output_parser

        response = chain.invoke({"input": data})

        try:
            clean_up_reference = ast.literal_eval(response)
            # deduplicate the content
            for i in clean_up_reference.get('duplicated_content'):
                page = i.get('page')
                for raw_data in data:
                    if page == raw_data.get('page'):
                        raw_data['text'] = raw_data.get('text').replace(i.get('content'), '')
            cleaned_up_data = []
            # reorder the pages
            for i in clean_up_reference.get('pages_order'):
                for raw_data in data:
                    if i == raw_data.get('page'):
                        cleaned_up_data.append(raw_data)
        except Exception as e:
            raise e

        return cleaned_up_data
