@echo off
pyside6-uic main_window_app.ui -o ..\view\template_from_ui\main_frame.py
pyside6-uic login_app.ui -o ..\view\template_from_ui\login_frame.py
pyside6-uic register_new_customer.ui -o ..\view\template_from_ui\register_new_customer_frame.py
pyside6-uic new_work_register.ui -o ..\view\template_from_ui\new_work_frame.py
pyside6-uic forgot_password.ui -o ..\view\template_from_ui\forgot_password_frame.py


pyside6-uic check_job_progress.ui -o ..\view\template_from_ui\check_job_progress.py
pyside6-uic molecular_biology.ui -o ..\view\template_from_ui\molecular_biology_page.py
pyside6-uic barcode_page.ui -o ..\view\template_from_ui\barcode_page.py
pyside6-uic lab_report.ui -o ..\view\template_from_ui\lab_report.py
pyside6-uic lab_received_sample.ui -o ..\view\template_from_ui\lab_received_sample.py
pyside6-uic after_death.ui -o ..\view\template_from_ui\after_death.py

pyside6-uic specimen.ui -o ..\view\template_from_ui\specimen_frame.py
pyside6-uic bacteria.ui -o ..\view\template_from_ui\bacteria_frame.py
pyside6-uic parasite.ui -o ..\view\template_from_ui\parasite_frame.py
pyside6-uic edit_employee.ui -o ..\view\template_from_ui\edit_employee_frame.py


