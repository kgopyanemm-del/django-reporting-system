from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from Reporting.models import Report
from Tracking.models import StatusUpdate, Feedback


def track_home(request):
    report = None
    error  = None

    if request.method == 'POST':
        ref = request.POST.get('reference_number', '').strip().upper()
        try:
            report = Report.objects.get(reference_number=ref)
        except Report.DoesNotExist:
            error = f"No report found with reference '{ref}'. Please check and try again."

    return render(request, 'Tracking/track_home.html', {
        'report': report,
        'error':  error,
    })


def report_detail(request, pk):
    report   = get_object_or_404(Report, pk=pk)
    updates  = report.status_updates.all()
    feedback = report.feedback.all()
    return render(request, 'Tracking/report_detail.html', {
        'report':   report,
        'updates':  updates,
        'feedback': feedback,
    })


def update_status(request, pk):
    report = get_object_or_404(Report, pk=pk)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        note       = request.POST.get('note', '')

        StatusUpdate.objects.create(
            report     = report,
            new_status = new_status,
            note       = note,
            updated_by = request.POST.get('updated_by', 'Reporter'),
        )
        report.status = new_status
        report.save()
        return redirect('report_detail', pk=pk)

    return render(request, 'Tracking/status_update.html', {'report': report})


def submit_feedback(request, pk):
    report = get_object_or_404(Report, pk=pk)

    if request.method == 'POST':
        Feedback.objects.create(
            report        = report,
            rating        = request.POST.get('rating', 3),
            resolved      = request.POST.get('resolved'),
            comment       = request.POST.get('comment', ''),
            reporter_name = request.POST.get('reporter_name', ''),
        )
        return redirect('report_detail', pk=pk)

    return render(request, 'Tracking/feedback_form.html', {'report': report})


def map_pins_json(request):
    category = request.GET.get('category', 'all')
    reports  = Report.objects.exclude(latitude=None).exclude(longitude=None)

    if category != 'all':
        reports = reports.filter(category=category)

    pins = [{
        'ref':      r.reference_number,
        'category': r.category,
        'status':   r.status,
        'location': r.location,
        'lat':      r.latitude,
        'lng':      r.longitude,
    } for r in reports]

    return JsonResponse({'pins': pins}) 
