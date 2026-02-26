let currentFilter = 'all';

// Load tickets on page load
document.addEventListener('DOMContentLoaded', () => {
    loadTickets('all');
});

async function loadTickets(filter) {
    currentFilter = filter;
    
    // Update active button
    document.querySelectorAll('.btn').forEach(btn => btn.classList.remove('active'));
    document.getElementById(`btn-${filter}`).classList.add('active');
    
    // Show loading
    document.getElementById('loading').style.display = 'block';
    document.getElementById('error').style.display = 'none';
    document.getElementById('tickets-container').innerHTML = '';
    
    try {
        const url = filter === 'all' 
            ? '/api/tickets' 
            : `/api/tickets/${filter}`;
        
        const response = await fetch(url);
        const data = await response.json();
        
        if (data.success) {
            displayTickets(data.tickets, data.count);
        } else {
            showError(data.error);
        }
    } catch (error) {
        showError('Failed to load tickets: ' + error.message);
    } finally {
        document.getElementById('loading').style.display = 'none';
    }
}

function refreshTickets() {
    loadTickets(currentFilter);
}

function displayTickets(tickets, count) {
    const container = document.getElementById('tickets-container');
    const countDiv = document.getElementById('ticket-count');
    
    const p1Count = tickets.filter(t => t.priority === 'P1').length;
    const p2Count = tickets.filter(t => t.priority === 'P2').length;
    
    countDiv.innerHTML = `
        <div>Showing ${count} ticket(s)</div>
        <div style="font-size: 14px; color: #666;">
            <span style="color: #ff4444;">●</span> P1: ${p1Count} | 
            <span style="color: #ff9800;">●</span> P2: ${p2Count}
        </div>
    `;
    
    if (tickets.length === 0) {
        container.innerHTML = '<p style="text-align: center; padding: 40px; background: white; border-radius: 10px;">No tickets found.</p>';
        return;
    }
    
    container.innerHTML = tickets.map(ticket => `
        <div class="ticket-card ${ticket.priority}">
            <div class="ticket-header">
                <span class="incident-number">${ticket.incident_number || 'N/A'}</span>
                <span class="priority ${ticket.priority}">${ticket.priority}</span>
            </div>
            
            <div class="ticket-description">${ticket.description || 'No description'}</div>
            
            ${ticket.detailed_description ? `
                <div class="ticket-detailed">${ticket.detailed_description}</div>
            ` : ''}
            
            <div class="ticket-info">
                <div class="info-item">
                    <span class="info-label">Company</span>
                    <span class="info-value">${ticket.company || 'N/A'}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Customer</span>
                    <span class="info-value">${ticket.customer || 'N/A'}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Service CI</span>
                    <span class="info-value">${ticket.service_ci || 'N/A'}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Impact</span>
                    <span class="info-value">
                        <span class="impact-badge">${ticket.impact || 'N/A'}</span>
                    </span>
                </div>
                <div class="info-item">
                    <span class="info-label">Assigned Group</span>
                    <span class="info-value">${ticket.assigned_group || 'Unassigned'}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Status</span>
                    <span class="info-value">
                        <span class="status">${ticket.status || 'Unknown'}</span>
                    </span>
                </div>
            </div>
            
            <div class="ticket-footer">
                <span class="submit-date">
                    📅 ${ticket.submit_date ? formatDate(ticket.submit_date) : 'No date'}
                </span>
            </div>
        </div>
    `).join('');
}

function formatDate(dateString) {
    try {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    } catch (e) {
        return dateString;
    }
}

function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = '⚠️ Error: ' + message;
    errorDiv.style.display = 'block';
}