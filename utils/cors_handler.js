XMLHttpRequest.prototype.normalOpen = XMLHttpRequest.prototype.open;

XMLHttpRequest.prototype.open = function (method, url, async, user, password) {
  //? Wrap open function and replace urls with ones that correspond
  //? to the spoofer's origin before executing open
  return this.normalOpen(
    method,
    `${window.origin}/?targetDomain=${url}`,
    async,
    user,
    password
  );
};
