from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee
import random
from datetime import datetime
from .forms import EmpForm
from django.template.loader import render_to_string
from django.http import Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


def p_range(pages, num_page):   # function which creates convenient list of page-numbers;
    p_set = {1, pages.num_pages}
    try:
        num_page = int(num_page)
    except (ValueError, TypeError):
        num_page = 1
    base_set = set(pages.page_range)
    p_set.update(range(num_page - 5, num_page + 6))
    p_set.update(range(0, pages.num_pages, 50))
    p_set.intersection_update(base_set)
    return sorted(list(p_set))


def ftree(request):
    employees = Employee.objects.all()
    pages = Paginator(employees, 50)
    num_page = request.GET.get('page')
    p_list = p_range(pages, num_page)
    try:
        page_content = pages.page(num_page)
        first_obj_level = page_content.object_list[0].level
        for obj in page_content.object_list:
            if first_obj_level > obj.level:
                return render(request, 'emp/simple.html', {'emps': page_content, 'p_list': p_list})

    except PageNotAnInteger:
        page_content = pages.page(1)
    except EmptyPage:
        page_content = pages.page(pages.num_pages)
    return render(request, 'emp/tree.html', {'emps': page_content, 'p_list': p_list})


def all_table(request):
    try:
        field = request.GET.get('field')
        text = request.GET.get('text')
        order_by_ = request.GET.get('order_by')
        emp1 = Employee.objects.filter(full_name__icontains=text)
        emp2 = Employee.objects.filter(id__icontains=text)
        emp3 = Employee.objects.filter(chief__full_name__icontains=text)
        emp4 = Employee.objects.filter(emp_position__icontains=text)
        emp5 = Employee.objects.filter(date_of_recruit__icontains=text)
        emp6 = Employee.objects.filter(salary__icontains=text)
        emp7 = Employee.objects.filter(level__icontains=text)
        emp8 = emp1.union(emp2, emp3, emp4, emp5, emp6, emp7)
        if field == 'full_name':
            employee = emp1
        elif field == 'id':
            employee = emp2
        elif field == 'chief':
            employee = emp3
        elif field == 'emp_position':
            employee = emp4
        elif field == 'date_of_recruit':
            employee = emp5
        elif field == 'salary':
            employee = emp6
        elif field == 'level':
            employee = emp7
        else:
            employee = emp8
        employees = employee.order_by(order_by_)
    except (TypeError, ValueError):
        employees = Employee.objects.all()
    pages = Paginator(employees, 50)
    num_page = request.GET.get('page')
    try:
        page_content = pages.page(num_page)
    except PageNotAnInteger:
        page_content = pages.page(1)
    except EmptyPage:
        page_content = pages.page(pages.num_pages)
    p_list = p_range(pages, num_page)
    return render(request, 'emp/all_table.html', {'emps': page_content, 'p_list': p_list})


@login_required
def table_ajx(request):
    try:
        if request.method == 'POST' and request.is_ajax():
            field = request.POST.get('field')
            text = request.POST.get('text')
            order_by_ = request.POST.get('order_by')
            emp1 = Employee.objects.filter(full_name__icontains=text)
            emp2 = Employee.objects.filter(id__icontains=text)
            emp3 = Employee.objects.filter(chief__full_name__icontains=text)
            emp4 = Employee.objects.filter(emp_position__icontains=text)
            emp5 = Employee.objects.filter(date_of_recruit__icontains=text)
            emp6 = Employee.objects.filter(salary__icontains=text)
            emp7 = Employee.objects.filter(level__icontains=text)
            emp8 = emp1.union(emp2, emp3, emp4, emp5, emp6, emp7)
            if field == 'full_name':
                employee = emp1
            elif field == 'id':
                employee = emp2
            elif field == 'chief':
                employee = emp3
            elif field == 'emp_position':
                employee = emp4
            elif field == 'date_of_recruit':
                employee = emp5
            elif field == 'salary':
                employee = emp6
            elif field == 'level':
                employee = emp7
            else:
                employee = emp8
            employees = employee.order_by(order_by_)
            pages = Paginator(employees, 50)
            num_page = request.GET.get('page')
            try:
                page_content = pages.page(num_page)
            except PageNotAnInteger:
                page_content = pages.page(1)
            except EmptyPage:
                page_content = pages.page(pages.num_pages)
            p_list = p_range(pages, num_page)
            temp = render_to_string('emp/ajax.html', {'emps': page_content, 'p_list': p_list})
            context = {'response': temp, 'result': 'success'}
            return JsonResponse(context)
        else:
            employees = Employee.objects.all()
            pages = Paginator(employees, 50)
            num_page = request.GET.get('page')
            try:
                page_content = pages.page(num_page)
            except PageNotAnInteger:
                page_content = pages.page(1)
            except EmptyPage:
                page_content = pages.page(pages.num_pages)
            p_list = p_range(pages, num_page)
            return render(request, 'emp/aj_temp.html', {'emps': page_content, 'p_list': p_list})
    except (TypeError, ValueError):
        raise Http404


@login_required
def get_descendants(request):
    if request.method == "GET":
        try:
            emp_id = request.GET.get('id')
            employee = Employee.objects.get(id=emp_id)
            emp_descendants = employee.get_descendants(include_self=True)
        except TypeError:
            raise Http404
        except ObjectDoesNotExist:
            return render(request, 'emp/no_desc.html')
        pages = Paginator(emp_descendants, 50)
        num_page = request.GET.get('page')
        try:
            page_content = pages.page(num_page)
        except PageNotAnInteger:
            page_content = pages.page(1)
        except EmptyPage:
            page_content = pages.page(pages.num_pages)
        p_list = p_range(pages, num_page)
        return render(request, 'emp/aj_temp.html', {'emps': page_content, 'p_list': p_list})

@login_required
def emp_edit(request, pk):
    emp = get_object_or_404(Employee, pk=pk)
    if request.method == "POST":
        form = EmpForm(request.POST, request.FILES, instance=emp)
        if form.is_valid():
            emp = form.save()
            emp.save()
            return render(request, 'emp/emp_detail.html', {'emp': emp})
    else:
        form = EmpForm(instance=emp)
        return render(request, 'emp/emp_edit.html', {'form': form, 'emp': emp})


@login_required
def create_emp(request):
    if request.method == "POST":
        form = EmpForm(request.POST, request.FILES)
        if form.is_valid():
            emp = form.save()
            emp.save()
            return render(request, 'emp/emp_detail.html', {'emp': emp})
    else:
        form = EmpForm()
        return render(request, 'emp/emp_edit.html', {'form': form})


@login_required
def del_emp(request):
    try:
        if request.method == 'POST' and request.is_ajax():
            button = request.POST.get('delete')
            if button:
                if button == 'del':
                    if request.POST.get('empl'):
                        emp_id = request.POST.get('empl')
                        emp = Employee.objects.get(id=emp_id)
                        temp = render_to_string('emp/del_temp.html', {'emp': emp})
                    context = {'response': temp, 'result': 'success'}
                    return JsonResponse(context)
        else:
            button = request.GET.get('id')
            emp = get_object_or_404(Employee, pk=button)
            emp.delete()
            return redirect('ajx')
    except (TypeError, ValueError):
        raise Http404



#####################################SEEDER############################################################################
def make_sex():
    sex = ('male', 'female')
    return random.choice(sex)

names_ma = ['Andrey', 'Vladimir', 'Sergey', 'Mihail', 'Evgeniy', 'Aleksandr', 'Vsevolod', 'Arkadiy', 'Gennadiy',
    'Petro', 'Dmitriy', 'Denis', 'Fedor', 'Ostap', 'Juriy',
    'Konstantin', 'Pavlo', 'Semen', 'Vitaliy']

def make_name(sex):
    names_fe = ['Anna', 'Anastasia', 'Daria', 'Ludmila', 'Aleksandra', 'Varvara', 'Maria', 'Antonina', 'Lea',
                'Vasilisa', 'Elena', 'Ekaterina', 'Belka', 'Svetlana', 'Yana', 'Julia', ]
    if sex == 'male':
        return random.choice(names_ma)
    else:
        return random.choice(names_fe)

def make_surname(sex):
    sur = ''
    next = 'a'
    vowel = 'aeyuio'
    consonant = 'qwrtpsdfghjklzxcvbnm'
    alpha = vowel + consonant
    length = random.choice(range(4,9))
    for n in range(length):
        if next == 'a':
            sur += random.choice(alpha)
        elif next == 'c':
            sur += random.choice(consonant)
        else:
            sur += random.choice(vowel)
        if n == 0 and sur[n] in vowel:
            next = 'c'
        elif n >= 1 and (sur[n] in vowel and sur[n-1] in vowel):
            next = 'c'
        elif n >= 1 and (sur[n] in consonant and sur[n-1] in consonant):
            next = 'v'
        elif n-1 >= 0 and ((sur[n] in vowel) != (sur[n-1] in vowel)):
            next = 'a'
    end_male = ('uk', 'ov')
    end_female = ('uk', 'ova')
    end_ma = random.choice(end_male)
    end_fe = random.choice(end_female)

    if sur.endswith(tuple(vowel)):
        sur += 'ko'
    elif sex == 'male':
        sur += end_ma
    else:
        sur += end_fe
    return sur.capitalize()

def make_fathers(sex):
    fathersstart =random.choice(names_ma)
    if sex == 'male':
        if fathersstart.endswith('y'):
            return fathersstart.rstrip('y') + 'evich'
        else:
            return fathersstart + 'ovich'
    else:
        if fathersstart.endswith('y'):
            return fathersstart.rstrip('y') + 'evna'
        else:
            return fathersstart + 'ovna'

def make_fullname():
    sex = make_sex()
    return make_surname(sex) + ' ' + make_name(sex) + ' ' + make_fathers(sex)

def make_datetime():
    year = random.randint(1970, 2018)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    hour = random.randint(1, 23)
    minute = random.randint(1, 59)
    return datetime(year, month, day, hour, minute)

def make_empposition():
    pos = ('accountant', 'manager', 'director of security', 'developer', 'architector', 'project manager',
                         'auditor', 'collector', 'driver', 'cleaner', 'electrician', 'engineer', 'explorer', 'financier',
                         'guide', 'market coach', 'interpreter')
    return random.choice(pos)

def make_salary():
    return random.randrange(3000, 70000)


def make_employee(request):
    if request.method == "GET":
        return render(request, 'emp/make_emp.html')
    else:
        ids = []
        level = request.POST.get('Chief level')
        quantity = int(request.POST.get('quantity'))
        id_ = Employee.objects.filter(level=int(level)).values('id')
        for dic in id_:
            ids += (dic.values())

        with transaction.atomic():
            with Employee.objects.disable_mptt_updates():
                objs = (Employee(full_name=make_fullname(), emp_position=make_empposition(),
                                    chief=Employee.objects.get(id=random.choice(ids)),
                                    date_of_recruit=make_datetime(), salary=make_salary()) for i in range(quantity))

                batch = list(objs)

                emp = Employee.objects.bulk_create(batch, quantity)
            Employee.objects.rebuild()
    return redirect('root')

###################################################### END OF SEEDER ###################################################
