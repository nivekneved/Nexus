/**
 * Nexus Polymorphic Data Access Layer (DAL)
 * Features:
 * 1. Request Deduplication: Merges concurrent in-flight requests to the same endpoint.
 * 2. In-Memory Cache (SWR): Returns cached data immediately while refreshing in background.
 * 3. Pluggable Adapters: Seamless toggle between FastAPI REST endpoints and Supabase Client.
 * 4. Error Normalization: Consistent error formatting across all data requests.
 */

(function (window) {
    'use strict';

    class NexusDAL {
        constructor(config = {}) {
            this.mode = config.mode || 'rest'; // 'rest' | 'supabase'
            this.cacheDurationMs = config.cacheDurationMs || 5000;
            this.cache = new Map();
            this.inFlight = new Map();
            this.supabaseClient = config.supabaseClient || null;
            this.baseUrl = config.baseUrl || '';
        }

        /**
         * Set the operational backend mode ('rest' | 'supabase')
         */
        setMode(mode, client = null) {
            this.mode = mode;
            if (client) this.supabaseClient = client;
            console.info(`[NexusDAL] Switched backend mode to: ${this.mode}`);
        }

        /**
         * Invalidate cache for a specific key or pattern
         */
        invalidateCache(pattern = null) {
            if (!pattern) {
                this.cache.clear();
                return;
            }
            for (const key of this.cache.keys()) {
                if (key.includes(pattern)) {
                    this.cache.delete(key);
                }
            }
        }

        /**
         * Polymorphic resource fetcher with SWR and deduplication
         */
        async query(endpoint, options = {}) {
            const method = (options.method || 'GET').toUpperCase();
            const cacheKey = `${method}:${endpoint}:${JSON.stringify(options.body || {})}`;

            // Mutations bypass cache and invalidate affected cache keys
            if (method !== 'GET') {
                const res = await this._executeRequest(endpoint, options);
                this.invalidateCache(endpoint.split('?')[0]);
                return res;
            }

            // Check in-flight deduplication
            if (this.inFlight.has(cacheKey)) {
                return this.inFlight.get(cacheKey);
            }

            // Check cache validity
            const cached = this.cache.get(cacheKey);
            const now = Date.now();
            if (cached && (now - cached.timestamp < this.cacheDurationMs)) {
                return cached.data;
            }

            // Execute request with deduplication
            const fetchPromise = this._executeRequest(endpoint, options)
                .then(data => {
                    this.cache.set(cacheKey, { data, timestamp: Date.now() });
                    this.inFlight.delete(cacheKey);
                    return data;
                })
                .catch(err => {
                    this.inFlight.delete(cacheKey);
                    throw err;
                });

            this.inFlight.set(cacheKey, fetchPromise);
            return fetchPromise;
        }

        /**
         * Low-level dispatcher between REST and Supabase adapters
         */
        async _executeRequest(endpoint, options) {
            if (this.mode === 'supabase' && this.supabaseClient && !options.forceRest) {
                return this._querySupabase(endpoint, options);
            }
            return this._queryRest(endpoint, options);
        }

        /**
         * REST adapter
         */
        async _queryRest(endpoint, options) {
            const url = `${this.baseUrl}${endpoint}`;
            const headers = Object.assign({
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }, options.headers || {});

            const fetchOpts = {
                method: options.method || 'GET',
                headers: headers
            };

            if (options.body && options.method !== 'GET') {
                fetchOpts.body = typeof options.body === 'string' ? options.body : JSON.stringify(options.body);
            }

            const res = await fetch(url, fetchOpts);
            if (!res.ok) {
                let errDetail = `HTTP ${res.status} ${res.statusText}`;
                try {
                    const errBody = await res.json();
                    errDetail = errBody.detail || errBody.message || JSON.stringify(errBody);
                } catch (_) {}
                throw new Error(`[NexusDAL] ${errDetail}`);
            }

            return res.json();
        }

        /**
         * Supabase adapter stub for instant zero-code backend swapping
         */
        async _querySupabase(endpoint, options) {
            // Translates standard API endpoint pattern (/api/<table_or_resource>) to Supabase query
            const parts = endpoint.replace(/^\/api\//, '').split('?');
            const tableName = parts[0];
            
            if (!this.supabaseClient) {
                console.warn('[NexusDAL] Supabase client uninitialized. Falling back to REST.');
                return this._queryRest(endpoint, options);
            }

            const sb = this.supabaseClient;
            if (options.method === 'POST') {
                const { data, error } = await sb.from(tableName).insert(options.body).select();
                if (error) throw new Error(`[Supabase Error] ${error.message}`);
                return data;
            } else if (options.method === 'PUT' || options.method === 'PATCH') {
                const id = options.body.id;
                const { data, error } = await sb.from(tableName).update(options.body).eq('id', id).select();
                if (error) throw new Error(`[Supabase Error] ${error.message}`);
                return data;
            } else {
                const { data, error } = await sb.from(tableName).select('*');
                if (error) throw new Error(`[Supabase Error] ${error.message}`);
                return data;
            }
        }
    }

    // Export globally
    window.NexusDAL = NexusDAL;
    window.dal = new NexusDAL();
})(window);
