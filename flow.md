## Variable Definition

```text
{URL}: Spoof Server's Host
{Target}: Target Domain
{QS}: ?targetDomain={Target} querystring (url encoded)

{org:QS}: Original URL querystring (given context)
{org:PATH}: Original URL path (given context)

{spoofed:URL}
Format:
    http://{URL}{org:PATH}?{QS}
Should be generated dynamically given context
```

#### (The Fragment Portion of the URL is ignored as it is handled client side)

## URL Format

A valid URL is described as:

```text
<schema>:<domain></path>?<query>
```

A valid domain is described as:

```text
//<userinfo>@<host>:<port>
```

```text
        Initial request (www.proxy.com/Request?targetUrl=google.com)
      /     |      |     \
    req 1, req 2, req 3, req 4
       \
   redirect link (www.proxy.com/Request?targetUrl=google.com/redirect)
   /     |     \
 req 1, req 2, req 3
```

#### On Client requests `{URL}?{QS}`:

1. Get `{Target}` from `{QS}` through query string value `?targetRequest=` (Assume `{Target}` is valid URL)
1. Server requests `{Target}`
    1. If content mimetype is HTML
        1. Server parses returned HTML content
        1. Search and replace all tag attributes that can contain a link and replaces them `{spoofed:URL}` with  (with all extra QS that URL originally had)
        1. Add script tag to modify requests in `<head>`
    1. If content mimetype is CSS
        1. Use regex to replace all urls inside `url()` with `{spoofed:URL}`
1. Server returns HTTP Response with new content (flask) to Client

#### When server spoofs a url (points it towards itself) it goes through these steps

1. Parse the original URL
1. Add `?targetUrl=` in the query string
    1. Get the original URL (the url that was supposed to be used before spoofing happened)
    1. Normalize URL to valid URL format as described
    1. Set value of `{QS}`
        1. Parse query string of original URL
        1. Set `targetUrl` in the query string
        1. Encode new query string
1. Replace `<domain>` and `<queryString>` in parsed URL with `{URL}` and the `{QS}`
