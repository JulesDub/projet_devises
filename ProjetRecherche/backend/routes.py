from flask import Blueprint, request, jsonify
from models import db, Devise, Cours
import csv
from datetime import datetime

app_routes = Blueprint('app_routes', __name__)

@app_routes.route('/api/devises', methods=['GET'])
def get_devises():
    devises = Devise.query.all()
    return jsonify([{'id': devise.id, 'nom': devise.nom, 'symbole': devise.symbole} for devise in devises])

@app_routes.route('/api/cours/<string:symbole>', methods=['GET'])
def get_cours(symbole):
    devise = Devise.query.filter_by(symbole=symbole).first()
    if not devise:
        return jsonify({'message': 'Devise not found'}), 404
    cours = Cours.query.filter_by(devise_id=devise.id).all()
    return jsonify([{'id': c.id, 'valeur': str(c.valeur), 'date': c.date.isoformat()} for c in cours])

@app_routes.route('/api/cours/upload', methods=['POST'])
def upload_csv():
    file = request.files['file']
    if not file or not file.filename.endswith('.csv'):
        return jsonify({'message': 'Le fichier doit être un CSV'}), 400
    
    try:
        # Ouvrir le fichier en mode texte
        file.stream.seek(0)  # Revenir au début du fichier
        content = file.stream.read().decode('utf-8').splitlines()
        reader = csv.DictReader(content)

        # Identifier le nom de la colonne de la devise
        fieldnames = reader.fieldnames
        if not fieldnames or len(fieldnames) < 2:
            return jsonify({'message': 'Le CSV doit contenir au moins deux colonnes : DateTime et une devise'}), 400
        date_column = fieldnames[0]
        devise_column = fieldnames[1]

        # Déterminer le symbole de la devise
        devise_symbole = devise_column.split('_')[0]  # Supposons que le nom soit sous la forme 'XYZ_to_EUR'

        for row in reader:
            print(f"Lecture de la ligne: {row}")

            if date_column not in row or devise_column not in row:
                return jsonify({'message': f'Le CSV doit contenir les colonnes {date_column} et {devise_column}'}), 400

            devise = Devise.query.filter_by(symbole=devise_symbole).first()
            if not devise:
                devise = Devise(nom=devise_symbole, symbole=devise_symbole)
                db.session.add(devise)
                db.session.commit()

            cours = Cours(devise_id=devise.id, valeur=row[devise_column], date=datetime.strptime(row[date_column], '%Y-%m-%d %H:%M:%S.%f'))
            db.session.add(cours)
        
        db.session.commit()
        return 'Upload Successful', 201
    except Exception as e:
        print(f"Erreur lors du traitement du fichier: {str(e)}")
        return jsonify({'message': f'Erreur lors du chargement du fichier: {str(e)}'}), 500


