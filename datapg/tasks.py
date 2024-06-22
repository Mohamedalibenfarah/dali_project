
from celery import shared_task
import pandas as pd

@shared_task
def import_data_from_excel(file_path):
    df = pd.read_excel(file_path)
    required_columns = ['Mission', 'Client', 'Qté en u. réf.']  
    extracted_data = df[required_columns]
    output_file_path = 'extracted_data.csv'
    extracted_data.to_csv(output_file_path, index=False)
