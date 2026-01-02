const API_BASE = '/api';

class IPTVApp {
    constructor() {
        this.channels = [];
        this.groups = [];
        this.favorites = new Set();
        this.currentPage = 1;
        this.pageSize = 50;
        this.currentFilter = null;
        this.currentSearch = '';
        this.player = null;
        
        this.init();
    }
    
    async init() {
        await this.loadFavorites();
        await this.loadGroups();
        await this.loadChannels();
        this.setupEventListeners();
    }
    
    setupEventListeners() {
        const searchInput = document.getElementById('searchInput');
        const groupFilter = document.getElementById('groupFilter');
        const refreshBtn = document.getElementById('refreshBtn');
        const prevBtn = document.getElementById('prevBtn');
        const nextBtn = document.getElementById('nextBtn');
        const closePlayer = document.getElementById('closePlayer');
        
        let searchTimeout;
        searchInput?.addEventListener('input', (e) => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                this.currentSearch = e.target.value;
                this.currentPage = 1;
                if (this.currentSearch.length > 0) {
                    this.searchChannels(this.currentSearch);
                } else {
                    this.loadChannels();
                }
            }, 500);
        });
        
        groupFilter?.addEventListener('change', (e) => {
            this.currentFilter = e.target.value;
            this.currentPage = 1;
            this.loadChannels();
        });
        
        refreshBtn?.addEventListener('click', () => this.refreshChannels());
        prevBtn?.addEventListener('click', () => this.prevPage());
        nextBtn?.addEventListener('click', () => this.nextPage());
        closePlayer?.addEventListener('click', () => this.closePlayer());
    }
    
    async loadGroups() {
        try {
            const response = await fetch(`${API_BASE}/channels/groups`);
            const data = await response.json();
            this.groups = data.groups;
            this.renderGroups();
        } catch (error) {
            console.error('Error loading groups:', error);
        }
    }
    
    renderGroups() {
        const groupFilter = document.getElementById('groupFilter');
        const groupList = document.getElementById('groupList');
        
        if (groupFilter) {
            groupFilter.innerHTML = '<option value="">All Groups</option>';
            this.groups.forEach(group => {
                const option = document.createElement('option');
                option.value = group;
                option.textContent = group;
                groupFilter.appendChild(option);
            });
        }
        
        if (groupList) {
            groupList.innerHTML = '';
            const allItem = document.createElement('li');
            allItem.innerHTML = `<span>All Channels</span>`;
            allItem.addEventListener('click', () => {
                this.currentFilter = null;
                this.currentPage = 1;
                this.loadChannels();
                document.querySelectorAll('.group-list li').forEach(li => li.classList.remove('active'));
                allItem.classList.add('active');
            });
            allItem.classList.add('active');
            groupList.appendChild(allItem);
            
            this.groups.forEach(group => {
                const li = document.createElement('li');
                li.innerHTML = `<span>${group}</span>`;
                li.addEventListener('click', () => {
                    this.currentFilter = group;
                    this.currentPage = 1;
                    this.loadChannels();
                    document.querySelectorAll('.group-list li').forEach(li => li.classList.remove('active'));
                    li.classList.add('active');
                });
                groupList.appendChild(li);
            });
        }
    }
    
    async loadChannels() {
        try {
            this.showLoading();
            let url = `${API_BASE}/channels?page=${this.currentPage}&page_size=${this.pageSize}`;
            
            if (this.currentFilter) {
                url += `&group=${encodeURIComponent(this.currentFilter)}`;
            }
            
            const response = await fetch(url);
            const data = await response.json();
            
            this.channels = data.channels;
            this.totalChannels = data.total;
            this.renderChannels();
            this.updatePagination();
        } catch (error) {
            console.error('Error loading channels:', error);
            this.showError('Failed to load channels');
        }
    }
    
    async searchChannels(query) {
        try {
            this.showLoading();
            const response = await fetch(`${API_BASE}/channels/search?q=${encodeURIComponent(query)}&page=${this.currentPage}&page_size=${this.pageSize}`);
            const data = await response.json();
            
            this.channels = data.channels;
            this.totalChannels = data.total;
            this.renderChannels();
            this.updatePagination();
        } catch (error) {
            console.error('Error searching channels:', error);
            this.showError('Failed to search channels');
        }
    }
    
    renderChannels() {
        const grid = document.getElementById('channelGrid');
        if (!grid) return;
        
        if (this.channels.length === 0) {
            grid.innerHTML = '<div class="no-results">No channels found</div>';
            return;
        }
        
        grid.innerHTML = '';
        this.channels.forEach(channel => {
            const card = this.createChannelCard(channel);
            grid.appendChild(card);
        });
    }
    
    createChannelCard(channel) {
        const card = document.createElement('div');
        card.className = 'channel-card';
        
        const isFavorite = this.favorites.has(channel.id);
        
        card.innerHTML = `
            <button class="favorite-btn ${isFavorite ? 'active' : ''}" data-channel-id="${channel.id}">
                ${isFavorite ? '❤️' : '🤍'}
            </button>
            ${channel.logo ? 
                `<img src="${channel.logo}" alt="${channel.name}" class="channel-logo" onerror="this.src='data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 width=%22200%22 height=%22120%22><rect fill=%22%23f0f0f0%22 width=%22200%22 height=%22120%22/><text x=%2250%%22 y=%2250%%22 font-family=%22Arial%22 font-size=%2214%22 fill=%22%23999%22 text-anchor=%22middle%22 dy=%22.3em%22>No Logo</text></svg>'">` : 
                `<div class="channel-logo" style="display:flex;align-items:center;justify-content:center;color:#999;">📺</div>`
            }
            <div class="channel-name">${channel.name}</div>
            ${channel.group ? `<span class="channel-group">${channel.group}</span>` : ''}
            ${channel.language ? `<div class="channel-language">🌐 ${channel.language}</div>` : ''}
        `;
        
        card.addEventListener('click', (e) => {
            if (!e.target.classList.contains('favorite-btn')) {
                this.playChannel(channel);
            }
        });
        
        const favoriteBtn = card.querySelector('.favorite-btn');
        favoriteBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            this.toggleFavorite(channel.id);
        });
        
        return card;
    }
    
    async playChannel(channel) {
        try {
            const modal = document.getElementById('playerModal');
            const player = document.getElementById('videoPlayer');
            const channelInfo = document.getElementById('channelInfo');
            
            modal.classList.add('active');
            
            channelInfo.innerHTML = `
                <h2>${channel.name}</h2>
                ${channel.group ? `<p>Category: ${channel.group}</p>` : ''}
            `;
            
            if (Hls.isSupported() && channel.url.includes('.m3u8')) {
                if (this.player) {
                    this.player.destroy();
                }
                this.player = new Hls();
                this.player.loadSource(channel.url);
                this.player.attachMedia(player);
                this.player.on(Hls.Events.MANIFEST_PARSED, () => {
                    player.play();
                });
            } else if (player.canPlayType('application/vnd.apple.mpegurl')) {
                player.src = channel.url;
                player.play();
            } else {
                alert('Your browser does not support HLS playback');
            }
            
            await this.loadEPG(channel.id);
        } catch (error) {
            console.error('Error playing channel:', error);
            alert('Failed to load stream');
        }
    }
    
    async loadEPG(channelId) {
        try {
            const response = await fetch(`${API_BASE}/epg/${channelId}`);
            const data = await response.json();
            
            const epgInfo = document.getElementById('epgInfo');
            epgInfo.innerHTML = '<h3>Program Guide</h3>';
            
            if (data.current_program) {
                const currentDiv = document.createElement('div');
                currentDiv.innerHTML = `
                    <h4 style="margin-bottom: 10px;">Now Playing</h4>
                    <div class="program-item">
                        <div class="program-title">${data.current_program.title}</div>
                        <div class="program-time">
                            ${new Date(data.current_program.start_time).toLocaleTimeString()} - 
                            ${new Date(data.current_program.end_time).toLocaleTimeString()}
                        </div>
                        ${data.current_program.description ? 
                            `<div style="margin-top: 8px; color: #666;">${data.current_program.description}</div>` : ''}
                    </div>
                `;
                epgInfo.appendChild(currentDiv);
            }
            
            if (data.upcoming_programs && data.upcoming_programs.length > 0) {
                const upcomingDiv = document.createElement('div');
                upcomingDiv.innerHTML = '<h4 style="margin: 20px 0 10px;">Coming Up</h4>';
                
                data.upcoming_programs.slice(0, 5).forEach(program => {
                    const programDiv = document.createElement('div');
                    programDiv.className = 'program-item';
                    programDiv.innerHTML = `
                        <div class="program-title">${program.title}</div>
                        <div class="program-time">
                            ${new Date(program.start_time).toLocaleTimeString()} - 
                            ${new Date(program.end_time).toLocaleTimeString()}
                        </div>
                    `;
                    upcomingDiv.appendChild(programDiv);
                });
                
                epgInfo.appendChild(upcomingDiv);
            }
        } catch (error) {
            console.error('Error loading EPG:', error);
        }
    }
    
    closePlayer() {
        const modal = document.getElementById('playerModal');
        const player = document.getElementById('videoPlayer');
        
        modal.classList.remove('active');
        player.pause();
        player.src = '';
        
        if (this.player) {
            this.player.destroy();
            this.player = null;
        }
    }
    
    async loadFavorites() {
        try {
            const response = await fetch(`${API_BASE}/favorites`);
            const data = await response.json();
            this.favorites = new Set(data.favorites);
        } catch (error) {
            console.error('Error loading favorites:', error);
        }
    }
    
    async toggleFavorite(channelId) {
        try {
            if (this.favorites.has(channelId)) {
                await fetch(`${API_BASE}/favorites/${channelId}`, {
                    method: 'DELETE'
                });
                this.favorites.delete(channelId);
            } else {
                await fetch(`${API_BASE}/favorites`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        channel_id: channelId,
                        list_name: 'default'
                    })
                });
                this.favorites.add(channelId);
            }
            this.renderChannels();
        } catch (error) {
            console.error('Error toggling favorite:', error);
        }
    }
    
    async refreshChannels() {
        try {
            const refreshBtn = document.getElementById('refreshBtn');
            refreshBtn.disabled = true;
            refreshBtn.textContent = 'Refreshing...';
            
            await fetch(`${API_BASE}/channels/refresh`, { method: 'POST' });
            await this.loadGroups();
            await this.loadChannels();
            
            refreshBtn.disabled = false;
            refreshBtn.textContent = 'Refresh';
        } catch (error) {
            console.error('Error refreshing channels:', error);
            alert('Failed to refresh channels');
        }
    }
    
    showLoading() {
        const grid = document.getElementById('channelGrid');
        if (grid) {
            grid.innerHTML = '<div class="loading">Loading channels...</div>';
        }
    }
    
    showError(message) {
        const grid = document.getElementById('channelGrid');
        if (grid) {
            grid.innerHTML = `<div class="no-results">${message}</div>`;
        }
    }
    
    updatePagination() {
        const prevBtn = document.getElementById('prevBtn');
        const nextBtn = document.getElementById('nextBtn');
        const pageInfo = document.getElementById('pageInfo');
        
        if (prevBtn) {
            prevBtn.disabled = this.currentPage === 1;
        }
        
        if (nextBtn) {
            const totalPages = Math.ceil(this.totalChannels / this.pageSize);
            nextBtn.disabled = this.currentPage >= totalPages;
        }
        
        if (pageInfo) {
            const totalPages = Math.ceil(this.totalChannels / this.pageSize);
            pageInfo.textContent = `Page ${this.currentPage} of ${totalPages} (${this.totalChannels} channels)`;
        }
    }
    
    prevPage() {
        if (this.currentPage > 1) {
            this.currentPage--;
            if (this.currentSearch) {
                this.searchChannels(this.currentSearch);
            } else {
                this.loadChannels();
            }
        }
    }
    
    nextPage() {
        const totalPages = Math.ceil(this.totalChannels / this.pageSize);
        if (this.currentPage < totalPages) {
            this.currentPage++;
            if (this.currentSearch) {
                this.searchChannels(this.currentSearch);
            } else {
                this.loadChannels();
            }
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.app = new IPTVApp();
});
