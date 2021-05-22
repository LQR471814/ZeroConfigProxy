function construct_spoofed_request(original_url) {
	return `${window.origin}/Request?targetUrl=${encodeURIComponent(normalizeUrl(original_url))}`
}

if (!window.normalOpen) { //? If not already executed
	//? Actual Code
	var normalOpen = XMLHttpRequest.prototype.open
	var normalFetch = window.fetch

	XMLHttpRequest.prototype.open = function (method, url, asyn, user, password) {
		//? Wrap open function and replace urls with ones that correspond
		//? to the spoofer's origin before executing open
		return normalOpen(
			method,
			construct_spoofed_request(url),
			asyn,
			user,
			password
		)
	}

	window.fetch = function (resource, init) {
		if (resource instanceof URL) {
			resource = URL.toString()
		}

		return normalFetch(
			construct_spoofed_request(resource),
			init
		)
	}
}