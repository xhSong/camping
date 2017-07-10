from camping import check_park_for_n_weeks
from emailnotify import send_email


if __name__ == '__main__':
  sites = []

  # TODO: Add parks that you want to looking for.
  # UPPER PINES, CA
  sites.extend(check_park_for_n_weeks('NRSO', 70925))

  # NORTH PINES, CA
  sites.extend(check_park_for_n_weeks('NRSO', 70927))

  # HALF MOON BAY SB, CA
  sites.extend(check_park_for_n_weeks('CA', 120039))

  # LOWER PINES, CA
  sites.extend(check_park_for_n_weeks('NRSO', 70928))

  # PFEIFFER BIG SUR SP, CA
  sites.extend(check_park_for_n_weeks('CA', 120068))

  # JULIA PFEIFFER BURNS SP, CA
  sites.extend(check_park_for_n_weeks('CA', 120045))

  # TODO: Add your own filter here.
  sites = [site for site in sites if site.date.isoweekday() in [5, 6]]

  message = '\n'.join(str(site) for site in sites)
  if message:
    print 'Sending available sites to email ...'
    # TODO: Change the example email to your own email.  
    send_email(message, 'example@gmail.com')
  else:
    print "Available site not found"
