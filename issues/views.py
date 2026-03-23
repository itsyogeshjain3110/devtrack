import json
from pathlib import Path

from rest_framework.decorators import api_view
from .models import Issue, Reporter, CriticalIssue, HighPriorityIssue, MediumPriorityIssue, LowPriorityIssue
from django.http import JsonResponse

# Create your views here.

BASE_DIR = Path(__file__).resolve().parent.parent
REPORTERS_FILE = BASE_DIR / 'reporters.json'
ISSUES_FILE = BASE_DIR / 'issues.json'


def _load_records(file_path):
    if not file_path.exists():
        return []
    with file_path.open('r', encoding='utf-8') as f:
        data = json.load(f)
    if isinstance(data, list):
        return data
    return []


def _save_records(file_path, records):
    with file_path.open('w', encoding='utf-8') as f:
        json.dump(records, f, indent=2)

def create_reporter(request):
    data = request.data
    try:
        reporter = Reporter(
            id=data.get('id'),
            name=data.get('name'),
            email=data.get('email'),
            team=data.get('team')
        )
        reporter.validate()
        reporter_data = reporter.to_dict()
        reporters = _load_records(REPORTERS_FILE)
        if any(str(item.get('id')) == str(reporter_data.get('id')) for item in reporters):
            return JsonResponse({'error': 'Reporter with this id already exists'}, status=400)
        reporters.append(reporter_data)
        _save_records(REPORTERS_FILE, reporters)
        return JsonResponse(reporter_data, status=201)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)

def list_reporters(request):
    try:
        reporters = _load_records(REPORTERS_FILE)
        return JsonResponse(reporters, safe=False, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_reporter(request, reporter_id):
    try:
        reporters = _load_records(REPORTERS_FILE)
        for reporter in reporters:
            if str(reporter.get('id')) == str(reporter_id):
                return JsonResponse(reporter, status=200)
        return JsonResponse({'error': 'Reporter not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


    
def create_issue(request):
    data = request.data
    try:
        if data['priority'] == 'critical':
            issue = CriticalIssue(
                id=data.get('id'),
                title=data.get('title'),
                description=data.get('description'),
                status=data.get('status'),
                priority=data.get('priority'),
                reporter_id=data.get('reporter_id')
            )
        elif data['priority'] == 'high':
            issue = HighPriorityIssue(
                id=data.get('id'),
                title=data.get('title'),
                description=data.get('description'),
                status=data.get('status'),
                priority=data.get('priority'),
                reporter_id=data.get('reporter_id')
            )
        elif data['priority'] == 'medium':
            issue = MediumPriorityIssue(
                id=data.get('id'),
                title=data.get('title'),
                description=data.get('description'),
                status=data.get('status'),
                priority=data.get('priority'),
                reporter_id=data.get('reporter_id')
            )
        elif data['priority'] == 'low':
            issue = LowPriorityIssue(
                id=data.get('id'),
                title=data.get('title'),
                description=data.get('description'),
                status=data.get('status'),
                priority=data.get('priority'),
                reporter_id=data.get('reporter_id')
            )
        else:
            issue = Issue(
                id=data.get('id'),
                title=data.get('title'),
                description=data.get('description'),
                status=data.get('status'),
                priority=data.get('priority'),
                reporter_id=data.get('reporter_id')
            )
        issue.validate()
        response_data = issue.to_dict()
        issues = _load_records(ISSUES_FILE)
        if any(str(item.get('id')) == str(response_data.get('id')) for item in issues):
            return JsonResponse({'error': 'Issue with this id already exists'}, status=400)
        issues.append(response_data)
        _save_records(ISSUES_FILE, issues)
        response_data['message'] = issue.describe()
        return JsonResponse(response_data, status=201)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)
    
def get_issue(request, issue_id):
    try:
        issues = _load_records(ISSUES_FILE)
        for issue in issues:
            if str(issue.get('id')) == str(issue_id):
                return JsonResponse(issue, status=200)
        return JsonResponse({'error': 'Issue not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def list_issues(request):
    try:
        issues = _load_records(ISSUES_FILE)
        response_data = []
        status = request.query_params.get('status')
        for issue in issues:
            if status and issue.get('status') != status:
                continue
            response_data.append(issue)
        return JsonResponse(response_data, safe=False, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    


@api_view(['GET', 'POST'])
def issues_collection(request):
    if request.method == 'POST':
        return create_issue(request)
    elif request.method == 'GET' and (request.query_params.get('id')):
        return get_issue(request, issue_id=request.query_params.get('id'))
    elif request.method == 'GET':
        return list_issues(request)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    

@api_view(['GET', 'POST'])
def reporters_collection(request):
    if request.method == 'POST':
        return create_reporter(request)
    elif request.method == 'GET' and (request.query_params.get('id')):
        return get_reporter(request, reporter_id=request.query_params.get('id'))
    elif request.method == 'GET':
        return list_reporters(request)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)