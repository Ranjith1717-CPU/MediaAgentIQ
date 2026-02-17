/**
 * MediaAgentIQ - Frontend JavaScript
 * Main application logic for the AI Agent Platform
 */

// Global state
const MediaAgentIQ = {
    agents: {},
    stats: {},
    activity: []
};

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

/**
 * Initialize the application
 */
function initializeApp() {
    // Load initial data
    loadStats();
    loadActivity();

    // Set up auto-refresh for activity
    setInterval(loadActivity, 30000);

    // Initialize tooltips
    initTooltips();

    console.log('MediaAgentIQ initialized');
}

/**
 * Load dashboard statistics
 */
async function loadStats() {
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();
        MediaAgentIQ.stats = data;
        updateStatsDisplay(data);
    } catch (error) {
        console.error('Failed to load stats:', error);
    }
}

/**
 * Load recent activity
 */
async function loadActivity() {
    try {
        const response = await fetch('/api/activity?limit=5');
        const data = await response.json();
        MediaAgentIQ.activity = data;
        updateActivityDisplay(data);
    } catch (error) {
        console.error('Failed to load activity:', error);
    }
}

/**
 * Update stats display on dashboard
 */
function updateStatsDisplay(stats) {
    const elements = {
        totalJobs: document.getElementById('stat-total-jobs'),
        completedJobs: document.getElementById('stat-completed-jobs'),
        archiveSize: document.getElementById('stat-archive-size'),
        complianceIssues: document.getElementById('stat-compliance-issues')
    };

    for (const [key, element] of Object.entries(elements)) {
        if (element && stats[key] !== undefined) {
            animateNumber(element, stats[key]);
        }
    }
}

/**
 * Update activity feed display
 */
function updateActivityDisplay(activity) {
    const feed = document.getElementById('activity-feed');
    if (!feed) return;

    if (!activity || activity.length === 0) {
        feed.innerHTML = `
            <div class="text-gray-500 text-center py-8">
                No activity yet. Start using an agent!
            </div>
        `;
        return;
    }

    feed.innerHTML = activity.map(item => `
        <div class="flex items-center justify-between p-3 bg-gray-800/50 rounded-lg fade-in">
            <div class="flex items-center space-x-3">
                <span class="w-2 h-2 bg-green-400 rounded-full"></span>
                <span class="text-gray-300">${capitalize(item.agent_type)} Agent</span>
                <span class="text-gray-500">${item.action}</span>
            </div>
            <span class="text-gray-500 text-sm">${formatTimestamp(item.created_at)}</span>
        </div>
    `).join('');
}

/**
 * Animate number change
 */
function animateNumber(element, target, duration = 500) {
    const start = parseInt(element.textContent) || 0;
    const change = target - start;
    const startTime = performance.now();

    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);

        element.textContent = Math.round(start + change * easeOutQuad(progress));

        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }

    requestAnimationFrame(update);
}

/**
 * Easing function for animations
 */
function easeOutQuad(t) {
    return t * (2 - t);
}

/**
 * Capitalize first letter
 */
function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

/**
 * Format timestamp for display
 */
function formatTimestamp(timestamp) {
    if (!timestamp) return '';

    const date = new Date(timestamp);
    const now = new Date();
    const diff = now - date;

    // Less than a minute
    if (diff < 60000) {
        return 'Just now';
    }

    // Less than an hour
    if (diff < 3600000) {
        const minutes = Math.floor(diff / 60000);
        return `${minutes}m ago`;
    }

    // Less than a day
    if (diff < 86400000) {
        const hours = Math.floor(diff / 3600000);
        return `${hours}h ago`;
    }

    // More than a day
    return date.toLocaleDateString();
}

/**
 * Format duration in seconds to readable string
 */
function formatDuration(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);

    if (hours > 0) {
        return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
    return `${minutes}:${secs.toString().padStart(2, '0')}`;
}

/**
 * Format file size
 */
function formatFileSize(bytes) {
    if (bytes === 0) return '0 B';

    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
}

/**
 * Initialize tooltips
 */
function initTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', showTooltip);
        element.addEventListener('mouseleave', hideTooltip);
    });
}

/**
 * Show tooltip
 */
function showTooltip(event) {
    const text = event.target.dataset.tooltip;
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.textContent = text;
    tooltip.style.cssText = `
        position: fixed;
        background: #1e293b;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 0.375rem;
        font-size: 0.875rem;
        z-index: 9999;
        pointer-events: none;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    `;

    document.body.appendChild(tooltip);

    const rect = event.target.getBoundingClientRect();
    tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
    tooltip.style.top = rect.bottom + 8 + 'px';

    event.target._tooltip = tooltip;
}

/**
 * Hide tooltip
 */
function hideTooltip(event) {
    if (event.target._tooltip) {
        event.target._tooltip.remove();
        delete event.target._tooltip;
    }
}

/**
 * Show toast notification
 */
function showToast(message, type = 'info', duration = 3000) {
    const toast = document.createElement('div');
    toast.className = 'toast';

    const colors = {
        info: '#3b82f6',
        success: '#22c55e',
        warning: '#eab308',
        error: '#ef4444'
    };

    toast.style.borderLeft = `4px solid ${colors[type]}`;
    toast.innerHTML = `
        <div class="flex items-center gap-3">
            <span>${message}</span>
            <button onclick="this.parentElement.parentElement.remove()" class="text-gray-400 hover:text-white">×</button>
        </div>
    `;

    document.body.appendChild(toast);

    // Trigger animation
    setTimeout(() => toast.classList.add('show'), 10);

    // Auto remove
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

/**
 * Copy text to clipboard
 */
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        showToast('Copied to clipboard!', 'success');
        return true;
    } catch (error) {
        console.error('Failed to copy:', error);
        showToast('Failed to copy', 'error');
        return false;
    }
}

/**
 * Download content as file
 */
function downloadFile(content, filename, mimeType = 'text/plain') {
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

/**
 * Debounce function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Throttle function
 */
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = MediaAgentIQ;
}
