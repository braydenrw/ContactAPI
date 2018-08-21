import json

from django.http import JsonResponse, HttpResponse, Http404
from django.core import serializers
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.middleware.csrf import get_token


from .models import Contact


def get_contact(request, contact_id):
    """ Returns a json formatted single contact by id number"""
    try:
        contact = Contact.objects.get(id=contact_id)
        output = json.loads(serializers.serialize('json', [contact]))

        del output[0]['model']

        return JsonResponse(output, safe=False)
    except Contact.DoesNotExist:
        return Http404("Contact not found")


def get_full_contact_list(request):
    """ Returns json formatted list of contacts within query parameters
        Query params:
        names: comma separated names, searches exactly case insensitive.
        emails: comma separated emails, searches exactly case insensitive.
    """
    try:
        names = request.GET.get('names')
        emails = request.GET.get('emails')
        contact_list = Contact.objects.all()

        if names is not None and emails is not None:
            names = names.split(',')
            emails = emails.split(',')

            name_queries = [Q(name__iexact=name) for name in names]
            email_queries = [Q(email__iexact=email) for email in emails]
            query = name_queries.pop()

            for elem in name_queries:
                query |= elem

            for elem in email_queries:
                query |= elem

            contact_list = contact_list.filter(query)
        elif names is not None:
            names = names.split(',')
            name_queries = [Q(name__iexact=name) for name in names]
            query = name_queries.pop()

            for elem in name_queries:
                query |= elem

            contact_list = contact_list.filter(query)
        elif emails is not None:
            emails = emails.split(',')
            email_queries = [Q(email__iexact=email) for email in emails]
            query = email_queries.pop()

            for elem in email_queries:
                query |= elem

            contact_list = contact_list.filter(query)

        output = json.loads(serializers.serialize('json', contact_list))

        for elem in output:
            del elem['model']

        return JsonResponse(output, safe=False)
    except Contact.DoesNotExist:
        return Http404("Contact not found")


def create_contact(request):
    """ Creates a new contact from an attached json payload containing the following:
        {
            name:
            phone_number:
            physical_address:
            city:
            state:
            email:
        }
        Also required are valid user credentials and a csrf token
    """
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            data = request.POST
            name = data['name']
            phone_number = data['phone_number']
            physical_address = data['physical_address']
            city = data['city']
            state = data['state']
            email = data['email']
            con = Contact.objects.create(name=name, phone_number=phone_number, physical_address=physical_address,
                                         city=city, state=state, email=email, user=request.POST.get('username'))
            c = dict(name=name, phone_number=phone_number, physical_address=physical_address, city=city, state=state,
                     email=email)
            print("Created contact for {}".format(con))
            return JsonResponse({'Created': c}, safe=False)
        else:
            return HttpResponse(status=403)

    elif request.method == 'GET':
        get_token(request)
        return HttpResponse(request)
    else:
        raise Http404("Something's wrong")


def edit_contact(request, contact_id):
    """ Modifies an existing user by given id number
        Accepts a payload with user credentials and columns to be modified as seen in contact_create.
    """
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            try:
                contact = Contact.objects.get(id=contact_id)
                update_info = request.POST
                for key in update_info.keys():
                    if key == 'name':
                        contact.name = update_info[key]
                    if key == 'phone_number':
                        contact.phone_number = update_info[key]
                    if key == 'physical_address':
                        contact.physical_address = update_info[key]
                    if key == 'city':
                        contact.city = update_info[key]
                    if key == 'state':
                        contact.state = update_info[key]
                    if key == 'email':
                        contact.email = update_info[key]
                contact.user = update_info['username']
                contact.save()
                print("Edited contact with id: {}".format(contact_id))
                return JsonResponse({'Updated': contact_id})
            except Contact.DoesNotExist:
                return HttpResponse("Contact not found")
        else:
            return HttpResponse(status=403)
    elif request.method == 'GET':
        get_token(request)
        return HttpResponse(request)
    else:
        raise Http404('Something\'s wrong')


def delete_contact(request):
    """ Deletes a user by id number given.
        Accepts a payload containing the superuser to login and contact_id to be deleted
    """
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            contact_id = request.POST['contact_id']
            try:
                Contact.objects.get(id=contact_id).delete()
                print('Deleted contact with id: {}'.format(contact_id))
                return JsonResponse({'Deleted': contact_id})
            except Contact.DoesNotExist:
                return HttpResponse('Contact does not exist')
        else:
            return HttpResponse(status=403)
    elif request.method == 'GET':
        get_token(request)
        return HttpResponse(request)
    else:
        raise Http404("Something's wrong")
