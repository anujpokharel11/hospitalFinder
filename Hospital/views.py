from django.shortcuts import render, redirect

from .forms import CreateClientForm
from django.contrib.auth.forms import \
    UserCreationForm  # yo UserCreationForm import nagare pani hunxa jasto lagxa malai because tala CreateUserForm import gari sake ko xa jun chai UserCreationForm nai ho  # UserCreationForm  import garnu ko karan vaneko yesle djagno ko le User ko lagi diyeko authentication form automatic dinxa... yo form use garyo vani password lai manually hash garnu pardaina... django le automatic hash gardinxa  & Username pahilai nai use vako xa ki nai vanera check garne code lekhnu parena ... django le automatic check gardinxa

from django.contrib.auth import authenticate, login, \
    logout  # django ko inbuilt feature authenticate, login, logout use garna ko lagi

from django.contrib import messages  # django le diyeko inbuilt messages featueres lai import gareko

from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required  # For bydefault django login_required decorator
from .decorators import admin_required, client_required  # For Using the functionality of decorators.py
from Hospital.models import User
from Hospital.models import Disease
from Hospital.models import Patient
from Hospital.models import Hospital
from Hospital.models import Rate

# For Contact Form to send email
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from django.contrib import messages

# For Email Confirmation after User Signup
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from django.core.mail import EmailMessage


# Create your views here.
def home(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        contact_detail = "Name:" + name + "\nEmail:\t" + email + "\nMessage:\n" + message

        if not request.user.is_authenticated:
            subject = "A Visitor's Comment"
        else:
            subject = str(request.user) + "'s Comment"

        send_mail(subject,
                  contact_detail,
                  settings.EMAIL_HOST_USER,
                  ['dipen.stha8786@gmail.com'],
                  fail_silently=False)

        messages.success(request, 'Thank you for getting in touch!')
    return render(request, 'Hospital/index.html')


def clientregisterPage(request):
    form = CreateClientForm()

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'client'
        return super().get_context_data(**kwargs)

    if request.method == 'POST':
        form = CreateClientForm(request.POST)

        if form.is_valid():
            user = form.save()  # yo code run hune bittikai  signals.py page ma user as Sender le signa pathauxa , for calling customer_profile function
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('Hospital/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()

            messages.success(request,
                             'Account activation Link has been send to email: ' + to_email + '!')  # SYNTAX:  messages.success(request,'Custom message')
            return redirect('clienthome')

    context = {'form': form}
    return render(request, 'Hospital/register.html', context)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('clienthome')
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')







def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:  # user ko value TRUE xa i.e FALSE chaina vani vaneko... khas ma mathi ko authenticate le Boolean Value return garxa i.e user authenticate vayo vani TRUE return garxa & vayena vani chai FALSE return garxa
            login(request,
                  user)  # login(request, user) django ko inbuilt keyword jastai ho jasle login vaye ko user ko session lai database ko django_session table ma hold garera rakhcha.

            if request.user.is_client:
                return redirect('clienthome')

            else:
                return redirect('adminhome')

        else:
            messages.error(request,
                           'Username OR Password is incorrect!!')  # SYNTAX: messages.info(request, 'Custom Message').......django le provide gareko informative message lai display garaune kaam garxa

    # yo talako code GET method ko lagi ho
    context = {}
    if not request.user.is_authenticated:
        return render(request, 'Hospital/login.html', context)
    else:
        return redirect('home')


@login_required  # @login_required are bydefault given by django but in setting.py we need to add LOGIN_URL ='path' as like this =>(LOGIN_URL = 'login')
def logoutall(request):
    if request.method == "POST":
        logout(request)  # logout(request) chai django le diyeko inbuilt features ho
        return redirect('login')  # logout garepaxi  feri login page ma redirect gardinxa
    return redirect('home')


@login_required  # @login_required are bydefault given by django but in setting.py we need to add LOGIN_URL ='path' as like this =>(LOGIN_URL = 'login')
@client_required
def clienthome(request):
    diseases = Disease.objects.all()  # Disease table bata j jati kura cha tyo sabai lai get garera 'disease' vanni object ma haleko. Yo Query kina gareko vanda yesle template ma drop down ma database ma jun jun disease cha tyo sabai list out garna help gareko cha.

    # Post method
    if request.method == 'POST':
        patient_name = request.POST['p_name']
        patient_age = request.POST['p_age']
        patient_location = request.POST['p_location']
        patient_contact = request.POST['p_contact']
        patient_bloodgroup = request.POST['bloodgroup']

        disease_id, patient_disease = request.POST['disease'].split(
            '-')  # select option ko value and text both chaiyo vani yesari split garera liencha.
        # ALTERNATIVE CODE # disease_id = request.POST['disease']

        userObject = request.user  # User vanni object lai userObject vanii variable ma rakheko so that hamiley tyo object dot garera disease_id  Usermodel ma add garna sakiyos vanera
        userObject.disease_id = disease_id  # hospital_User vanni table ma disease_id vanni field cha so tyo field ma user le choose gareko disease ko id store garayeko.

        userObject.save()

        patientObject = Patient()  # Patient vanni table ma yedi kei kura store garauna cha vani pahele tesko object banauna parcha.. i.e here it is 'patientObject'
        patientObject.name = patient_name  # table ko field ko ma kei kura insert garna cha vani yesari  baneko object i.e ('patientObject') dot ani field ko name ma hami user bata ayeko kura rakhdinchau
        patientObject.age = patient_age
        patientObject.location = patient_location
        patientObject.contact = patient_contact
        patientObject.blood_group = patient_bloodgroup
        patientObject.disease = patient_disease
        patientObject.user_id = request.user.id  # User Model ma vako particular logged in vako user ko id get garera tyo id lai Patient table ma rakheko as Patient Model and User Model are linked with each other with the help of user_id.
        patientObject.save()

        diseaseById = request.user.disease_id  # User Model bata hamiley disease_id lai get gareko so that tyo 'disease_id' 'getRecommendation' vanni method ma pass garna ko lagi.
        hospitals = getRecommendations(
            diseaseById)  # Jaba yo method-> 'getRecommendation(diseaseById)' call huncha yesle particular user le kun disease search gareyko cha tesko id ko through disease liyera tyo disease ko hospital lai recommend gareko huncha..
        # 'hospitals' vanni yeuta list ho jasma getRecommendation() method call hunda tyo method le return vareko values haru ayera baseko huncha.

        context = {'diseases': diseases, 'patient_disease': patient_disease, 'diseaseById': diseaseById,
                   'hospitals': hospitals}  # Key value pair ma hamiley context pass gareko so that it could be used in templates.

        return render(request, 'Hospital/clienthome.html', context)

    # Downside is get method.
    diseaseById = request.user.disease_id  # Yo Query le User Model bata pahele particular user ko 'disease_id' vanni field linxa and tyo field ma user le search gareko disease ko id ayera baseko huncha

    if diseaseById is None:  # Yo if condition kina lagauna parcha ta vanda... Yedi kunai user chai first time login gardai cha (i.e new user )cha vani User Model ma 'disease_id' suruma NULL vako huncha so tyo case check garna parcha natra error falxa.
        context = {
            'diseases': diseases}  # Yo 'diseases' vani line no. 89 mai get gareko cha so yo line le template ma disease name haru pass gardeko matrai ho becz hamailai disease name dropdown ma dekhauna cha..
        return render(request, 'Hospital/clienthome.html', context)

    else:
        patient_disease = Disease.objects.get(
            id=diseaseById)  # Disease vanni Model ma  User model bata ayeko 'disease_id' (diseaseById) lai pass garera particular disease name nikaleko so that yo chai template ma "Hospital Recommendation For {{patient_disease}}" vanera garna pawos vanera gareko..

    hospitals = getRecommendations(
        diseaseById)  # Jaba yo method-> 'getRecommendation(diseaseById)' call huncha yesle particular user le kun disease search gareyko cha tesko id ko through disease liyera tyo disease ko hospital lai recommend gareko huncha..
    # 'hospitals' vanni yeuta list ho jasma getRecommendation() method call hunda tyo method le return vareko values haru ayera baseko huncha.

    context = {'diseases': diseases, 'patient_disease': patient_disease, 'diseaseById': diseaseById,
               'hospitals': hospitals}  # Key value pair ma hamiley context pass gareko so that it could be used in templates.

    return render(request, 'Hospital/clienthome.html', context)


# Yo method sabsey important role play garcha. Yo method ko main target vaneko database ko Linker Table (i.e hospital_diesase_hospitals<= ManyToManyField() le create gardeko table) ma kam gareko cha..
def getRecommendations(diseaseById):
    hospitalById = list(Disease.hospitals.through.objects.filter(disease_id=diseaseById).values(
        'hospital_id'))  # 1. Suru ma ta disease_id as a parameter auncha method call hunda. (method call clienthome() method bata vako cha..)
    # 2. Yo Query le  tyo ayeko 'disease_id' liyera Linker Table bata jati pani 'disease_id' gareko diseases haru cha tesbata hospitals haru nikalni kam gareko cha.[ .values('hospital_id') garera hospitals haru filterout gareko cha]
    # 3. Linker Table ma query chalauna at first:
    #			i) Model ma hererera ManyToManyField() kun Model name ma cha patta lagauna paryo => In our case it's in 'Disease' Model
    #			   tesailey query ko suru mai 'Disease' vanera haleko
    #			ii) Disease vanni model ma ManyToManyField() gareko field ko name 'hospitals' vanni cha tesailey query ma 'Disease.hospitals' vanera aako ho.
    #			iii) '.through' pani use garnai parcha kina ki Hami Linker Table ma kam gardai chau..
    # 4. Ayeko Queryset lai hami le 'list' ma convert gardiyeko so that haneko query bata ayeko hospital_id lai sajilai nikalna sakos vanera.
    # 5. IMP NOTEE: .values('hospital_id') le dictionary return gardincha so ava hamro 'hospitalById' vanni list vitra yeuta dictionary baseko huncha..

    # hospitalById<{'hospital_id':3}, {'hospital_id':4}, {'hospital_id':5}, {'hospital_id':6}>	#hospitalById query set ma exact yesari value ayerako huncha.

    recommended_hospital = []  # recommended_hospital yeuta khali list create gareko..
    for i in range(len(
            hospitalById)):  # 'hospitalById' aba yeuta as a list jasto vitra values haru chai as  a dictionary ko rup ma baseko huncha so tesma loop chalayeko.
        recommended_hospital.append(hospitalById[i][
                                        'hospital_id'])  # 'hospitalById' vanni list vitra ko dictionary bata hamilai aba key chaindaina tara 'values' haru chai chaini vako le yesto gareko => "hospitalById[i]['hospital_id']". yo dictionary ma hareko values ko key vaney feri 'hospital_id' nai baseko huncha..
    # tespachi loop bata jati ni values haru ayeko cha teslai recommended_hospital vanni list ma append gardeko.. append garena vani loop bata ayeko last ko values matra gayera bascha..

    hospitals = []  # yeuta hospitals vanni khali list create gareko.
    for i in range(len(
            recommended_hospital)):  # ahiley sama ta 'recommended_hospital' list ma hospital ko id matrai baseko cha. Aba hamilai tyo hospital ko id ko through hamilai hospital ko name chayeko cha so loop lagayera 'Hospital' table ma hospital ko name haru nilakera 'hospitals' vanni list ma rakheko ho
        hospitals += Hospital.objects.filter(id=recommended_hospital[i])
    return hospitals  # Yesle method call hunda 'hospitals' vanni list lai return garcha jasma hamro particular patient lai lageko ko disease ko adhar ma hospitals haru ayera baseko huncha..


def detail(request, hospital_id):
    hospital = get_object_or_404(Hospital, id=hospital_id)

    if request.method == "POST":
        rate = request.POST['rating']
        rateObject = Rate()
        rateObject.user = request.user
        rateObject.hospital = hospital
        rateObject.rating = rate
        rateObject.save()
        messages.success(request, "Your Rating has been submited.")

    context = {'hospital': hospital}
    return render(request, 'Hospital/detail.html', context)


@login_required  # @login_required are bydefault given by django but in setting.py we need to add LOGIN_URL ='path' as like this =>(LOGIN_URL = 'login')
@admin_required
def adminhome(request):
    context = {}
    return render(request, 'Hospital/adminhome.html', context)


@login_required  # @login_required are bydefault given by django but in setting.py we need to add LOGIN_URL ='path' as like this =>(LOGIN_URL = 'login')
@admin_required
def customerdetail(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'Hospital/customerdetail.html', context)


# Find hospital function to display all the hospitals.
def findHospital(request):
    query = request.GET.get('searchvalue')

    if query:
        hospital = Hospital.objects.filter(Q(name__icontains=query)).distinct()
        context = {'hospital_list': hospital}
        return render(request, 'Hospital/hospital_list.html', context)

    hospital_list = Hospital.objects.all()

    context = {'hospital_list': hospital_list}
    return render(request, 'Hospital/hospital_list.html', context)
