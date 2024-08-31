from django.shortcuts import render
from Ships.models import PositionReport
def main(request):
    return render(request,'stat.html')
def AIS(request):
    reports = PositionReport.objects.all()
    return render(request, 'Ships/position_reports.html', {'reports': reports})
# Create your views here.
