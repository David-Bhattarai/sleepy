/**
 * Admin Dashboard JavaScript
 * Complete database management for AURA Mental Health Platform
 */

document.addEventListener('DOMContentLoaded', () => {
    // Check admin authentication
    checkAdminAuth();
    
    // Initialize admin dashboard
    initializeAdminDashboard();
});

// Global variables
let currentTable = 'users';
let tableData = {};
let currentUser = null;

// Database table configurations
const tableConfigs = {
    users: {
        title: '👥 Users Table',
        endpoint: '/api/admin/users',
        columns: ['id', 'name', 'email', 'phone', 'gender', 'is_admin', 'created_at'],
        displayNames: ['ID', 'Name', 'Email', 'Phone', 'Gender', 'Admin', 'Created'],
        primaryKey: 'id'
    },
    doctors: {
        title: '👨‍⚕️ Doctors Table',
        endpoint: '/api/admin/doctors',
        columns: ['id', 'name', 'specialty', 'qualification', 'experience_years', 'price_per_session', 'is_available'],
        displayNames: ['ID', 'Name', 'Specialty', 'Qualification', 'Experience', 'Price', 'Available'],
        primaryKey: 'id'
    },
    appointments: {
        title: '📅 Appointments Table',
        endpoint: '/api/admin/appointments',
        columns: ['id', 'user_id', 'doctor_id', 'appointment_date', 'appointment_time', 'status', 'payment_status'],
        displayNames: ['ID', 'User ID', 'Doctor ID', 'Date', 'Time', 'Status', 'Payment'],
        primaryKey: 'id'
    },
    chat_history: {
        title: '💬 Chat History Table',
        endpoint: '/api/admin/chat_history',
        columns: ['id', 'user_id', 'user_message', 'ai_response', 'sentiment', 'timestamp'],
        displayNames: ['ID', 'User ID', 'User Message', 'AI Response', 'Sentiment', 'Timestamp'],
        primaryKey: 'id'
    },
    simple_mood_entries: {
        title: '😊 Simple Mood Entries Table',
        endpoint: '/api/admin/mood_entries',
        columns: ['id', 'user_id', 'mood_rating', 'mood_notes', 'timestamp'],
        displayNames: ['ID', 'User ID', 'Rating', 'Notes', 'Timestamp'],
        primaryKey: 'id'
    },
    payments: {
        title: '💳 Payments Table',
        endpoint: '/api/admin/payments',
        columns: ['id', 'user_id', 'appointment_id', 'amount', 'payment_method', 'payment_status', 'payment_date'],
        displayNames: ['ID', 'User ID', 'Appointment ID', 'Amount', 'Method', 'Status', 'Date'],
        primaryKey: 'id'
    },
    face_emotion_detection: {
        title: '😐 Emotion Detection Table',
        endpoint: '/api/admin/emotions',
        columns: ['id', 'user_id', 'detected_emotion', 'confidence_score', 'timestamp'],
        displayNames: ['ID', 'User ID', 'Emotion', 'Confidence', 'Timestamp'],
        primaryKey: 'id'
    },
    emotional_intelligence_scores: {
        title: '🧠 Emotional Intelligence Table',
        endpoint: '/api/admin/emotional_intelligence',
        columns: ['id', 'user_id', 'awareness_score', 'regulation_score', 'timestamp'],
        displayNames: ['ID', 'User ID', 'Awareness', 'Regulation', 'Timestamp'],
        primaryKey: 'id'
    },
    mood_entries_advanced: {
        title: '📈 Advanced Mood Entries Table',
        endpoint: '/api/admin/mood_entries_advanced',
        columns: ['id', 'user_id', 'mood_rating', 'energy_level', 'sleep_quality', 'stress_level', 'timestamp'],
        displayNames: ['ID', 'User ID', 'Mood', 'Energy', 'Sleep', 'Stress', 'Timestamp'],
        primaryKey: 'id'
    },
    mood_insights: {
        title: '💡 Mood Insights Table',
        endpoint: '/api/admin/mood_insights',
        columns: ['id', 'user_id', 'insight_type', 'insight_data', 'confidence_score', 'generated_at'],
        displayNames: ['ID', 'User ID', 'Type', 'Data', 'Confidence', 'Generated'],
        primaryKey: 'id'
    },
    mood_patterns: {
        title: '📊 Mood Patterns Table',
        endpoint: '/api/admin/mood_patterns',
        columns: ['id', 'user_id', 'pattern_type', 'pattern_data', 'strength', 'last_updated'],
        displayNames: ['ID', 'User ID', 'Type', 'Data', 'Strength', 'Updated'],
        primaryKey: 'id'
    },
    doctor_availability: {
        title: '🕒 Doctor Availability Table',
        endpoint: '/api/admin/doctor_availability',
        columns: ['id', 'doctor_id', 'day_of_week', 'start_time', 'end_time', 'is_available'],
        displayNames: ['ID', 'Doctor ID', 'Day', 'Start Time', 'End Time', 'Available'],
        primaryKey: 'id'
    }
};

// Authentication functions
function checkAdminAuth() {
    const token = localStorage.getItem('authToken') || localStorage.getItem('token');
    const isAdmin = localStorage.getItem('isAdmin') === 'true';
    
    // Allow access for ALL authenticated users (not just admins)
    if (!token) {
        alert('Please login first. Redirecting to login...');
        window.location.href = '/signin.html';
        return;
    }
    
    // Set current user info
    const userName = localStorage.getItem('userName') || (isAdmin ? 'Admin' : 'User');
    const adminNameElement = document.getElementById('admin-name');
    if (adminNameElement) {
        adminNameElement.textContent = userName;
    }
    
    // Update page title - ALL users can access database view
    const pageTitle = document.querySelector('title');
    if (pageTitle) {
        pageTitle.textContent = 'Database Dashboard - AURA';
    }
    
    // Update header text - ALL users can view database
    const headerTitle = document.querySelector('h1');
    if (headerTitle) {
        headerTitle.innerHTML = '📊 Database Dashboard';
    }
    
    // Update description - ALL users can view database records
    const headerDesc = document.querySelector('main p');
    if (headerDesc) {
        headerDesc.textContent = 'View all database records and system information for AURA Mental Health Platform';
    }
    
    console.log(`✅ Database access granted for user: ${userName} (Admin: ${isAdmin})`);
}

// Initialize admin dashboard
function initializeAdminDashboard() {
    console.log('🛠️ Initializing Admin Dashboard...');
    
    // Load initial statistics
    loadStatistics();
    
    // Load initial table (users)
    loadTable('users');
    
    // Set up event listeners
    setupEventListeners();
    
    // Load recent activity
    loadRecentActivity();
    
    console.log('✅ Admin Dashboard initialized');
}

// Set up all event listeners
function setupEventListeners() {
    // Table tab switching
    document.querySelectorAll('.table-tab').forEach(tab => {
        tab.addEventListener('click', (e) => {
            const tableName = e.target.dataset.table;
            switchTable(tableName);
        });
    });
    
    // Refresh buttons
    document.getElementById('refresh-all').addEventListener('click', refreshAll);
    document.getElementById('refresh-table').addEventListener('click', () => loadTable(currentTable));
    
    // Export button
    document.getElementById('export-table').addEventListener('click', exportCurrentTable);
    
    // Quick action buttons
    document.getElementById('backup-database').addEventListener('click', backupDatabase);
    document.getElementById('clear-old-data').addEventListener('click', clearOldData);
    document.getElementById('system-stats').addEventListener('click', showSystemStats);
    document.getElementById('manage-doctors').addEventListener('click', manageDoctors);
    document.getElementById('user-management').addEventListener('click', manageUsers);
    document.getElementById('view-logs').addEventListener('click', viewSystemLogs);
    
    // Modal close
    document.getElementById('close-modal').addEventListener('click', closeModal);
    document.getElementById('detail-modal').addEventListener('click', (e) => {
        if (e.target.id === 'detail-modal') closeModal();
    });
    
    // Retry button
    document.getElementById('retry-load').addEventListener('click', () => loadTable(currentTable));
}

// Load statistics
async function loadStatistics() {
    try {
        const token = localStorage.getItem('authToken') || localStorage.getItem('token');
        const response = await fetch('/api/admin/stats', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (response.ok) {
            const stats = await response.json();
            updateStatistics(stats);
        } else {
            // Use fallback stats
            updateStatistics({
                total_users: 0,
                total_doctors: 6,
                total_appointments: 0,
                total_chats: 0
            });
        }
    } catch (error) {
        console.error('Error loading statistics:', error);
        // Use fallback stats
        updateStatistics({
            total_users: 0,
            total_doctors: 6,
            total_appointments: 0,
            total_chats: 0
        });
    }
}

// Update statistics display
function updateStatistics(stats) {
    document.getElementById('total-users').textContent = stats.total_users || 0;
    document.getElementById('total-doctors').textContent = stats.total_doctors || 6;
    document.getElementById('total-appointments').textContent = stats.total_appointments || 0;
    document.getElementById('total-chats').textContent = stats.total_chats || 0;
}

// Switch table
function switchTable(tableName) {
    // Update active tab
    document.querySelectorAll('.table-tab').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelector(`[data-table="${tableName}"]`).classList.add('active');
    
    // Update current table
    currentTable = tableName;
    
    // Load table data
    loadTable(tableName);
}

// Load table data
async function loadTable(tableName) {
    const config = tableConfigs[tableName];
    if (!config) {
        console.error('Unknown table:', tableName);
        return;
    }
    
    // Show loading state
    showTableLoading();
    
    // Update table title
    document.getElementById('table-title').textContent = config.title;
    
    try {
        const token = localStorage.getItem('authToken') || localStorage.getItem('token');
        let data = [];
        
        // Use real API endpoints for ALL tables
        console.log(`🔄 Loading ${tableName} from ${config.endpoint}`);
        
        const response = await fetch(config.endpoint, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (response.ok) {
            const result = await response.json();
            console.log(`✅ ${tableName} response:`, result);
            
            // Extract data based on table type
            if (tableName === 'users') {
                data = result.users || [];
            } else if (tableName === 'doctors') {
                data = result.doctors || [];
            } else if (tableName === 'appointments') {
                data = result.appointments || [];
            } else if (tableName === 'chat_history') {
                data = result.chat_history || [];
            } else if (tableName === 'simple_mood_entries') {
                data = result.mood_entries || [];
            } else if (tableName === 'payments') {
                data = result.payments || [];
            } else if (tableName === 'face_emotion_detection') {
                data = result.emotions || [];
            } else if (tableName === 'emotional_intelligence_scores') {
                data = result.emotional_intelligence || [];
            } else if (tableName === 'mood_entries_advanced') {
                data = result.mood_entries_advanced || [];
            } else if (tableName === 'mood_insights') {
                data = result.mood_insights || [];
            } else if (tableName === 'mood_patterns') {
                data = result.mood_patterns || [];
            } else if (tableName === 'doctor_availability') {
                data = result.doctor_availability || [];
            } else {
                // Fallback for any other format
                data = result.data || result[tableName] || [];
            }
            
            console.log(`📊 ${tableName}: ${data.length} records loaded`);
        } else {
            console.error(`❌ Failed to fetch ${tableName}: ${response.status} ${response.statusText}`);
            
            // Show error details
            const errorText = await response.text();
            console.error('Error details:', errorText);
            
            // Use empty array as fallback
            data = [];
        }
        
        // Store data
        tableData[tableName] = data;
        
        // Render table
        renderTable(config, data);
        
        // Update count
        document.getElementById('table-count').textContent = `${data.length} records`;
        
        // Hide loading state
        hideTableLoading();
        
        // Add create button
        addCreateButton();
        
    } catch (error) {
        console.error(`❌ Error loading ${tableName}:`, error);
        showTableError();
    }
}

// Generate mock data for tables not yet implemented
function generateMockData(tableName) {
    switch (tableName) {
        case 'appointments':
            return [
                {
                    id: 'apt-001',
                    user_id: 'user-001',
                    doctor_id: 'dr-smith-001',
                    appointment_date: '2026-01-25',
                    appointment_time: '10:00',
                    status: 'scheduled',
                    payment_status: 'completed'
                }
            ];
        case 'chat_history':
            return [
                {
                    id: 'chat-001',
                    user_id: 'user-001',
                    user_message: 'I feel anxious today',
                    ai_response: 'I understand you are feeling anxious. Can you tell me more about what is causing this anxiety?',
                    sentiment: 'Negative',
                    timestamp: '2026-01-23 10:30:00'
                }
            ];
        case 'simple_mood_entries':
            return [
                {
                    id: 1,
                    user_id: 'user-001',
                    mood_rating: 3,
                    mood_notes: 'Feeling okay today',
                    timestamp: '2026-01-23 09:00:00'
                }
            ];
        case 'payments':
            return [
                {
                    id: 'pay-001',
                    user_id: 'user-001',
                    appointment_id: 'apt-001',
                    amount: 80.00,
                    payment_method: 'card',
                    status: 'completed',
                    created_at: '2026-01-23 08:00:00'
                }
            ];
        case 'face_emotion_detection':
            return [
                {
                    id: 'emo-001',
                    user_id: 'user-001',
                    detected_emotion: 'happy',
                    confidence_score: 85.5,
                    timestamp: '2026-01-23 11:00:00'
                }
            ];
        default:
            return [];
    }
}

// Render table
function renderTable(config, data) {
    const tableHeader = document.getElementById('table-header');
    const tableBody = document.getElementById('table-body');
    
    // Clear existing content
    tableHeader.innerHTML = '';
    tableBody.innerHTML = '';
    
    if (data.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="${config.columns.length + 1}" class="text-center py-8 text-gray-400">
                    No data available
                </td>
            </tr>
        `;
        return;
    }
    
    // Create header
    const headerRow = document.createElement('tr');
    config.displayNames.forEach(name => {
        const th = document.createElement('th');
        th.className = 'px-4 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider border-b border-white/10';
        th.textContent = name;
        headerRow.appendChild(th);
    });
    
    // Add actions column
    const actionsHeader = document.createElement('th');
    actionsHeader.className = 'px-4 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider border-b border-white/10';
    actionsHeader.textContent = 'Actions';
    headerRow.appendChild(actionsHeader);
    
    tableHeader.appendChild(headerRow);
    
    // Create body rows
    data.forEach(row => {
        const tr = document.createElement('tr');
        tr.className = 'border-b border-white/5 hover:bg-white/5';
        
        config.columns.forEach(column => {
            const td = document.createElement('td');
            td.className = 'px-4 py-3 text-sm text-gray-300';
            
            let value = row[column];
            
            // Format specific columns
            if (column.includes('_at') || column === 'timestamp') {
                value = value ? new Date(value).toLocaleString() : 'N/A';
            } else if (column === 'is_admin' || column === 'is_available') {
                value = value ? 'Yes' : 'No';
            } else if (column === 'price_per_session' || column === 'amount') {
                value = value ? `$${parseFloat(value).toFixed(2)}` : 'N/A';
            } else if (column === 'confidence_score') {
                value = value ? `${parseFloat(value).toFixed(1)}%` : 'N/A';
            }
            
            td.textContent = value || 'N/A';
            tr.appendChild(td);
        });
        
        // Add actions column
        const actionsTd = document.createElement('td');
        actionsTd.className = 'px-4 py-3 text-sm';
        actionsTd.innerHTML = `
            <button class="text-blue-400 hover:text-blue-300 mr-2" onclick="viewRecord('${currentTable}', '${row[config.primaryKey]}')">
                View
            </button>
            <button class="text-green-400 hover:text-green-300 mr-2" onclick="editRecord('${currentTable}', '${row[config.primaryKey]}')">
                Edit
            </button>
            <button class="text-red-400 hover:text-red-300" onclick="deleteRecord('${currentTable}', '${row[config.primaryKey]}')">
                Delete
            </button>
        `;
        tr.appendChild(actionsTd);
        
        tableBody.appendChild(tr);
    });
}

// Show table loading state
function showTableLoading() {
    document.getElementById('table-loading').style.display = 'block';
    document.getElementById('table-error').style.display = 'none';
    document.getElementById('data-table').style.display = 'none';
}

// Hide table loading state
function hideTableLoading() {
    document.getElementById('table-loading').style.display = 'none';
    document.getElementById('table-error').style.display = 'none';
    document.getElementById('data-table').style.display = 'table';
}

// Show table error state
function showTableError() {
    document.getElementById('table-loading').style.display = 'none';
    document.getElementById('table-error').style.display = 'block';
    document.getElementById('data-table').style.display = 'none';
}

// Record actions
function viewRecord(tableName, recordId) {
    const data = tableData[tableName];
    const config = tableConfigs[tableName];
    const record = data.find(r => r[config.primaryKey] === recordId);
    
    if (!record) {
        alert('Record not found');
        return;
    }
    
    // Show modal with record details
    const modal = document.getElementById('detail-modal');
    const modalTitle = document.getElementById('modal-title');
    const modalContent = document.getElementById('modal-content');
    
    modalTitle.textContent = `${config.title} - Record Details`;
    
    let content = '<div class="space-y-4">';
    config.columns.forEach((column, index) => {
        const displayName = config.displayNames[index];
        let value = record[column];
        
        // Format value
        if (column.includes('_at') || column === 'timestamp') {
            value = value ? new Date(value).toLocaleString() : 'N/A';
        } else if (column === 'is_admin' || column === 'is_available') {
            value = value ? 'Yes' : 'No';
        } else if (column === 'price_per_session' || column === 'amount') {
            value = value ? `$${parseFloat(value).toFixed(2)}` : 'N/A';
        } else if (column === 'confidence_score') {
            value = value ? `${parseFloat(value).toFixed(1)}%` : 'N/A';
        }
        
        content += `
            <div class="flex justify-between">
                <span class="font-semibold text-gray-300">${displayName}:</span>
                <span class="text-white">${value || 'N/A'}</span>
            </div>
        `;
    });
    content += '</div>';
    
    modalContent.innerHTML = content;
    modal.classList.remove('hidden');
}

function editRecord(tableName, recordId) {
    const data = tableData[tableName];
    const config = tableConfigs[tableName];
    const record = data.find(r => r[config.primaryKey] === recordId);
    
    if (!record) {
        alert('Record not found');
        return;
    }
    
    // Show edit modal
    showEditModal(tableName, record);
}

function deleteRecord(tableName, recordId) {
    if (!confirm(`Are you sure you want to delete this ${tableName} record? This action cannot be undone.`)) {
        return;
    }
    
    const config = tableConfigs[tableName];
    const token = localStorage.getItem('authToken') || localStorage.getItem('token');
    
    // Show loading
    const deleteBtn = event.target;
    const originalText = deleteBtn.textContent;
    deleteBtn.textContent = 'Deleting...';
    deleteBtn.disabled = true;
    
    fetch(`${config.endpoint}/${recordId}`, {
        method: 'DELETE',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            alert('Record deleted successfully!');
            loadTable(tableName); // Reload table
            loadStatistics(); // Refresh stats
        } else {
            alert(`Error deleting record: ${result.error || 'Unknown error'}`);
        }
    })
    .catch(error => {
        console.error('Delete error:', error);
        alert('Error deleting record. Please try again.');
    })
    .finally(() => {
        deleteBtn.textContent = originalText;
        deleteBtn.disabled = false;
    });
}

function showEditModal(tableName, record = null) {
    const config = tableConfigs[tableName];
    const modal = document.getElementById('detail-modal');
    const modalTitle = document.getElementById('modal-title');
    const modalContent = document.getElementById('modal-content');
    
    const isEdit = record !== null;
    modalTitle.textContent = `${isEdit ? 'Edit' : 'Create'} ${config.title.replace(/^[^\\s]+ /, '')}`;
    
    let formHtml = `<form id="crud-form" class="space-y-4">`;
    
    config.columns.forEach((column, index) => {
        const displayName = config.displayNames[index];
        const value = record ? (record[column] || '') : '';
        
        // Skip ID field for create, make it readonly for edit
        if (column === config.primaryKey) {
            if (isEdit) {
                formHtml += `
                    <div>
                        <label class="block text-gray-300 text-sm font-bold mb-2">${displayName}:</label>
                        <input type="text" name="${column}" value="${value}" readonly 
                               class="w-full px-3 py-2 bg-gray-700 text-white rounded border border-gray-600">
                    </div>
                `;
            }
            return;
        }
        
        // Special handling for different field types
        if (column === 'is_admin' || column === 'is_available') {
            formHtml += `
                <div>
                    <label class="block text-gray-300 text-sm font-bold mb-2">${displayName}:</label>
                    <select name="${column}" class="w-full px-3 py-2 bg-gray-700 text-white rounded border border-gray-600">
                        <option value="0" ${value == 0 ? 'selected' : ''}>No</option>
                        <option value="1" ${value == 1 ? 'selected' : ''}>Yes</option>
                    </select>
                </div>
            `;
        } else if (column === 'password' && !isEdit) {
            formHtml += `
                <div>
                    <label class="block text-gray-300 text-sm font-bold mb-2">${displayName}:</label>
                    <input type="password" name="${column}" value="defaultpass123" required
                           class="w-full px-3 py-2 bg-gray-700 text-white rounded border border-gray-600">
                </div>
            `;
        } else if (column.includes('_at') || column === 'timestamp') {
            // Skip timestamp fields - they're auto-generated
            return;
        } else {
            const required = ['name', 'email'].includes(column) ? 'required' : '';
            formHtml += `
                <div>
                    <label class="block text-gray-300 text-sm font-bold mb-2">${displayName}:</label>
                    <input type="text" name="${column}" value="${value}" ${required}
                           class="w-full px-3 py-2 bg-gray-700 text-white rounded border border-gray-600">
                </div>
            `;
        }
    });
    
    formHtml += `
        <div class="flex space-x-4 pt-4">
            <button type="submit" class="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded">
                ${isEdit ? 'Update' : 'Create'}
            </button>
            <button type="button" onclick="closeModal()" class="bg-gray-500 hover:bg-gray-600 text-white px-6 py-2 rounded">
                Cancel
            </button>
        </div>
    </form>`;
    
    modalContent.innerHTML = formHtml;
    modal.classList.remove('hidden');
    
    // Handle form submission
    document.getElementById('crud-form').addEventListener('submit', (e) => {
        e.preventDefault();
        submitCrudForm(tableName, isEdit);
    });
}

function submitCrudForm(tableName, isEdit) {
    const form = document.getElementById('crud-form');
    const formData = new FormData(form);
    const data = {};
    
    // Convert FormData to object
    for (let [key, value] of formData.entries()) {
        // Convert numeric fields
        if (['is_admin', 'is_available'].includes(key)) {
            data[key] = parseInt(value);
        } else {
            data[key] = value;
        }
    }
    
    const config = tableConfigs[tableName];
    const token = localStorage.getItem('authToken') || localStorage.getItem('token');
    
    let url = config.endpoint;
    let method = 'POST';
    
    if (isEdit) {
        const recordId = data[config.primaryKey];
        url += `/${recordId}`;
        method = 'PUT';
        // Remove ID from data for update
        delete data[config.primaryKey];
    }
    
    // Show loading
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = isEdit ? 'Updating...' : 'Creating...';
    submitBtn.disabled = true;
    
    fetch(url, {
        method: method,
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            alert(`Record ${isEdit ? 'updated' : 'created'} successfully!`);
            closeModal();
            loadTable(tableName); // Reload table
            loadStatistics(); // Refresh stats
        } else {
            alert(`Error ${isEdit ? 'updating' : 'creating'} record: ${result.error || 'Unknown error'}`);
        }
    })
    .catch(error => {
        console.error('CRUD error:', error);
        alert(`Error ${isEdit ? 'updating' : 'creating'} record. Please try again.`);
    })
    .finally(() => {
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    });
}

// Close modal
function closeModal() {
    document.getElementById('detail-modal').classList.add('hidden');
}

// Export current table
function exportCurrentTable() {
    const data = tableData[currentTable];
    const config = tableConfigs[currentTable];
    
    if (!data || data.length === 0) {
        alert('No data to export');
        return;
    }
    
    // Convert to CSV
    const headers = config.displayNames.join(',');
    const rows = data.map(row => {
        return config.columns.map(column => {
            let value = row[column] || '';
            // Escape commas and quotes
            if (typeof value === 'string' && (value.includes(',') || value.includes('"'))) {
                value = `"${value.replace(/"/g, '""')}"`;
            }
            return value;
        }).join(',');
    });
    
    const csv = [headers, ...rows].join('\n');
    
    // Download CSV
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${currentTable}_export_${new Date().toISOString().split('T')[0]}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
    
    alert('Table exported successfully!');
}

// Refresh all data
function refreshAll() {
    const refreshBtn = document.getElementById('refresh-all');
    refreshBtn.classList.remove('stopped');
    
    // Refresh statistics
    loadStatistics();
    
    // Refresh current table
    loadTable(currentTable);
    
    // Refresh recent activity
    loadRecentActivity();
    
    setTimeout(() => {
        refreshBtn.classList.add('stopped');
    }, 2000);
}

// Load recent activity
async function loadRecentActivity() {
    try {
        // Load recent users
        const recentUsersDiv = document.getElementById('recent-users');
        recentUsersDiv.innerHTML = `
            <div class="flex items-center space-x-3 p-3 bg-white/5 rounded-lg">
                <div class="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center text-white text-sm font-bold">
                    U
                </div>
                <div>
                    <div class="text-white font-medium">New User</div>
                    <div class="text-gray-400 text-sm">Joined recently</div>
                </div>
            </div>
        `;
        
        // Load recent appointments
        const recentAppointmentsDiv = document.getElementById('recent-appointments');
        recentAppointmentsDiv.innerHTML = `
            <div class="flex items-center space-x-3 p-3 bg-white/5 rounded-lg">
                <div class="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center text-white text-sm font-bold">
                    A
                </div>
                <div>
                    <div class="text-white font-medium">Upcoming Appointment</div>
                    <div class="text-gray-400 text-sm">Dr. Smith - Tomorrow 10:00 AM</div>
                </div>
            </div>
        `;
        
    } catch (error) {
        console.error('Error loading recent activity:', error);
    }
}

// Quick action functions
function backupDatabase() {
    alert('Database backup functionality will be implemented in future updates.');
}

function clearOldData() {
    if (confirm('Are you sure you want to clear old data? This action cannot be undone.')) {
        alert('Clear old data functionality will be implemented in future updates.');
    }
}

function showSystemStats() {
    alert('System statistics functionality will be implemented in future updates.');
}

function manageDoctors() {
    switchTable('doctors');
}

function manageUsers() {
    switchTable('users');
}

function viewSystemLogs() {
    alert('System logs functionality will be implemented in future updates.');
}

// Add Create button functionality
function addCreateButton() {
    const tableContent = document.getElementById('table-content');
    const tableHeader = tableContent.querySelector('.flex.justify-between.items-center.mb-4');
    
    // Add Create button if not already present
    if (!document.getElementById('create-record-btn')) {
        const createBtn = document.createElement('button');
        createBtn.id = 'create-record-btn';
        createBtn.className = 'bg-green-500 hover:bg-green-600 text-white px-3 py-1 rounded text-sm mr-2';
        createBtn.innerHTML = '➕ Create New';
        createBtn.onclick = () => showEditModal(currentTable, null);
        
        const buttonContainer = tableHeader.querySelector('.flex.space-x-2');
        buttonContainer.insertBefore(createBtn, buttonContainer.firstChild);
    }
}
