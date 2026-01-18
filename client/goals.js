document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const goalInput = document.getElementById('goal-input');
    const addGoalBtn = document.getElementById('add-goal-btn');
    const goalList = document.getElementById('goal-list');

    const habitInput = document.getElementById('habit-input');
    const addHabitBtn = document.getElementById('add-habit-btn');
    const habitList = document.getElementById('habit-list');

    const suggestionBox = document.getElementById('suggestion-box');

    // --- API Endpoints ---
    const GOALS_API = '/api/goals';
    const HABITS_API = '/api/habits';
    const SUGGESTIONS_API = '/api/goal_suggestions';

    // --- Functions ---

    /**
     * Fetches and renders the user's goals and habits.
     */
    const loadTracker = async () => {
        try {
            // Fetch Goals
            const goalsRes = await fetch(GOALS_API);
            const { goals } = await goalsRes.json();
            renderList(goalList, goals, 'goal');

            // Fetch Habits
            const habitsRes = await fetch(HABITS_API);
            const { habits } = await habitsRes.json();
            renderList(habitList, habits, 'habit');

        } catch (error) {
            console.error("Error loading tracker data:", error);
        }
    };

    /**
     * Renders a list of items (goals or habits).
     * @param {HTMLElement} listElement - The UL element to render into.
     * @param {Array} items - The array of items to render.
     * @param {String} type - 'goal' or 'habit'.
     */
    const renderList = (listElement, items, type) => {
        listElement.innerHTML = ''; // Clear existing list
        if (!items || items.length === 0) {
            listElement.innerHTML = `<li class="text-gray-500 italic">No ${type}s added yet.</li>`;
            return;
        }

        items.forEach(item => {
            const li = document.createElement('li');
            li.className = `flex justify-between items-center p-3 rounded-lg ${item.completed ? 'bg-gray-200 text-gray-500 line-through' : 'bg-white'}`;
            li.dataset.id = item.id;

            li.innerHTML = `
                <span>${item.text}</span>
                <div>
                    <button class="complete-btn text-green-500 hover:text-green-700 mr-2">&#10004;</button>
                    <button class="delete-btn text-red-500 hover:text-red-700">&#10006;</button>
                </div>
            `;
            listElement.appendChild(li);
        });
    };

    /**
     * Adds a new item (goal or habit).
     * @param {String} text - The text of the item.
     * @param {String} type - 'goal' or 'habit'.
     */
    const addItem = async (text, type) => {
        if (!text) return;
        
        const API = type === 'goal' ? GOALS_API : HABITS_API;

        try {
            await fetch(API, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text }),
            });
            loadTracker(); // Reload the lists
        } catch (error) {
            console.error(`Error adding ${type}:`, error);
        }
    };

    /**
     * Handles clicks on the complete or delete buttons.
     */
    const handleItemClick = async (e, type) => {
        const target = e.target;
        const li = target.closest('li');
        if (!li) return;

        const id = li.dataset.id;
        const API = type === 'goal' ? GOALS_API : HABITS_API;

        if (target.classList.contains('complete-btn')) {
            try {
                await fetch(`${API}/${id}`, { method: 'PUT' });
                loadTracker();
            } catch (error) {
                console.error(`Error completing ${type}:`, error);
            }
        } else if (target.classList.contains('delete-btn')) {
            try {
                await fetch(`${API}/${id}`, { method: 'DELETE' });
                loadTracker();
            } catch (error) {
                console.error(`Error deleting ${type}:`, error);
            }
        }
    };

    /**
     * Fetches and displays AI-powered goal suggestions.
     */
    const loadSuggestions = async () => {
        try {
            const res = await fetch(SUGGESTIONS_API);
            const { suggestions } = await res.json();

            suggestionBox.innerHTML = '';
            if (suggestions && suggestions.length > 0) {
                suggestions.forEach(suggestion => {
                    const suggestionEl = document.createElement('div');
                    suggestionEl.className = 'p-3 bg-indigo-200 rounded-lg mb-2 flex justify-between items-center';
                    suggestionEl.innerHTML = `
                        <span class="text-indigo-900">${suggestion}</span>
                        <button class="add-suggestion-btn bg-indigo-500 text-white px-3 py-1 rounded-md hover:bg-indigo-600">Add as Goal</button>
                    `;
                    suggestionBox.appendChild(suggestionEl);
                });
            } else {
                suggestionBox.innerHTML = '<p class="text-indigo-800">No new suggestions right now. Keep chatting with your AI therapist to get personalized recommendations!</p>';
            }
        } catch (error) {
            console.error("Error loading suggestions:", error);
        }
    };

    // --- Event Listeners ---
    addGoalBtn.addEventListener('click', () => {
        addItem(goalInput.value, 'goal');
        goalInput.value = '';
    });

    addHabitBtn.addEventListener('click', () => {
        addItem(habitInput.value, 'habit');
        habitInput.value = '';
    });

    goalList.addEventListener('click', (e) => handleItemClick(e, 'goal'));
    habitList.addEventListener('click', (e) => handleItemClick(e, 'habit'));

    suggestionBox.addEventListener('click', (e) => {
        if (e.target.classList.contains('add-suggestion-btn')) {
            const suggestionText = e.target.previousElementSibling.textContent;
            addItem(suggestionText, 'goal');
        }
    });


    // --- Initial Load ---
    loadTracker();
    loadSuggestions();
});