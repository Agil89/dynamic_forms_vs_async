from django.shortcuts import render,redirect
from django.views.generic import TemplateView,CreateView
from mForms.forms import AllForms
from mForms.models import Forms,Fields,Values,SendList
from django.contrib import messages
import requests
import json
from asgiref.sync import sync_to_async
import asyncio,time
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.decorators import classonlymethod
from threading import Thread
# e bu zad deyishib axi :D

class FormCreateView(CreateView):
    form_class = AllForms
    template_name = 'forms.html'

    @classonlymethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        view._is_coroutine = asyncio.coroutines._is_coroutine
        return view

    async def post(self, request, *args, **kwargs):
        all_values = {}
        form_id=request.POST.get('formId')
        self.form_pk = form_id
        captcha_token = request.POST.get('g-recaptcha-response')
        cap_url = 'https://www.google.com/recaptcha/api/siteverify'
        cap_secret = '6LcUp9oZAAAAAFz1tVvpNF9EeG37qkvFFO2s9QB5'
        cap_data = {"secret":cap_secret,"response":captcha_token}
        cap_server_response = requests.post(url=cap_url,data=cap_data)
        cap_json = json.loads(cap_server_response.text)
        if cap_json['success']==False:
            messages.error(self.request, 'REcaptcha is not signed!')
            return redirect(reverse_lazy('forms:form-fields',kwargs={'pk':form_id}))
        for i in request.POST:
            if i == 'csrfmiddlewaretoken':
                continue
            elif i== 'formId':
                continue
            elif i=='g-recaptcha-response':
                continue
            elif i == 'Email':
                if '@' not in request.POST[i] and '.' not in request.POST[i]:
                    messages.error(self.request, 'Email field is not valid')
                    return redirect(reverse_lazy('forms:form-fields', kwargs={'pk': form_id}))
                # else:
                #     form = Forms.objects.filter(id=form_id).first()
                #     email = SendList(forms=form,email=request.POST[i])
                #     email.save()
            else:

                need_field = self.get_need_field(i)
                main_form = self.get_main_form(form_id)

                print(main_form)
                print(need_field)
                # main_form, need_field = self.get_fields(i, form_id) # bu nedi eeee :D
                form = Values(forms=main_form,form_fields=need_field, value=request.POST[i],)
                all_values[i]=str(request.POST[i])
                form.save()
        # functions = [
        #     asyncio.ensure_future(self.send_email(form_id, all_values)),
        # ]
        # event_loop = asyncio.get_event_loop()
        # event_loop.run_until_complete(asyncio.gather(*functions))
        task1 = asyncio.create_task(self.send_email(form_id, all_values))
        task2 = asyncio.create_task(self.send_email(form_id, all_values))
        # await asyncio.wait([task1,task2])
        # return render(request,'success.html')
        await task1
        await task2
        await asyncio.sleep(0.1)
        return HttpResponse("Non-blocking post call!")
        # Thread(target=send_email,args=(form_id, all_values)).start()
        # return render(request,'success.html')
    #
    async def __call__(self, *args, **kwargs):
        pass
    #
    @sync_to_async
    def get_main_form(self, form_id):
        main_form = Forms.objects.filter(id=form_id).first()
        return main_form

    @sync_to_async
    def get_need_field(self, label):
        need_field = Fields.objects.filter(label=label).first()
        return need_field


    @sync_to_async
    def send_email(self, form_id, all_values):
        time.sleep(15)
        template_name = 'user_info.html'
        context = {
            'all_values': all_values
        }
        msg = render_to_string(template_name, context)
        subject = 'New users info'
        user_emails = SendList.objects.filter(forms_id=form_id).values_list('email', flat=True)
        message = EmailMessage(subject=subject, body=msg, from_email=settings.EMAIL_HOST_USER, to=user_emails)
        message.content_subtype = 'html'
        message.send()



class FormsView(TemplateView):
    template_name = 'forms.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = Forms.objects.filter(id=context['pk']).first()
        context['form'] = form
        return context

