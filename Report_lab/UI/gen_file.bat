@echo off
pyside6-uic main_window_app.ui -o ..\view\template_from_ui\main_frame.py
pyside6-uic login_app.ui -o ..\view\template_from_ui\login_frame.py
pyside6-uic forgot_password.ui -o ..\view\template_from_ui\forgot_password_frame.py
pyside6-uic send_report_pdf.ui -o ..\view\template_from_ui\send_report_pdf_frame.py
pyside6-uic receive_lab.ui -o ..\view\template_from_ui\receive_lab_frame.py
pyside6-uic error_page.ui -o ..\view\template_from_ui\error_page_frame.py
pyside6-uic lab_edite_form.ui -o ..\view\template_from_ui\lab_edit_form_frame.py
pyside6-uic merg_report_form.ui -o ..\view\template_from_ui\Export_form_frame.py