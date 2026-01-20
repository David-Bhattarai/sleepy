document.addEventListener('DOMContentLoaded', () => {
    const userListDiv = document.getElementById('user-list');
    const chatHistorySection = document.getElementById('chat-history-section');
    const selectedUserNameSpan = document.getElementById('selected-user-name');
    const chatHistoryContainer = document.getElementById('chat-history-container');

    const token = localStorage.getItem('token');

    // Fetch all users (Admin only)
    const fetchUsers = async () => {
        if (!token) {
            userListDiv.innerHTML = '<p class="text-red-500">Access Denied. Please log in as an admin.</p>';
            return;
        }

        try {
            const response = await fetch('/api/admin/users', {
                headers: { 'Authorization': `Bearer ${token}` }
            });

            if (!response.ok) {
                userListDiv.innerHTML = '<p class="text-red-500">Could not fetch users. You may not have admin rights.</p>';
                return;
            }

            const users = await response.json();
            renderUserTable(users);

        } catch (error) {
            console.error('Error fetching users:', error);
            userListDiv.innerHTML = '<p class="text-red-500">An error occurred.</p>';
        }
    };

    // Render the table of users
    const renderUserTable = (users) => {
        if (users.length === 0) {
            userListDiv.innerHTML = '<p>No users found.</p>';
            return;
        }

        const table = document.createElement('table');
        table.className = 'min-w-full divide-y divide-gray-200';
        table.innerHTML = `
            <thead class="bg-gray-50">
                <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Is Admin</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
                ${users.map(user => `
                    <tr>
                        <td class="px-6 py-4 whitespace-nowrap">${user.name}</td>
                        <td class="px-6 py-4 whitespace-nowrap">${user.email}</td>
                        <td class="px-6 py-4 whitespace-nowrap">${user.is_admin ? 'Yes' : 'No'}</td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <button class="view-chat-btn text-blue-600 hover:underline" data-user-id="${user.id}" data-user-name="${user.name}">View Chat</button>
                        </td>
                    </tr>
                `).join('')}
            </tbody>
        `;

        userListDiv.innerHTML = '';
        userListDiv.appendChild(table);

        // Add event listeners to 'View Chat' buttons
        document.querySelectorAll('.view-chat-btn').forEach(button => {
            button.addEventListener('click', handleViewChat);
        });
    };

    // Handle clicking the 'View Chat' button
    const handleViewChat = async (event) => {
        const userId = event.target.dataset.userId;
        const userName = event.target.dataset.userName;

        selectedUserNameSpan.textContent = userName;
        chatHistorySection.classList.remove('hidden');
        chatHistoryContainer.innerHTML = '<p>Loading chat history...</p>';

        try {
            const response = await fetch(`/api/admin/chat_history/${userId}` , {
                 headers: { 'Authorization': `Bearer ${token}` }
            });

            if (!response.ok) {
                chatHistoryContainer.innerHTML = '<p class="text-red-500">Could not fetch chat history.</p>';
                return;
            }

            const history = await response.json();
            renderChatHistory(history);

        } catch (error) {
            console.error('Error fetching chat history:', error);
            chatHistoryContainer.innerHTML = '<p class="text-red-500">An error occurred.</p>';
        }
    };

    // Render the chat history for a selected user
    const renderChatHistory = (history) => {
        if (history.length === 0) {
            chatHistoryContainer.innerHTML = '<p>No chat history found for this user.</p>';
            return;
        }

        chatHistoryContainer.innerHTML = history.map(entry => `
            <div class="mb-3">
                <p class="font-bold text-gray-700">You:</p>
                <p class="bg-blue-100 rounded-lg p-2">${entry.user_message}</p>
            </div>
            <div class="mb-3">
                <p class="font-bold text-blue-600">AI Therapist:</p>
                <p class="bg-gray-200 rounded-lg p-2">${entry.ai_response}</p>
                <p class="text-xs text-gray-500 text-right">${new Date(entry.timestamp).toLocaleString()}</p>
            </div>
        `).join('');
    };

    // Initial fetch
    fetchUsers();
});
