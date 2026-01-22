/**
 * Yaoundé Multilingual Expression Analyzer
 * Frontend JavaScript Application
 * ICT University - Compiler Construction Project
 */

// ==================== INITIALIZATION ====================
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

let typeChart = null;
let frequencyChart = null;
let currentAnalysis = null;
let allExamples = [];
let soundEnabled = true;
let autoSaveTimer = null;
let compareResultA = null;
let compareResultB = null;
let recognition = null;

function initializeApp() {
    // Load initial data
    loadExamples();
    loadGrammar();

    // Set up event listeners
    setupEventListeners();
    setupKeyboardShortcuts();

    // Initialize theme
    initializeTheme();

    // Initialize sound setting
    initializeSoundSetting();

    // Initialize voice recognition
    initializeVoiceRecognition();
    
    // Setup voice suggestions
    setupVoiceSuggestions();

    // Initialize auto-save
    initializeAutoSave();

    // Restore saved input
    restoreAutoSave();

    // Show welcome toast
    showToast('Welcome to Yaoundé Analyzer! 🇨🇲', 'success');
}

// ==================== EVENT LISTENERS ====================
function setupEventListeners() {
    // Input events
    const input = document.getElementById('expression-input');
    input.addEventListener('input', handleInputChange);
    input.addEventListener('keydown', handleInputKeydown);

    // Button events
    document.getElementById('btn-analyze').addEventListener('click', fullAnalysis);
    document.getElementById('btn-tokenize').addEventListener('click', tokenizeOnly);
    document.getElementById('btn-parse').addEventListener('click', parseOnly);
    document.getElementById('btn-clear').addEventListener('click', clearAll);
    document.getElementById('btn-export').addEventListener('click', exportResults);
    document.getElementById('btn-export-pdf').addEventListener('click', exportToPDF);
    document.getElementById('btn-upload').addEventListener('click', () => {
        document.getElementById('file-input').click();
    });
    document.getElementById('file-input').addEventListener('change', handleFileUpload);

    // Voice input
    document.getElementById('btn-voice').addEventListener('click', toggleVoiceInput);

    // Tab navigation
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => switchTab(btn.dataset.tab));
    });

    // Theme toggle
    document.getElementById('theme-toggle').addEventListener('click', toggleTheme);

    // Sound toggle
    document.getElementById('sound-toggle').addEventListener('click', toggleSound);

    // Compare toggle
    document.getElementById('compare-toggle').addEventListener('click', () => {
        document.getElementById('compare-modal').classList.add('open');
    });
    document.getElementById('close-compare').addEventListener('click', () => {
        document.getElementById('compare-modal').classList.remove('open');
    });

    // Compare analyze buttons
    document.getElementById('compare-analyze-a').addEventListener('click', () => analyzeForCompare('a'));
    document.getElementById('compare-analyze-b').addEventListener('click', () => analyzeForCompare('b'));

    // History sidebar
    document.getElementById('history-toggle').addEventListener('click', toggleHistory);
    document.getElementById('close-history').addEventListener('click', toggleHistory);
    document.getElementById('clear-history').addEventListener('click', clearHistory);

    // Shortcuts modal
    document.getElementById('shortcuts-btn').addEventListener('click', () => {
        document.getElementById('shortcuts-modal').classList.add('open');
    });
    document.getElementById('close-shortcuts').addEventListener('click', () => {
        document.getElementById('shortcuts-modal').classList.remove('open');
    });

    // Batch modal
    document.getElementById('close-batch-modal').addEventListener('click', () => {
        document.getElementById('batch-modal').classList.remove('open');
    });

    // Example category filter
    document.getElementById('example-category').addEventListener('change', filterExamples);

    // Close modals on escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            document.querySelectorAll('.modal.open').forEach(m => m.classList.remove('open'));
            document.getElementById('history-sidebar').classList.remove('open');
        }
    });

    // Close modals on backdrop click
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.classList.remove('open');
            }
        });
    });
}

function setupKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
        // Ctrl + Enter = Full Analysis
        if (e.ctrlKey && e.key === 'Enter') {
            e.preventDefault();
            fullAnalysis();
        }
        // Ctrl + T = Tokenize
        if (e.ctrlKey && e.key === 't') {
            e.preventDefault();
            tokenizeOnly();
        }
        // Ctrl + P = Parse (prevent print)
        if (e.ctrlKey && e.key === 'p') {
            e.preventDefault();
            parseOnly();
        }
        // Ctrl + D = Dark mode
        if (e.ctrlKey && e.key === 'd') {
            e.preventDefault();
            toggleTheme();
        }
        // Ctrl + H = History
        if (e.ctrlKey && e.key === 'h') {
            e.preventDefault();
            toggleHistory();
        }
        // Ctrl + L = Clear
        if (e.ctrlKey && e.key === 'l') {
            e.preventDefault();
            clearAll();
        }
        // Ctrl + S = Export
        if (e.ctrlKey && e.key === 's') {
            e.preventDefault();
            exportResults();
        }
    });
}

// ==================== INPUT HANDLING ====================
function handleInputChange() {
    const input = document.getElementById('expression-input');
    const text = input.value;

    // Update character count
    document.getElementById('char-count').textContent = text.length;

    // Update status
    if (text.trim()) {
        updateStatus('Ready to analyze', '#f39c12');
    } else {
        updateStatus('Enter an expression', '#95a5a6');
    }

    // Trigger auto-save
    triggerAutoSave();
}

function handleInputKeydown(e) {
    // Tab inserts spaces instead of changing focus
    if (e.key === 'Tab') {
        e.preventDefault();
        const input = e.target;
        const start = input.selectionStart;
        const end = input.selectionEnd;
        input.value = input.value.substring(0, start) + '  ' + input.value.substring(end);
        input.selectionStart = input.selectionEnd = start + 2;
    }
}

// ==================== ANALYSIS FUNCTIONS ====================
async function fullAnalysis() {
    const expression = document.getElementById('expression-input').value.trim();

    if (!expression) {
        showToast('Please enter an expression first', 'warning');
        return;
    }

    updateStatus('Analyzing...', '#3498db');

    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ expression })
        });

        const data = await response.json();

        if (data.error) {
            showToast('Error: ' + data.error, 'error');
            updateStatus('Error occurred', '#e74c3c');
            return;
        }

        currentAnalysis = data;

        // Update all displays
        displayTokens(data.tokens);
        displayParseResult(data);
        displayStatistics(data);
        displayLanguages(data.languages_detected);
        updateResultStatus(data.accepted);

        // Update history
        loadHistory();

        // Show success toast
        if (data.accepted) {
            showToast('✓ Expression accepted!', 'success');
            updateStatus('✓ Valid expression', '#27ae60');
            playSound('success');
        } else {
            showToast('✗ Expression rejected', 'error');
            updateStatus('✗ Invalid expression', '#e74c3c');
            playSound('error');
        }

    } catch (error) {
        console.error('Analysis error:', error);
        showToast('Network error occurred', 'error');
        updateStatus('Connection error', '#e74c3c');
    }
}

async function tokenizeOnly() {
    const expression = document.getElementById('expression-input').value.trim();

    if (!expression) {
        showToast('Please enter an expression first', 'warning');
        return;
    }

    updateStatus('Tokenizing...', '#3498db');

    try {
        const response = await fetch('/api/tokenize', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ expression })
        });

        const data = await response.json();

        if (data.error) {
            showToast('Error: ' + data.error, 'error');
            return;
        }

        displayTokens(data.tokens);
        displayStatistics(data);
        if (data.languages_detected) {
            displayLanguages(data.languages_detected);
        }
        switchTab('tokens');

        showToast(`Found ${data.token_count} tokens`, 'success');
        updateStatus(`${data.token_count} tokens found`, '#27ae60');

    } catch (error) {
        console.error('Tokenize error:', error);
        showToast('Error tokenizing expression', 'error');
    }
}

async function parseOnly() {
    const expression = document.getElementById('expression-input').value.trim();

    if (!expression) {
        showToast('Please enter an expression first', 'warning');
        return;
    }

    updateStatus('Parsing...', '#3498db');

    try {
        const response = await fetch('/api/parse', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ expression })
        });

        const data = await response.json();

        if (data.error) {
            showToast('Error: ' + data.error, 'error');
            return;
        }

        displayParseResult(data);
        updateResultStatus(data.accepted);
        if (data.languages_detected) {
            displayLanguages(data.languages_detected);
        }
        switchTab('parse');

        if (data.accepted) {
            showToast('✓ Parse successful!', 'success');
            updateStatus('✓ Valid syntax', '#27ae60');
        } else {
            showToast('✗ Parse failed', 'error');
            updateStatus('✗ Invalid syntax', '#e74c3c');
        }

    } catch (error) {
        console.error('Parse error:', error);
        showToast('Error parsing expression', 'error');
    }
}

// ==================== FILE UPLOAD ====================
async function handleFileUpload(e) {
    const file = e.target.files[0];
    if (!file) return;

    if (!file.name.endsWith('.txt')) {
        showToast('Please upload a .txt file', 'warning');
        return;
    }

    updateStatus('Processing file...', '#3498db');

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/api/analyze-batch', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.error) {
            showToast('Error: ' + data.error, 'error');
            return;
        }

        displayBatchResults(data);
        document.getElementById('batch-modal').classList.add('open');

        showToast(`Analyzed ${data.statistics.total_expressions} expressions`, 'success');
        updateStatus('Batch complete', '#27ae60');

    } catch (error) {
        console.error('Batch error:', error);
        showToast('Error processing file', 'error');
    }

    // Reset file input
    e.target.value = '';
}

function displayBatchResults(data) {
    const stats = data.statistics;

    // Display aggregate statistics
    const statsHtml = `
        <div class="batch-stat">
            <div class="batch-stat-value">${stats.total_expressions}</div>
            <div class="batch-stat-label">Total Expressions</div>
        </div>
        <div class="batch-stat">
            <div class="batch-stat-value" style="color: #27ae60">${stats.accepted}</div>
            <div class="batch-stat-label">Accepted</div>
        </div>
        <div class="batch-stat">
            <div class="batch-stat-value" style="color: #e74c3c">${stats.rejected}</div>
            <div class="batch-stat-label">Rejected</div>
        </div>
        <div class="batch-stat">
            <div class="batch-stat-value">${stats.acceptance_rate}%</div>
            <div class="batch-stat-label">Success Rate</div>
        </div>
    `;
    document.getElementById('batch-stats').innerHTML = statsHtml;

    // Display individual results
    const resultsHtml = data.results.map((r, i) => `
        <div class="batch-result-item ${r.accepted ? 'accepted' : 'rejected'}">
            <div>
                <span style="color: var(--text-muted); margin-right: 8px;">${i + 1}.</span>
                <span>${r.expression}</span>
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 0.8rem; color: var(--text-muted);">${r.token_count} tokens</span>
                <span style="font-size: 1.2rem;">${r.accepted ? '✓' : '✗'}</span>
            </div>
        </div>
    `).join('');
    document.getElementById('batch-results').innerHTML = resultsHtml;
}

// ==================== DISPLAY FUNCTIONS ====================
function displayTokens(tokens) {
    const container = document.getElementById('tokens-container');

    if (!tokens || tokens.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">🔤</div>
                <p>No tokens to display</p>
            </div>
        `;
        return;
    }

    const tokensHtml = tokens.map((token, i) => `
        <div class="token-item ${token.category}" style="animation-delay: ${i * 0.05}s">
            <span class="token-index">${i + 1}</span>
            <span class="token-type">${token.type}</span>
            <span class="token-arrow">→</span>
            <span class="token-value">'${escapeHtml(token.value)}'</span>
        </div>
    `).join('');

    container.innerHTML = tokensHtml;

    // Update badge
    document.getElementById('token-count-badge').textContent = tokens.length;
}

function displayParseResult(data) {
    const statusCard = document.getElementById('parse-status-card');
    const treeContainer = document.getElementById('parse-tree-container');

    // Update status card
    statusCard.className = 'parse-status-card ' + (data.accepted ? 'accepted' : 'rejected');
    statusCard.innerHTML = `
        <div class="status-icon">${data.accepted ? '✅' : '❌'}</div>
        <div class="status-message">${data.parse_result}</div>
    `;

    // Display parse tree
    if (data.parse_tree && data.parse_tree.length > 0) {
        const treeHtml = data.parse_tree.map((step, i) => `
            <div class="parse-step" style="animation-delay: ${i * 0.03}s">
                <span class="parse-step-number">${i + 1}.</span>
                <span>${escapeHtml(step)}</span>
            </div>
        `).join('');
        treeContainer.innerHTML = treeHtml;
    } else {
        treeContainer.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">🌳</div>
                <p>No parse steps available</p>
            </div>
        `;
    }
}

function displayStatistics(data) {
    const stats = data.statistics || {};

    // Update stat cards
    document.getElementById('stat-total').textContent = stats.total_count || 0;
    document.getElementById('stat-unique').textContent = stats.unique_count || 0;

    if (data.accepted !== undefined) {
        document.getElementById('stat-accepted').textContent = data.accepted ? '✓ Yes' : '✗ No';
        document.getElementById('stat-accepted').style.color = data.accepted ? '#27ae60' : '#e74c3c';
    }

    if (data.languages_detected) {
        document.getElementById('stat-languages').textContent = data.languages_detected.length;
    }

    // Update charts
    updateCharts(stats);
}

function displayLanguages(languages) {
    const section = document.getElementById('languages-section');
    const tagsContainer = document.getElementById('language-tags');

    if (!languages || languages.length === 0) {
        section.style.display = 'none';
        return;
    }

    section.style.display = 'block';
    tagsContainer.innerHTML = languages.map(lang =>
        `<span class="language-tag">${lang}</span>`
    ).join('');
}

function updateCharts(stats) {
    const byCategory = stats.by_category || {};
    const topTokens = stats.top_tokens || [];

    // Destroy existing charts if they exist
    if (typeChart) typeChart.destroy();
    if (frequencyChart) frequencyChart.destroy();

    // Type distribution chart (doughnut)
    const typeCtx = document.getElementById('type-chart');
    if (typeCtx && Object.keys(byCategory).length > 0) {
        const colors = [
            '#8e44ad', '#e67e22', '#c0392b', '#2980b9',
            '#27ae60', '#16a085', '#f39c12', '#7f8c8d'
        ];

        typeChart = new Chart(typeCtx, {
            type: 'doughnut',
            data: {
                labels: Object.keys(byCategory),
                datasets: [{
                    data: Object.values(byCategory),
                    backgroundColor: colors.slice(0, Object.keys(byCategory).length),
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            font: { family: 'Inter', size: 11 },
                            padding: 15
                        }
                    }
                }
            }
        });
    }

    // Frequency chart (bar)
    const freqCtx = document.getElementById('frequency-chart');
    if (freqCtx && topTokens.length > 0) {
        frequencyChart = new Chart(freqCtx, {
            type: 'bar',
            data: {
                labels: topTokens.map(t => t.token),
                datasets: [{
                    label: 'Frequency',
                    data: topTokens.map(t => t.count),
                    backgroundColor: '#c9a227',
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                indexAxis: 'y',
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        ticks: { stepSize: 1 }
                    }
                }
            }
        });
    }
}

function updateResultStatus(accepted) {
    const badge = document.querySelector('.status-badge');
    if (accepted) {
        badge.className = 'status-badge accepted';
        badge.textContent = '✓ Accepted';
    } else {
        badge.className = 'status-badge rejected';
        badge.textContent = '✗ Rejected';
    }
}

// ==================== GRAMMAR LOADING ====================
async function loadGrammar() {
    try {
        const response = await fetch('/api/grammar');
        const data = await response.json();

        // Display rules
        const rulesHtml = Object.entries(data.rules).map(([lhs, productions]) => `
            <div class="rule-item">
                <span class="rule-lhs">${lhs}</span>
                <span class="rule-arrow">→</span>
                <span class="rule-rhs">${productions.join(' | ')}</span>
            </div>
        `).join('');
        document.getElementById('rules-list').innerHTML = rulesHtml;

        // Display FIRST sets
        const firstHtml = Object.entries(data.first_sets).map(([nt, set]) => `
            <div class="rule-item">
                <span class="rule-lhs">FIRST(${nt})</span>
                <span class="rule-arrow">=</span>
                <span class="rule-rhs">{ ${set.join(', ')} }</span>
            </div>
        `).join('');
        document.getElementById('first-sets').innerHTML = firstHtml;

        // Display FOLLOW sets
        const followHtml = Object.entries(data.follow_sets).map(([nt, set]) => `
            <div class="rule-item">
                <span class="rule-lhs">FOLLOW(${nt})</span>
                <span class="rule-arrow">=</span>
                <span class="rule-rhs">{ ${set.join(', ')} }</span>
            </div>
        `).join('');
        document.getElementById('follow-sets').innerHTML = followHtml;

    } catch (error) {
        console.error('Error loading grammar:', error);
    }
}

// ==================== EXAMPLES ====================
async function loadExamples() {
    try {
        const response = await fetch('/api/examples');
        const data = await response.json();
        allExamples = data.examples;
        displayExamples(allExamples);
    } catch (error) {
        console.error('Error loading examples:', error);
    }
}

function displayExamples(examples) {
    const list = document.getElementById('examples-list');
    list.innerHTML = examples.map(ex => `
        <li onclick="loadExample('${escapeHtml(ex.text)}')">
            <span>${ex.text}</span>
            <span class="example-category-badge">${ex.category}</span>
        </li>
    `).join('');
}

function filterExamples() {
    const category = document.getElementById('example-category').value;
    if (category === 'all') {
        displayExamples(allExamples);
    } else {
        const filtered = allExamples.filter(ex => ex.category === category);
        displayExamples(filtered);
    }
}

function loadExample(text) {
    document.getElementById('expression-input').value = text;
    handleInputChange();
    fullAnalysis();
}

// ==================== HISTORY ====================
async function loadHistory() {
    try {
        const response = await fetch('/api/history');
        const data = await response.json();
        displayHistory(data.history);
    } catch (error) {
        console.error('Error loading history:', error);
    }
}

function displayHistory(history) {
    const list = document.getElementById('history-list');

    if (!history || history.length === 0) {
        list.innerHTML = '<li class="history-empty">No analysis history yet</li>';
        return;
    }

    list.innerHTML = history.reverse().map(item => `
        <li class="history-item ${item.accepted ? 'accepted' : 'rejected'}" 
            onclick="loadExample('${escapeHtml(item.expression)}')">
            <div class="history-expression">${escapeHtml(item.expression)}</div>
            <div class="history-meta">
                <span>${item.token_count} tokens</span>
                <span>${item.timestamp}</span>
            </div>
        </li>
    `).join('');
}

async function clearHistory() {
    try {
        await fetch('/api/clear-history', { method: 'POST' });
        displayHistory([]);
        showToast('History cleared', 'success');
    } catch (error) {
        showToast('Error clearing history', 'error');
    }
}

function toggleHistory() {
    const sidebar = document.getElementById('history-sidebar');
    sidebar.classList.toggle('open');
    if (sidebar.classList.contains('open')) {
        loadHistory();
    }
}

// ==================== THEME ====================
function initializeTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    if (savedTheme === 'dark') {
        document.body.classList.remove('light-mode');
        document.body.classList.add('dark-mode');
        document.getElementById('theme-toggle').querySelector('.theme-icon').textContent = '☀️';
    }
}

function toggleTheme() {
    const body = document.body;
    const icon = document.getElementById('theme-toggle').querySelector('.theme-icon');

    if (body.classList.contains('dark-mode')) {
        body.classList.remove('dark-mode');
        body.classList.add('light-mode');
        icon.textContent = '🌙';
        localStorage.setItem('theme', 'light');
        showToast('Light mode enabled', 'info');
    } else {
        body.classList.remove('light-mode');
        body.classList.add('dark-mode');
        icon.textContent = '☀️';
        localStorage.setItem('theme', 'dark');
        showToast('Dark mode enabled', 'info');
    }
}

// ==================== UTILITY FUNCTIONS ====================
function switchTab(tabName) {
    // Update tab buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === tabName);
    });

    // Update tab panels
    document.querySelectorAll('.tab-panel').forEach(panel => {
        panel.classList.toggle('active', panel.id === `tab-${tabName}`);
    });
}

function clearAll() {
    document.getElementById('expression-input').value = '';
    document.getElementById('char-count').textContent = '0';
    document.getElementById('tokens-container').innerHTML = `
        <div class="empty-state">
            <div class="empty-icon">🔤</div>
            <p>Enter an expression and click "Tokenize" or "Full Analysis" to see tokens</p>
        </div>
    `;
    document.getElementById('parse-status-card').className = 'parse-status-card';
    document.getElementById('parse-status-card').innerHTML = `
        <div class="status-icon">⏳</div>
        <div class="status-message">No expression parsed yet</div>
    `;
    document.getElementById('parse-tree-container').innerHTML = `
        <div class="empty-state">
            <div class="empty-icon">🌳</div>
            <p>Parse results will appear here</p>
        </div>
    `;
    document.getElementById('languages-section').style.display = 'none';
    document.getElementById('token-count-badge').textContent = '0';
    document.querySelector('.status-badge').className = 'status-badge pending';
    document.querySelector('.status-badge').textContent = 'Awaiting input';

    // Reset stats
    document.getElementById('stat-total').textContent = '0';
    document.getElementById('stat-unique').textContent = '0';
    document.getElementById('stat-accepted').textContent = '-';
    document.getElementById('stat-languages').textContent = '-';

    // Destroy charts
    if (typeChart) { typeChart.destroy(); typeChart = null; }
    if (frequencyChart) { frequencyChart.destroy(); frequencyChart = null; }

    currentAnalysis = null;
    updateStatus('Ready to analyze', '#95a5a6');
    showToast('Cleared all content', 'info');
}

function exportResults() {
    if (!currentAnalysis) {
        showToast('No analysis results to export', 'warning');
        return;
    }

    const data = currentAnalysis;
    const lines = [
        '═'.repeat(70),
        'YAOUNDÉ MULTILINGUAL EXPRESSION ANALYSIS',
        'ICT University - Compiler Construction Project',
        '═'.repeat(70),
        '',
        `Expression: ${data.original}`,
        `Status: ${data.accepted ? '✓ ACCEPTED' : '✗ REJECTED'}`,
        `Parse Result: ${data.parse_result}`,
        `Languages Detected: ${data.languages_detected.join(', ')}`,
        `Timestamp: ${new Date(data.timestamp).toLocaleString()}`,
        '',
        '─'.repeat(70),
        'TOKENS',
        '─'.repeat(70),
        ''
    ];

    data.tokens.forEach((token, i) => {
        lines.push(`${(i + 1).toString().padStart(3)}. ${token.type.padEnd(25)} → '${token.value}'`);
    });

    lines.push('');
    lines.push('─'.repeat(70));
    lines.push('PARSE STEPS');
    lines.push('─'.repeat(70));
    lines.push('');

    data.parse_tree.forEach((step, i) => {
        lines.push(`${(i + 1).toString().padStart(3)}. ${step}`);
    });

    lines.push('');
    lines.push('─'.repeat(70));
    lines.push('STATISTICS');
    lines.push('─'.repeat(70));
    lines.push(`Total Tokens: ${data.statistics.total_count}`);
    lines.push(`Unique Tokens: ${data.statistics.unique_count}`);

    const content = lines.join('\n');
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = `yaounde-analysis-${Date.now()}.txt`;
    a.click();

    URL.revokeObjectURL(url);
    showToast('Results exported successfully', 'success');
}

function updateStatus(text, color) {
    const statusText = document.getElementById('status-text');
    statusText.textContent = text;
    statusText.style.color = 'white';

    const statusDot = document.querySelector('.status-dot');
    statusDot.style.backgroundColor = color;
}

function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    const icons = {
        success: '✅',
        error: '❌',
        warning: '⚠️',
        info: 'ℹ️'
    };

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <span class="toast-icon">${icons[type]}</span>
        <span>${message}</span>
    `;

    container.appendChild(toast);

    // Remove after animation
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

function playSound(type) {
    if (!soundEnabled) return;

    // Create audio context for generating tones
    try {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();

        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);

        if (type === 'success') {
            // Pleasant ascending tone for success
            oscillator.frequency.setValueAtTime(523.25, audioContext.currentTime); // C5
            oscillator.frequency.setValueAtTime(659.25, audioContext.currentTime + 0.1); // E5
            oscillator.frequency.setValueAtTime(783.99, audioContext.currentTime + 0.2); // G5
        } else {
            // Descending tone for error
            oscillator.frequency.setValueAtTime(349.23, audioContext.currentTime); // F4
            oscillator.frequency.setValueAtTime(293.66, audioContext.currentTime + 0.15); // D4
        }

        oscillator.type = 'sine';
        gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3);

        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.3);
    } catch (e) {
        // Audio not supported, silently fail
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ==================== VOICE INPUT ====================
let voiceLanguage = 'en-US'; // Default language
let voiceAttempts = 0;
const maxVoiceAttempts = 3;

function initializeVoiceRecognition() {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = true;
        
        // Try to use a language that works better for multilingual expressions
        // English (US) with better multilingual support
        recognition.lang = 'en-US';
        
        // Enable better multilingual recognition
        // Note: Some browsers support multiple languages
        try {
            // Try to set multiple languages if supported (Chrome/Edge)
            if (recognition.lang) {
                // Keep en-US as primary, but allow French and English words
                recognition.lang = 'en-US';
            }
        } catch (e) {
            console.log('Language setting not fully supported, using default');
        }

        recognition.onstart = () => {
            const btn = document.getElementById('btn-voice');
            btn.classList.add('listening');
            btn.querySelector('.voice-status').textContent = 'Listening...';
            showToast('🎤 Listening... Speak clearly (English/French/Pidgin mix OK)', 'info');
            voiceAttempts = 0;
            
            // Show help text
            const helpText = document.getElementById('voice-help');
            if (helpText) {
                helpText.style.display = 'block';
                helpText.classList.add('show');
            }
        };

        recognition.onresult = (event) => {
            let transcript = '';
            
            // Get the most confident result
            for (let i = event.resultIndex; i < event.results.length; i++) {
                transcript += event.results[i][0].transcript;
            }
            
            // Clean up transcript
            transcript = transcript.trim();
            
            // Show interim results
            if (event.results[event.resultIndex].isFinal) {
                document.getElementById('expression-input').value = transcript;
                handleInputChange();
                
                // Show helpful message for common Yaoundé expressions
                if (transcript.length > 0) {
                    showToast(`✓ Captured: "${transcript}"`, 'success');
                }
            } else {
                // Show interim result
                document.getElementById('expression-input').value = transcript;
            }
        };

        recognition.onend = () => {
            const btn = document.getElementById('btn-voice');
            btn.classList.remove('listening');
            btn.querySelector('.voice-status').textContent = 'Click to speak';
            
            // Hide help text
            const helpText = document.getElementById('voice-help');
            if (helpText) {
                helpText.style.display = 'none';
                helpText.classList.remove('show');
            }

            const input = document.getElementById('expression-input').value.trim();
            if (input) {
                // Auto-analyze if we got input
                showToast('✅ Voice captured! Analyzing...', 'success');
                setTimeout(() => {
                    fullAnalysis();
                }, 500);
            } else {
                // No input captured - offer help
                voiceAttempts++;
                if (voiceAttempts < maxVoiceAttempts) {
                    showToast('⚠️ No speech detected. Try speaking louder or closer to microphone.', 'warning');
                } else {
                    showToast('💡 Tip: Speak clearly. For best results, type expressions manually.', 'info');
                    voiceAttempts = 0;
                }
            }
        };

        recognition.onerror = (event) => {
            const btn = document.getElementById('btn-voice');
            btn.classList.remove('listening');
            btn.querySelector('.voice-status').textContent = 'Click to speak';
            
            let errorMessage = 'Voice recognition error';
            
            // Provide helpful error messages
            switch(event.error) {
                case 'no-speech':
                    errorMessage = 'No speech detected. Please speak clearly.';
                    break;
                case 'audio-capture':
                    errorMessage = 'Microphone not found. Please check your microphone.';
                    break;
                case 'not-allowed':
                    errorMessage = 'Microphone permission denied. Please allow microphone access.';
                    break;
                case 'network':
                    errorMessage = 'Network error. Check your internet connection.';
                    break;
                case 'aborted':
                    // User stopped it, don't show error
                    return;
                default:
                    errorMessage = `Voice error: ${event.error}. Try typing instead.`;
            }
            
            showToast(errorMessage, 'error');
            
            // Suggest typing for multilingual expressions
            if (event.error === 'no-speech' || event.error === 'not-allowed') {
                setTimeout(() => {
                    showToast('💡 Tip: For multilingual expressions, typing may be more accurate.', 'info');
                }, 2000);
            }
        };
        
        // Add helpful tooltip
        const btn = document.getElementById('btn-voice');
        if (btn) {
            btn.title = 'Voice Input - Speak clearly. Works best with English/French. For Pidgin/mixed expressions, typing may be more accurate.';
        }
    } else {
        // Hide voice button if not supported
        const btn = document.getElementById('btn-voice');
        const helpText = document.getElementById('voice-help');
        if (btn) {
            btn.style.display = 'none';
        }
        if (helpText) {
            helpText.style.display = 'none';
        }
        console.log('Voice recognition not supported in this browser');
    }
}

// Helper function to suggest voice-friendly expressions
function getVoiceFriendlyExpressions() {
    return [
        "bros drop me for Total",
        "give me 500 francs",
        "network is bad today",
        "light is off",
        "I want to go to campus"
    ];
}

// Show voice-friendly suggestions when voice button is hovered
function setupVoiceSuggestions() {
    const btn = document.getElementById('btn-voice');
    if (btn) {
        btn.addEventListener('mouseenter', () => {
            // Could show a tooltip with suggestions
            // For now, just update the title
        });
    }
}

function toggleVoiceInput() {
    if (!recognition) {
        showToast('Voice input not supported in this browser. Please use Chrome, Edge, or Safari.', 'warning');
        return;
    }

    const btn = document.getElementById('btn-voice');
    if (btn.classList.contains('listening')) {
        // Stop listening
        recognition.stop();
        btn.classList.remove('listening');
        btn.querySelector('.voice-status').textContent = 'Click to speak';
        showToast('Voice input stopped', 'info');
    } else {
        // Start listening
        try {
            // Check if microphone permission is available
            if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
                navigator.mediaDevices.getUserMedia({ audio: true })
                    .then(() => {
                        // Permission granted, start recognition
                        recognition.start();
                    })
                    .catch((err) => {
                        if (err.name === 'NotAllowedError' || err.name === 'PermissionDeniedError') {
                            showToast('Microphone permission denied. Please allow microphone access in browser settings.', 'error');
                        } else if (err.name === 'NotFoundError' || err.name === 'DevicesNotFoundError') {
                            showToast('No microphone found. Please connect a microphone.', 'error');
                        } else {
                            showToast('Cannot access microphone: ' + err.message, 'error');
                        }
                    });
            } else {
                // Fallback: try to start recognition directly
                recognition.start();
            }
        } catch (err) {
            showToast('Error starting voice input: ' + err.message, 'error');
        }
    }
}

// ==================== SOUND TOGGLE ====================
function initializeSoundSetting() {
    soundEnabled = localStorage.getItem('soundEnabled') !== 'false';
    updateSoundButton();
}

function toggleSound() {
    soundEnabled = !soundEnabled;
    localStorage.setItem('soundEnabled', soundEnabled);
    updateSoundButton();

    if (soundEnabled) {
        showToast('\ud83d\udd0a Sound enabled', 'success');
        playSound('success');
    } else {
        showToast('\ud83d\udd07 Sound disabled', 'info');
    }
}

function updateSoundButton() {
    const btn = document.getElementById('sound-toggle');
    const icon = btn.querySelector('.sound-icon');

    if (soundEnabled) {
        btn.classList.add('active');
        btn.classList.remove('muted');
        icon.textContent = '\ud83d\udd0a';
    } else {
        btn.classList.remove('active');
        btn.classList.add('muted');
        icon.textContent = '\ud83d\udd07';
    }
}

// ==================== AUTO-SAVE ====================
function initializeAutoSave() {
    // Save input on page unload
    window.addEventListener('beforeunload', () => {
        saveCurrentInput();
    });
}

function triggerAutoSave() {
    // Debounce auto-save
    if (autoSaveTimer) clearTimeout(autoSaveTimer);

    const indicator = document.getElementById('auto-save-indicator');
    indicator.classList.add('saving');
    indicator.querySelector('.save-text').textContent = 'Saving...';

    autoSaveTimer = setTimeout(() => {
        saveCurrentInput();
        indicator.classList.remove('saving');
        indicator.querySelector('.save-text').textContent = 'Auto-saved';
        indicator.classList.add('save-success');
        setTimeout(() => indicator.classList.remove('save-success'), 300);
    }, 1000);
}

function saveCurrentInput() {
    const input = document.getElementById('expression-input').value;
    localStorage.setItem('autoSavedInput', input);
    localStorage.setItem('autoSaveTime', new Date().toISOString());
}

function restoreAutoSave() {
    const savedInput = localStorage.getItem('autoSavedInput');
    const saveTime = localStorage.getItem('autoSaveTime');

    if (savedInput && savedInput.trim()) {
        document.getElementById('expression-input').value = savedInput;
        document.getElementById('char-count').textContent = savedInput.length;

        if (saveTime) {
            const time = new Date(saveTime);
            const timeStr = time.toLocaleTimeString();
            showToast(`Restored from ${timeStr}`, 'info');
        }
    }
}

// ==================== PDF EXPORT ====================
function exportToPDF() {
    if (!currentAnalysis) {
        showToast('No analysis results to export', 'warning');
        return;
    }

    showToast('Generating PDF...', 'info');

    try {
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();
        const data = currentAnalysis;

        // Colors
        const navy = [26, 30, 79];
        const gold = [201, 162, 39];

        // Header
        doc.setFillColor(...navy);
        doc.rect(0, 0, 210, 40, 'F');

        doc.setTextColor(255, 255, 255);
        doc.setFontSize(20);
        doc.setFont('helvetica', 'bold');
        doc.text('Yaound\u00e9 Multilingual Expression Analysis', 105, 18, { align: 'center' });

        doc.setFontSize(10);
        doc.setFont('helvetica', 'normal');
        doc.text('ICT University - Compiler Construction Project', 105, 28, { align: 'center' });
        doc.text(new Date().toLocaleString(), 105, 35, { align: 'center' });

        // Reset text color
        doc.setTextColor(0, 0, 0);
        let y = 50;

        // Expression section
        doc.setFillColor(...gold);
        doc.rect(10, y, 190, 8, 'F');
        doc.setTextColor(255, 255, 255);
        doc.setFontSize(12);
        doc.setFont('helvetica', 'bold');
        doc.text('EXPRESSION', 15, y + 6);
        y += 12;

        doc.setTextColor(0, 0, 0);
        doc.setFont('helvetica', 'normal');
        doc.setFontSize(11);
        doc.text(data.original, 15, y);
        y += 8;

        doc.setFontSize(10);
        const status = data.accepted ? '\u2713 ACCEPTED' : '\u2717 REJECTED';
        doc.setTextColor(data.accepted ? 39 : 231, data.accepted ? 174 : 76, data.accepted ? 96 : 60);
        doc.setFont('helvetica', 'bold');
        doc.text('Status: ' + status, 15, y);
        y += 6;

        doc.setTextColor(100, 100, 100);
        doc.setFont('helvetica', 'normal');
        doc.text('Languages: ' + data.languages_detected.join(', '), 15, y);
        y += 15;

        // Tokens section
        doc.setFillColor(...gold);
        doc.rect(10, y, 190, 8, 'F');
        doc.setTextColor(255, 255, 255);
        doc.setFontSize(12);
        doc.setFont('helvetica', 'bold');
        doc.text('TOKENS (' + data.tokens.length + ')', 15, y + 6);
        y += 12;

        // Tokens table
        const tokenData = data.tokens.map((t, i) => [
            (i + 1).toString(),
            t.type,
            t.value,
            t.category
        ]);

        doc.autoTable({
            startY: y,
            head: [['#', 'Type', 'Value', 'Category']],
            body: tokenData,
            theme: 'striped',
            headStyles: { fillColor: navy },
            columnStyles: {
                0: { cellWidth: 15 },
                1: { cellWidth: 60 },
                2: { cellWidth: 60 },
                3: { cellWidth: 45 }
            },
            margin: { left: 15, right: 15 }
        });

        y = doc.lastAutoTable.finalY + 10;

        // Statistics section
        if (y > 240) {
            doc.addPage();
            y = 20;
        }

        doc.setFillColor(...gold);
        doc.rect(10, y, 190, 8, 'F');
        doc.setTextColor(255, 255, 255);
        doc.setFontSize(12);
        doc.setFont('helvetica', 'bold');
        doc.text('STATISTICS', 15, y + 6);
        y += 15;

        doc.setTextColor(0, 0, 0);
        doc.setFont('helvetica', 'normal');
        doc.setFontSize(10);
        doc.text('Total Tokens: ' + data.statistics.total_count, 15, y);
        doc.text('Unique Tokens: ' + data.statistics.unique_count, 80, y);
        doc.text('Languages: ' + data.languages_detected.length, 145, y);
        y += 15;

        // Parse result
        doc.setFillColor(...gold);
        doc.rect(10, y, 190, 8, 'F');
        doc.setTextColor(255, 255, 255);
        doc.setFontSize(12);
        doc.setFont('helvetica', 'bold');
        doc.text('PARSE RESULT', 15, y + 6);
        y += 12;

        doc.setTextColor(0, 0, 0);
        doc.setFont('helvetica', 'normal');
        doc.setFontSize(9);

        const parseSteps = data.parse_tree.slice(0, 15);
        parseSteps.forEach((step, i) => {
            if (y > 280) {
                doc.addPage();
                y = 20;
            }
            doc.text((i + 1) + '. ' + step, 15, y);
            y += 5;
        });

        if (data.parse_tree.length > 15) {
            doc.text('... and ' + (data.parse_tree.length - 15) + ' more steps', 15, y);
        }

        // Footer
        const pageCount = doc.internal.getNumberOfPages();
        for (let i = 1; i <= pageCount; i++) {
            doc.setPage(i);
            doc.setFontSize(8);
            doc.setTextColor(150, 150, 150);
            doc.text('Generated by Yaound\u00e9 Multilingual Analyzer - ICT University', 105, 290, { align: 'center' });
            doc.text('Page ' + i + ' of ' + pageCount, 195, 290, { align: 'right' });
        }

        // Save
        doc.save('yaounde-analysis-' + Date.now() + '.pdf');
        showToast('\ud83d\udce5 PDF exported successfully!', 'success');

    } catch (error) {
        console.error('PDF export error:', error);
        showToast('Error generating PDF: ' + error.message, 'error');
    }
}

// ==================== COMPARISON MODE ====================
async function analyzeForCompare(side) {
    const inputId = 'compare-input-' + side;
    const resultId = 'compare-result-' + side;
    const expression = document.getElementById(inputId).value.trim();

    if (!expression) {
        showToast('Please enter an expression for side ' + side.toUpperCase(), 'warning');
        return;
    }

    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ expression })
        });

        const data = await response.json();

        if (data.error) {
            showToast('Error: ' + data.error, 'error');
            return;
        }

        // Store result
        if (side === 'a') {
            compareResultA = data;
        } else {
            compareResultB = data;
        }

        // Display result
        displayCompareResult(side, data);

        // Update summary if both sides are analyzed
        if (compareResultA && compareResultB) {
            displayCompareSummary();
        }

        playSound(data.accepted ? 'success' : 'error');

    } catch (error) {
        console.error('Compare error:', error);
        showToast('Error analyzing expression', 'error');
    }
}

function displayCompareResult(side, data) {
    const container = document.getElementById('compare-result-' + side);
    container.className = 'compare-result ' + (data.accepted ? 'accepted' : 'rejected');

    const statusText = data.accepted ? '\u2713 Accepted' : '\u2717 Rejected';
    const tokensHtml = data.tokens.map(t =>
        `<span class="compare-token ${t.category}">${t.value}</span>`
    ).join('');

    container.innerHTML = `
        <div class="compare-status">${statusText}</div>
        <div class="compare-tokens">${tokensHtml}</div>
        <div class="compare-stats">
            <div class="compare-stat">
                <div class="compare-stat-value">${data.tokens.length}</div>
                <div class="compare-stat-label">Tokens</div>
            </div>
            <div class="compare-stat">
                <div class="compare-stat-value">${data.languages_detected.length}</div>
                <div class="compare-stat-label">Languages</div>
            </div>
        </div>
    `;
}

function displayCompareSummary() {
    const summary = document.getElementById('compare-summary');
    summary.style.display = 'block';

    const a = compareResultA;
    const b = compareResultB;

    const grid = document.getElementById('summary-grid');
    grid.innerHTML = `
        <div class="summary-item">
            <div class="summary-label">Token Count</div>
            <div class="summary-values">
                <span class="summary-a ${a.tokens.length >= b.tokens.length ? 'winner' : ''}">${a.tokens.length}</span>
                <span class="summary-vs">vs</span>
                <span class="summary-b ${b.tokens.length > a.tokens.length ? 'winner' : ''}">${b.tokens.length}</span>
            </div>
        </div>
        <div class="summary-item">
            <div class="summary-label">Languages</div>
            <div class="summary-values">
                <span class="summary-a">${a.languages_detected.length}</span>
                <span class="summary-vs">vs</span>
                <span class="summary-b">${b.languages_detected.length}</span>
            </div>
        </div>
        <div class="summary-item">
            <div class="summary-label">Parse Status</div>
            <div class="summary-values">
                <span class="summary-a" style="color: ${a.accepted ? '#27ae60' : '#e74c3c'}">${a.accepted ? '\u2713' : '\u2717'}</span>
                <span class="summary-vs">vs</span>
                <span class="summary-b" style="color: ${b.accepted ? '#27ae60' : '#e74c3c'}">${b.accepted ? '\u2713' : '\u2717'}</span>
            </div>
        </div>
        <div class="summary-item">
            <div class="summary-label">Unique Types</div>
            <div class="summary-values">
                <span class="summary-a">${new Set(a.tokens.map(t => t.type)).size}</span>
                <span class="summary-vs">vs</span>
                <span class="summary-b">${new Set(b.tokens.map(t => t.type)).size}</span>
            </div>
        </div>
    `;
}

// Make loadExample globally accessible
window.loadExample = loadExample;
