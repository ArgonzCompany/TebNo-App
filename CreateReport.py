import jinja2
import pdfkit
from database import PatientOperations
import os
from OSHandling import OSHandling


class CreateReport(object):

    @staticmethod
    def create_file(patient_ncode):

        results = PatientOperations.patient_info_file(patient_ncode)
        
        template_loader = jinja2.FileSystemLoader(OSHandling.resource_path('resources/'))
        template_env = jinja2.Environment(loader=template_loader)

        html_template = 'report.html'
        template = template_env.get_template(html_template)

        output_result = template.render(
            name_value = results['name'],
            fname_value = results['lastname'],
            code_value = results['nationalCode'],
            phone_value = results['phoneNumber'],
            visits = results['visits']
        )

        return output_result

