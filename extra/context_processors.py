def crap_browser(request):
  browser=request.META.get('HTTP_USER_AGENT','Nothing in http user agent')
  bool='MSIE' in browser
  return {'crap_browser':bool,'browser':browser}
