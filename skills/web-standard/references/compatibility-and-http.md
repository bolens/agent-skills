# Compatibility and HTTP

## Progressive enhancement

Use the [modern target policy](modern-targets.md): latest stable engines and features by default, legacy support only when explicitly required. Define the usable baseline within that target set and add the requested enhancement around it. Test capabilities through the relevant JavaScript API or CSS support query, but remember that API presence alone may not prove every required subfeature works. Use a narrow compatibility workaround only when supported by a real target-browser defect. [Progressive enhancement](https://developer.mozilla.org/en-US/docs/Glossary/Progressive_Enhancement), [feature detection over UA sniffing](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Browser_detection_using_the_user_agent).

Keep server/client rendering deterministic. A client-only browser API should not crash server evaluation. Do not hide hydration or parser repairs by suppressing warnings without finding the cause. Scope polyfills to the capabilities and delivery targets actually required.

## Requests and responses

Use HTTP methods and statuses for the operation actually performed. Safe navigation must not trigger application mutations. Preserve deliberate redirect behavior and verify whether the method/body is retained or changed when that matters. Use the actual response status for missing or rejected resources rather than a success-shaped error screen.

`fetch()` can resolve normally for an HTTP error response. Check status and the expected response format before treating it as success. Handle abort, network failure, invalid response bodies, and application rejection distinctly. `mode: "no-cors"` does not make a blocked cross-origin response readable. Inspect the intended server CORS policy instead. [Using Fetch](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch).

## Caching and delivery

Distinguish private and shared caches, storage and revalidation, and immutable versioned assets from changing HTML. `no-cache` permits storage with revalidation; it is not equivalent to `no-store`. Inspect validators, `Vary`, and CDN configuration when relevant. Do not broadly disable caching to cover an application state bug or share personalized responses without the intended protections. [HTTP caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching).

Verify response behavior through the real reverse proxy or hosting path when it controls headers and redirects. Local development-server results do not establish production behavior. Route security-sensitive policy to `web-security` and search visibility to `technical-seo`.
