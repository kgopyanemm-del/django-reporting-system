from django.shortcuts import render, redirect, get_object_or_404
from .models import Report

PROVINCES = [
    'Gauteng', 'Western Cape', 'KwaZulu-Natal', 'Eastern Cape',
    'Free State', 'Limpopo', 'Mpumalanga', 'North West', 'Northern Cape',
]


def home(request):
    return render(request, 'Reporting/home.html', {
        'total':     Report.objects.count(),
        'open_c':    Report.objects.filter(status='open').count(),
        'fixed_c':   Report.objects.filter(status='issue_fixed').count(),
        'provinces': PROVINCES,
    })


def report_issue(request):
    if request.method == 'POST':
        lat = request.POST.get('latitude') or None
        lng = request.POST.get('longitude') or None

        report = Report.objects.create(
            category        = request.POST.get('category'),
            sub_issue       = request.POST.get('sub_issue', ''),
            description     = request.POST.get('description'),
            location        = request.POST.get('location') or request.POST.get('addr_display', ''),
            latitude        = float(lat) if lat else None,
            longitude       = float(lng) if lng else None,
            municipality    = request.POST.get('municipality', ''),
            status          = request.POST.get('status', 'open'),
            reporter_name   = request.POST.get('reporter_name', ''),
            whatsapp_number = request.POST.get('whatsapp_number', ''),
            photo           = request.FILES.get('photo'),
        )
        return redirect('report_success', ref=report.reference_number)

    return render(request, 'Reporting/report_form.html', {'provinces': PROVINCES})


def report_success(request, ref):
    report = get_object_or_404(Report, reference_number=ref)
    return render(request, 'Reporting/report_success.html', {
        'report':    report,
        'provinces': PROVINCES,
    })


def report_list(request):
    reports  = Report.objects.all()
    category = request.GET.get('category', '')
    province = request.GET.get('province', '')
    status   = request.GET.get('status', '')

    if category:
        reports = reports.filter(category=category)
    if province:
        reports = reports.filter(location__icontains=province)
    if status:
        reports = reports.filter(status=status)

    return render(request, 'Reporting/report_list.html', {
        'reports':   reports,
        'category':  category,
        'province':  province,
        'status':    status,
        'provinces': PROVINCES,
    })


def province_reports(request):
    province = request.GET.get('province', '')
    reports  = Report.objects.filter(location__icontains=province) if province else Report.objects.none()
    return render(request, 'Reporting/report_list.html', {
        'reports':   reports,
        'province':  province,
        'provinces': PROVINCES,
})