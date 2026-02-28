(function () {
    console.log("CMS Injection Active: Overriding fetch for Prismic CMS...");

    const originalFetch = window.fetch;
    window.fetch = async function (...args) {
        const urlRequest = args[0];
        const url = typeof urlRequest === 'string' ? urlRequest : urlRequest.url;

        // Check if this is a Prismic CMS request
        if (url.includes('thevertmenthe.cdn.prismic.io')) {
            const decodedUrl = decodeURIComponent(url);
            console.log("CMS Injection: Intercepting Prismic request:", decodedUrl);

            // 1. Handle the base API request (handshake/refs)
            if (decodedUrl.includes('/api/v2') && (decodedUrl.endsWith('/api/v2') || decodedUrl.endsWith('/api/v2/') || decodedUrl.includes('/api/v2?'))) {
                const mockRefs = {
                    "refs": [{
                        "id": "master", "ref": "LOCAL_REF", "label": "Master", "isMasterRef": true
                    }],
                    "types": { "home": "Home", "article": "Article", "about": "About", "gallery": "Gallery" },
                    "languages": [{ "id": "fr-fr", "name": "French" }]
                };
                return new Response(JSON.stringify(mockRefs), { status: 200, headers: { 'Content-Type': 'application/json' } });
            }

            // Fetch our local site_content.json
            let masterContent;
            try {
                const response = await originalFetch('site_content.json');
                masterContent = await response.json();
            } catch (err) {
                console.error("CMS Injection: Failed to load site_content.json", err);
                return originalFetch(...args);
            }

            let result = { results: [] };

            // Build a flat list of all documents for ID/UID matching
            const allDocs = [
                ...(masterContent.article ? masterContent.article.results : []),
                ...(masterContent.home ? masterContent.home.results : []),
                ...(masterContent.about ? masterContent.about.results : [])
            ];

            // Helper to match Type in query
            const matchType = (type) => {
                // The URL is like: ...?q=[[at(document.type,"home")]]
                // We need to account for URI encoding of brackets and quotes, or just do a simple string includes
                return decodedUrl.includes(`document.type`) && (decodedUrl.includes(`"${type}"`) || decodedUrl.includes(`%22${type}%22`));
            };

            // PRIORITY 1: Match by specific ID or UID
            const idMatch = decodedUrl.match(/at\(document\.id,\s*["']([^"']+)["']\s*\)/) ||
                decodedUrl.match(/at\(document\.id,%22([^%]+)%22\)/) ||
                decodedUrl.match(/at\(my\.article\.uid,\s*["']([^"']+)["']\s*\)/) ||
                decodedUrl.match(/at\(my\.article\.uid,%22([^%]+)%22\)/);

            if (idMatch) {
                const idOrUid = idMatch[1];
                const found = allDocs.find(d => d.id === idOrUid || d.uid === idOrUid);
                if (found) {
                    console.log("CMS Injection: Found specific document by ID/UID:", idOrUid);
                    result = { results: [found] };
                }
            }
            // PRIORITY 2: Match by Type (if no ID/UID match was forced)
            else if (matchType('home')) {
                result = masterContent.home || { results: [] };
                console.log("CMS Injection: Returning HOME doc list (length " + result.results.length + ")");
            }
            else if (matchType('article') || matchType('gallery')) {
                result = masterContent.article || { results: [] };
                console.log("CMS Injection: Returning ARTICLE/GALLERY collection (length " + result.results.length + ")");
            }
            else if (matchType('about')) {
                result = masterContent.about || { results: [] };
                console.log("CMS Injection: Returning ABOUT doc list (empty)");
            }
            // PRIORITY 3: Fallback for Search
            else if (decodedUrl.includes('search') || decodedUrl.includes('fulltext')) {
                result = masterContent.article || { results: [] };
                console.log("CMS Injection: Returning Search Fallback (length " + result.results.length + ")");
            }

            return new Response(JSON.stringify(result), { status: 200, headers: { 'Content-Type': 'application/json' } });
        }

        // Pass through everything else (images, models, etc.)
        return originalFetch(...args);
    };
})();
