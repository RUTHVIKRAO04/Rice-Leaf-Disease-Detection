import os
import numpy as np
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib import colors

# Create Flask app
app = Flask(__name__)
app.secret_key = 'secret-key'  # required for sessions

# Create upload folder
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# History file
HISTORY_FILE = 'prediction_history.json'

# Load trained model
model = load_model('rice_leaf_densenet121_final_model.keras')

# Class labels
class_names = ['bacterial_leaf_blight', 'brown_spot', 'healthy', 'leaf_blast', 'leaf_scald', 'narrow_brown_spot']

# Dummy user credentials
REGISTERED_USERS = {}

# Helper functions for history
def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_history(history):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)

def add_to_history(username, filename, prediction):
    history = load_history()
    if username not in history:
        history[username] = []
    history[username].append({
        'filename': filename,
        'prediction': prediction,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    save_history(history)

def generate_pdf_report(filename, prediction):
    """Generate PDF report for prediction"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=0.75*inch, leftMargin=0.75*inch,
                            topMargin=0.75*inch, bottomMargin=0.75*inch)
    
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=30,
        alignment=1
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#764ba2'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Title
    story.append(Paragraph("Rice Leaf Disease Detection Report", title_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Report Details
    story.append(Paragraph("Report Details", heading_style))
    details_data = [
        ['Generated Date:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
        ['Analysis Date:', datetime.now().strftime('%Y-%m-%d')],
    ]
    details_table = Table(details_data, colWidths=[2*inch, 4*inch])
    details_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f2ff')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e0e0e0')),
    ]))
    story.append(details_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Diagnosis
    story.append(Paragraph("Diagnosis Result", heading_style))
    diagnosis_text = f"<b>Disease Identified:</b> {prediction.replace('_', ' ').title()}"
    story.append(Paragraph(diagnosis_text, styles['Normal']))
    story.append(Spacer(1, 0.15*inch))
    
    # Recommendations
    story.append(Paragraph("Recommendations", heading_style))
    story.append(Paragraph(
        "1. <b>Immediate Action:</b> Consult with local agricultural experts for confirmation and detailed guidance.<br/>"
        "2. <b>Treatment:</b> Refer to the detailed treatment plan provided in the Disease Management section of our platform.<br/>"
        "3. <b>Prevention:</b> Implement cultural practices and disease management strategies outlined in the remedy section.<br/>"
        "4. <b>Monitoring:</b> Regularly monitor the affected plants and document progress.",
        styles['Normal']
    ))
    story.append(Spacer(1, 0.2*inch))
    
    # Footer
    story.append(Paragraph(
        "<i>This report is generated automatically. For medical diagnosis, please consult with agricultural experts.</i>",
        styles['Normal']
    ))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

# Home Page
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if user already exists
        if username in REGISTERED_USERS:
            flash("Username already exists!", "danger")
            return redirect(url_for('register'))

        # Check if passwords match
        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('register'))

        # Store user in memory
        REGISTERED_USERS[username] = {
            'email': email,
            'password': password
        }
        flash("Registered successfully. Please login.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_data = REGISTERED_USERS.get(username)

        if user_data and user_data['password'] == password:
            session['user'] = username
            return redirect(url_for('predict'))
        else:
            flash("Invalid username or password!", "danger")
            return redirect(url_for('login'))

    return render_template('login.html')



# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Logged out", "info")
    return redirect(url_for('home'))

from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Prediction
            img = image.load_img(filepath, target_size=(224, 224))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array /= 255.

            prediction = model.predict(img_array)
            predicted_class = class_names[np.argmax(prediction)]

            # Save to history
            add_to_history(session.get('user'), filename, predicted_class)

            # Pass filename & prediction to result page
            return redirect(url_for('result', filename=filename, prediction=predicted_class))

    return render_template('predict.html')

@app.route('/result')
def result():
    filename = request.args.get('filename')
    prediction = request.args.get('prediction')
    return render_template('result.html', image_path=f"uploads/{filename}", prediction=prediction)

@app.route('/export-pdf')
def export_pdf():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    filename = request.args.get('filename', 'unknown')
    prediction = request.args.get('prediction', 'unknown')
    
    pdf_buffer = generate_pdf_report(filename, prediction)
    
    return send_file(
        pdf_buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'disease_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    )

@app.route('/history')
def history():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    username = session.get('user')
    all_history = load_history()
    user_history = all_history.get(username, [])
    
    return render_template('history.html', predictions=user_history)

# Chart Page (static example chart)
@app.route('/chart')
def chart():
    return render_template('chart.html')



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
