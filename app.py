from flask import Flask, render_template, jsonify
from google.cloud import bigquery
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize BigQuery client
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
client = bigquery.Client(project=os.getenv('GCP_PROJECT_ID'))

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# API endpoint to fetch all P1/P2 tickets
@app.route('/api/tickets')
def get_tickets():
    try:
        # Query for all tickets (table already filtered to P1/P2)
        query = f"""
            SELECT 
                INCIDENT_NUMBER,
                COMPANY,
                PRIORITY,
                CUSTOMER,
                SERVICECI,
                IMPACT,
                Assigned_Group,
                STATUS,
                SUBMIT_DATE,
                DESCRIPTION,
                DETAILED_DECRIPTION
            FROM `{os.getenv('GCP_PROJECT_ID')}.{os.getenv('BIGQUERY_DATASET')}.{os.getenv('BIGQUERY_TABLE')}`
            ORDER BY SUBMIT_DATE DESC
            LIMIT 100
        """
        
        # Execute query
        query_job = client.query(query)
        results = query_job.result()
        
        # Convert to list of dictionaries
        tickets = []
        for row in results:
            tickets.append({
                'incident_number': row.INCIDENT_NUMBER,
                'company': row.COMPANY,
                'priority': row.PRIORITY,
                'customer': row.CUSTOMER,
                'service_ci': row.SERVICECI,
                'impact': row.IMPACT,
                'assigned_group': row.Assigned_Group,
                'status': row.STATUS,
                'submit_date': str(row.SUBMIT_DATE) if row.SUBMIT_DATE else None,
                'description': row.DESCRIPTION,
                'detailed_description': row.DETAILED_DECRIPTION
            })
        
        return jsonify({
            'success': True,
            'count': len(tickets),
            'tickets': tickets
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Filter by priority (P1 or P2)
@app.route('/api/tickets/<priority>')
def get_tickets_by_priority(priority):
    try:
        # Validate priority
        if priority not in ['P1', 'P2']:
            return jsonify({
                'success': False,
                'error': 'Invalid priority. Use P1 or P2.'
            }), 400
        
        query = f"""
            SELECT 
                INCIDENT_NUMBER,
                COMPANY,
                PRIORITY,
                CUSTOMER,
                SERVICECI,
                IMPACT,
                Assigned_Group,
                STATUS,
                SUBMIT_DATE,
                DESCRIPTION,
                DETAILED_DECRIPTION
            FROM `{os.getenv('GCP_PROJECT_ID')}.{os.getenv('BIGQUERY_DATASET')}.{os.getenv('BIGQUERY_TABLE')}`
            WHERE PRIORITY = '{priority}'
            ORDER BY SUBMIT_DATE DESC
            LIMIT 100
        """
        
        query_job = client.query(query)
        results = query_job.result()
        
        tickets = []
        for row in results:
            tickets.append({
                'incident_number': row.INCIDENT_NUMBER,
                'company': row.COMPANY,
                'priority': row.PRIORITY,
                'customer': row.CUSTOMER,
                'service_ci': row.SERVICECI,
                'impact': row.IMPACT,
                'assigned_group': row.Assigned_Group,
                'status': row.STATUS,
                'submit_date': str(row.SUBMIT_DATE) if row.SUBMIT_DATE else None,
                'description': row.DESCRIPTION,
                'detailed_description': row.DETAILED_DECRIPTION
            })
        
        return jsonify({
            'success': True,
            'count': len(tickets),
            'tickets': tickets
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Optional: Filter by status
@app.route('/api/tickets/status/<status>')
def get_tickets_by_status(status):
    try:
        query = f"""
            SELECT 
                INCIDENT_NUMBER,
                COMPANY,
                PRIORITY,
                CUSTOMER,
                SERVICECI,
                IMPACT,
                Assigned_Group,
                STATUS,
                SUBMIT_DATE,
                DESCRIPTION,
                DETAILED_DECRIPTION
            FROM `{os.getenv('GCP_PROJECT_ID')}.{os.getenv('BIGQUERY_DATASET')}.{os.getenv('BIGQUERY_TABLE')}`
            WHERE UPPER(STATUS) = UPPER('{status}')
            ORDER BY SUBMIT_DATE DESC
            LIMIT 100
        """
        
        query_job = client.query(query)
        results = query_job.result()
        
        tickets = []
        for row in results:
            tickets.append({
                'incident_number': row.INCIDENT_NUMBER,
                'company': row.COMPANY,
                'priority': row.PRIORITY,
                'customer': row.CUSTOMER,
                'service_ci': row.SERVICECI,
                'impact': row.IMPACT,
                'assigned_group': row.Assigned_Group,
                'status': row.STATUS,
                'submit_date': str(row.SUBMIT_DATE) if row.SUBMIT_DATE else None,
                'description': row.DESCRIPTION,
                'detailed_description': row.DETAILED_DECRIPTION
            })
        
        return jsonify({
            'success': True,
            'count': len(tickets),
            'tickets': tickets
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)