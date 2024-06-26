import pandas as pd
from .models import Mydata
from django.http import JsonResponse
from django.forms.models import model_to_dict
from .forms import DateRangeForm
from .forms import fetchForm
from django.db.models import Sum
from django.shortcuts import render
from .forms import UploadFileForm
from datetime import datetime, timedelta, date

import numpy as np

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            df = pd.read_excel(request.FILES['file'])
            for index, row in df.iterrows():
                try:
                    # Check for NaN values and replace them with None
                    row = {k: v if pd.notnull(v) else None for k, v in row.items()}

                    # Check if similar entry already exists in the database
                    existing_entry = Mydata.objects.filter(
                        Assistant=row['Assistant'],
                        TMission=row['Mission'],
                        CMission=row['Code de la mission'],
                        Raison_sociale=row['Raison sociale'],
                        Description=row['Descriptif général mission'],
                        Client=row['Client'],
                        Manager=row['Manager mission'],
                        Date=row['Date'],
                        Libellé=row['Libellé'],
                        Nbre_heures=row['Qté en u. réf.']
                    ).exists()

                    # If similar entry does not exist, create a new one
                    if not existing_entry:
                        Mydata.objects.create(**row)
                except Exception as e:
                    print(f"Error creating Mydata entry: {e}")
            if 'json' in request.GET:
                return JsonResponse({'message': 'Data uploaded successfully'})
            else:
                return render(request, 'upload_success.html')
    else:
        form = UploadFileForm()
    return render(request, 'upload_form.html', {'form': form})


def fetch_data(request):
    form = fetchForm(request.GET)
    if form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        try:
            data = Mydata.objects.filter(Date__range=[start_date, end_date])
            data_json = []
            for entry in data:
                entry_dict = model_to_dict(entry)
                # Handle NaN values in the 'Manager' field
                if isinstance(entry_dict['Manager'], float) and np.isnan(entry_dict['Manager']):
                    entry_dict['Manager'] = None  # Convert NaN to None
                data_json.append(entry_dict)
            return JsonResponse({'data': data_json})
        except Exception as e:
            print(f"Error fetching data: {e}")
            return JsonResponse({'error': 'Failed to load data'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid form data'}, status=400)


    
def calculate_total_hours(start_date, end_date, hours_per_day, num_holidays):
    total_hours = 0

    # Calculate the number of working days between start_date and end_date
    current_date = start_date
    while current_date <= end_date:
        # Check if the current day is a weekday (Monday=0, Sunday=6)
        if current_date.weekday() < 5:  
            total_hours += hours_per_day

        current_date += timedelta(days=1)

    # Subtract the number of holidays from the total hours
    total_hours -= num_holidays * hours_per_day

    return total_hours



def ttl_heures(request):
    form = DateRangeForm(request.GET)
    if form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        data = Mydata.objects.filter(Date__range=[start_date, end_date])
        total_hours = data.values('Assistant').annotate(total_hours=Sum('Nbre_heures'))
        if 'json' in request.GET:
            try:
                total_hours_json = [model_to_dict(entry) for entry in total_hours]
                return JsonResponse({'data': total_hours_json})
            except Exception as e:
                return JsonResponse({'error': 'Failed to parse data'}, status=500)
    else:
        data = Mydata.objects.none()  # Return no data if form is not valid
        total_hours = []

    return render(request, 'ttl_heures.html', {'form': form, 'data': data, 'total_hours': total_hours})



def calculate_hours(request):
    if request.method == 'GET':
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')
        hours_per_day_str = request.GET.get('hours_per_day')
        holidays_str = request.GET.get('holidays')

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            hours_per_day = int(hours_per_day_str)
            holidays = int(holidays_str)

            # Calculate hours here
            # Replace this with your actual calculation logic
            total_hours_thorique = (end_date - start_date).days * hours_per_day

            data = {
                'total_hours_thorique': total_hours_thorique,
                'total_hours_reel': []  # Replace this with your actual data
            }

            return JsonResponse(data)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)