from django.core.mail import EmailMessage
from reportlab.pdfgen import canvas
from django.core.files.base import ContentFile
from home.models import Ctheft  # Your model for FIR data
from reportlab.lib.pagesizes import A4
from io import BytesIO

def generate_pdf(fir):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4  # Get PDF width and height

    # **Add a Centered Heading**
    title = "Eagle Insight - Vehicle Tracking & Alert System"
    p.setFont("Helvetica-Bold", 20)  # Set font size for title
    p.drawCentredString(width / 2, height - 50, title)  # Centered title

    # Set normal font for content
    p.setFont("Helvetica", 12)
    
    p.drawString(100, height - 100, f"FIR Number: {fir.fir_no}")
    p.drawString(100, height - 120, f"Vehicle Number: {fir.number_plate}")
    p.drawString(100, height - 140, f"Owner Name: {fir.owner_name}")
    p.drawString(100, height - 160, f"Phone: {fir.phone_number}")
    p.drawString(100, height - 180, f"Email: {fir.email}")
    p.drawString(100, height - 200, f"Vehicle Type: {fir.vehicle_type}")
    p.drawString(100, height - 220, f"Model: {fir.model_number}")
    p.drawString(100, height - 240, f"RC Number: {fir.rc_no}")
    p.drawString(100, height - 260, f"Color: {fir.vehicle_color}")
    p.drawString(100, height - 280, f"Stolen Date: {fir.date_of_theft}")
    p.drawString(100, height - 300, f"Additional Info: {fir.additional_information}")
    
    p.save()
    pdf_file = buffer.getvalue()
    buffer.close()
    
    return ContentFile(pdf_file, name=f"FIR_{fir.fir_no}.pdf")

def send_email(request, fir_id):
    
    fir = Ctheft.objects.get(fir_no=fir_id)  # Fetch FIR record
    pdf_file = generate_pdf(fir)  # Generate PDF
    
    # Send Email
    email = EmailMessage(
        subject="Your FIR Report",
        body="Attached is your FIR report.",
        from_email="",
        to=[fir.email]  # Use user email from FIR
    )
    email.attach(pdf_file.name, pdf_file.read(), "application/pdf")
    email.send()
