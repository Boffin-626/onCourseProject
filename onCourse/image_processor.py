from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
import io
import easyocr

from .models import Learner, Subject, Concept, LearnerGrade

def extract_text_from_image(image_file):
    # Convert the uploaded InMemoryUploadedFile or file-like object to bytes
    img = Image.open(image_file)
    byte_io = io.BytesIO()
    img.save(byte_io, format='PNG')
    img_bytes = byte_io.getvalue()

    # Initialize EasyOCR reader and extract text
    reader = easyocr.Reader(['en'])
    result = reader.readtext(img_bytes, detail=0)
    extracted_text = " ".join(result)
    return extracted_text

def parse_report_data(extracted_text):
    lines = extracted_text.split('\n')
    report_data = {}
    for line in lines:
        if "Name" in line:
            report_data['learner_name'] = line.split(":")[-1].strip()  # Handles missing space after colon
        elif "Subject" in line:
            report_data['subject'] = line.split(":")[-1].strip()
        elif "Concept" in line:
            report_data['concept'] = line.split(":")[-1].strip()
        elif "Grade" in line:
            report_data['grade'] = line.split(":")[-1].strip()
    return report_data
           
def save_report_data(report_data):
    # Check if learner name exists
    learner_name = report_data.get('learner_name', None)
    learner_grade = report_data.get('grade', 'Not Provided')
    subject_data = report_data.get('subject_data', {})

    if learner_name:
        try:
            learner = Learner.objects.get(name=learner_name)
            # Optionally save the report for the identified learner
            print(f"Processing report for {learner_name}.")
            # learner.progress.update(grade=learner_grade, subjects=subject_data)

            return {
                "learner": learner,
                "grade": learner_grade,
                "status": "identified"
            }
        except Learner.DoesNotExist:
            print(f"Learner with name '{learner_name}' not found in the database.")
            return {
                "learner": None,
                "grade": learner_grade,
                "status": "not found"
            }
    else:
        # Log the absence of learner name, continue to process other data
        print("Learner name is missing from the report data. Proceeding without learner identification.")
        return {
            "learner": None,
            "grade": learner_grade,
            "status": "unidentified"
        }

# In your upload_report function:
def upload_report(request):
    # Assuming report_data is extracted correctly from the request
    report_data = extract_data_from_request(request)  # Placeholder for your extraction logic
    result = save_report_data(report_data)

    if result['learner']:
        # If learner is identified, we can access the learner's name
        return HttpResponse(f"Learner Grade for {result['learner'].name} saved successfully.")
    else:
        # Handle unidentified learner case
        if result['status'] == 'unidentified':
            return HttpResponse(f"Unidentified learner's report saved with grade: {result['grade']}.")
        elif result['status'] == 'not found':
            return HttpResponse(f"Report processed but learner '{report_data.get('learner_name')}' not found.")



