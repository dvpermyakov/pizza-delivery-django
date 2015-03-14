import os
import requests

ACCESS_TOKEN = 'd74d121660d8482b92a2239b44356fc1'
BASE_URL = 'https://cloud-api.yandex.net/v1/disk'

COMPANY = 'company'
VENUE = 'venue'
CATEGORY = 'category'
PRODUCT = 'product'
MODIFIER = 'modifier'


def _get_upload_url(folder, name):
    params = {
        'path': '/%s/%s' % (folder, name)
    }
    headers = {
        'Authorization': 'OAuth %s' % ACCESS_TOKEN,
        'Content-Type': 'application/json'
    }
    url = '%s/resources/upload/' % BASE_URL
    response = requests.get(url, params=params, headers=headers).json()

    return response['href']


def _get_public_preview(folder, name):
    params = {
        'path': '/%s/%s' % (folder, name),
        'preview_size': 'M'
    }
    headers = {
        'Authorization': 'OAuth %s' % ACCESS_TOKEN,
        'Content-Type': 'application/json'
    }
    url = '%s/resources/' % BASE_URL
    response = requests.get(url, params=params, headers=headers).json()

    return response['preview']


def _publish_file(folder, name):  # It returns meta-info url
    params = {
        'path': '/%s/%s' % (folder, name)
    }
    headers = {
        'Authorization': 'OAuth %s' % ACCESS_TOKEN,
        'Content-Type': 'application/json'
    }
    url = '%s/resources/publish/' % BASE_URL
    requests.put(url, params=params, headers=headers).json()

    return _get_public_preview(folder, name)


def _upload_file(folder, name, file_):
    url = _get_upload_url(folder, name)

    requests.post(url, files={
        'file': file_
    })

    return _publish_file(folder, name)


def upload_company_file(company, type_, id_, file_):
    folder = '%s_%s_%s' % (COMPANY, company.name, company.id)
    name = '%s_%s.%s' % (type_, id_, os.path.splitext(file_.name)[1])
    return _upload_file(folder, name, file_)


def upload_venue_file(venue, type_, id_, file_):
    company = venue.company
    folder = '%s_%s_%s/%s_%s_%s' % (COMPANY, company.name, company.id, VENUE, venue.name, venue.id)
    name = '%s_%s.%s' % (type_, id_, os.path.splitext(file_.name)[1])
    return _upload_file(folder, name, file_)


def delete_file(venue, type_, id_):
    company = venue.company
    params = {
        'path': '%s_%s_%s/%s_%s_%s/%s_%s' % (COMPANY, company.name, company.id, VENUE, venue.name, venue.id, type_, id_),
        'permanently': True
    }
    headers = {
        'Authorization': 'OAuth %s' % ACCESS_TOKEN,
        'Content-Type': 'application/json'
    }
    url = '%s/resources' % BASE_URL

    requests.delete(url, params=params, headers=headers)


def _create_folder(folder):
    params = {
        'path': folder
    }
    headers = {
        'Authorization': 'OAuth %s' % ACCESS_TOKEN,
        'Content-Type': 'application/json'
    }
    url = '%s/resources/' % BASE_URL

    requests.put(url, params=params, headers=headers).json()


def create_venue_folder(venue):
    company = venue.company
    _create_folder('%s_%s_%s/%s_%s_%s' % (COMPANY, company.name, company.id, VENUE, venue.name, venue.id))


def create_company_folder(company):
    _create_folder('%s_%s_%s' % (COMPANY, company.name, company.id))


def _delete_folder(folder):
    params = {
        'path': folder,
        'permanently': True
    }
    headers = {
        'Authorization': 'OAuth %s' % ACCESS_TOKEN,
        'Content-Type': 'application/json'
    }
    url = '%s/resources' % BASE_URL

    requests.delete(url, params=params, headers=headers)


def delete_venue_folder(venue):
    company = venue.company
    _delete_folder('%s_%s_%s/%s_%s_%s' % (COMPANY, company.name, company.id, VENUE, venue.name, venue.id))


def delete_company_folder(company):
    _delete_folder('%s_%s_%s' % (COMPANY, company.name, company.id))