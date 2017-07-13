Historic Oregon News theme
===

This repository holds the theme and other customizations for http://oregonnews.uoregon.edu using Open ONI.


Usage
---

Put this into `themes/oregon`.

Hook up the apps in `onisite/settings_local.py` as such:

    INSTALLED_APPS = (
      'django.contrib.humanize',
      'django.contrib.staticfiles',
      'themes.oregon',
      'themes.default',
      'core',
    )
