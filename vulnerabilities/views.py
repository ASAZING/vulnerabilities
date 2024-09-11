import requests
from rest_framework import status
from .models import Vulnerability
from django.db.models import Count
from .serializers import VulnerabilitySerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes

NVD_API_URL = 'https://services.nvd.nist.gov/rest/json/cves/2.0/'
PAGE_SIZE = 10  

def save_vulnerabilities_from_nist(data):
    existing_cve_ids = set(Vulnerability.objects.values_list('cve_id', flat=True))
    
    new_vulnerabilities = []
    for vulnerability in data.get('vulnerabilities', []):
        cve_info = vulnerability.get('cve', {})
        cve_id = cve_info.get('id', '')

        descriptions = cve_info.get('descriptions', [])
        description_en = next((desc['value'] for desc in descriptions if desc['lang'] == 'en'), '')

        severity = 'Unknown'
        metrics = cve_info.get('metrics', {}).get('cvssMetricV2', [])
        if metrics:
            severity = metrics[0].get('baseSeverity', 'Unknown')

        if cve_id not in existing_cve_ids:
            new_vulnerabilities.append(
                Vulnerability(
                    cve_id=cve_id,
                    description=description_en,
                    severity=severity
                )
            )

    if new_vulnerabilities:
        Vulnerability.objects.bulk_create(new_vulnerabilities)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_vulnerabilities(request):
    try:
        page = request.GET.get('page', 1) 
        
        page = int(page)
        start_index = (page - 1) * PAGE_SIZE
        params = {
            'resultsPerPage': PAGE_SIZE,
            'startIndex': start_index,
        }
        external_response = requests.get(NVD_API_URL, params=params,timeout=20)
        print(f"Request URL: {external_response.request.url}")
        external_data = external_response.json()

        save_vulnerabilities_from_nist(external_data)
    except requests.exceptions.RequestException as e:
        return Response({'error': 'Error fetching external data', 'details': str(e)}, status=status.HTTP_502_BAD_GATEWAY)

    vulnerabilities = Vulnerability.objects.all()

    paginator = PageNumberPagination()
    paginator.page_size = 100 
    result_page = paginator.paginate_queryset(vulnerabilities, request)

    local_data_serializer = VulnerabilitySerializer(result_page, many=True)

    return paginator.get_paginated_response(local_data_serializer.data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated]) 
def fixed_vulnerabilities(request): 
    ids = request.data.get('vulnerability_ids', [])
    Vulnerability.objects.filter(cve_id__in=ids).update(is_fixed=True)

    return Response({'message': 'Vulnerabilities marked as fixed.'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated]) 
def unfixed_vulnerabilities(request): 
    ids = request.data.get('vulnerability_ids', [])
    Vulnerability.objects.filter(cve_id__in=ids).update(is_fixed=False)

    return Response({'message': 'Vulnerabilities marked as unfixed.'}, status=status.HTTP_200_OK)

@api_view(['GET']) 
@authentication_classes([TokenAuthentication]) 
@permission_classes([IsAuthenticated]) 
def get_unfixed_vulnerabilities(request): 
    vulnerabilities = Vulnerability.objects.filter(is_fixed=False)
    paginator = PageNumberPagination()
    paginator.page_size = 100
    result_page = paginator.paginate_queryset(vulnerabilities, request)

    serializer = VulnerabilitySerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET']) 
@authentication_classes([TokenAuthentication]) 
@permission_classes([IsAuthenticated]) 
def get_vulnerabilities_by_severity(request): 
    summary = Vulnerability.objects.filter(is_fixed=False).values('severity').annotate(total=Count('id'))
    return Response(summary, status=status.HTTP_200_OK)