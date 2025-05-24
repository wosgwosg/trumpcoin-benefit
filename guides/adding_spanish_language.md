# Adding Spanish Language Support to TrumpCoin Benefit

This guide provides step-by-step instructions for adding Spanish language support to your TrumpCoin Benefit Django application.

## Step 1: Configure Django for Internationalization

1. **Update settings.py**

   Open `trumpcoin_benefit/settings.py` and make the following changes:

   ```python
   # Add the LocaleMiddleware (make sure it's after SessionMiddleware)
   MIDDLEWARE = [
       'django.middleware.security.SecurityMiddleware',
       'django.contrib.sessions.middleware.SessionMiddleware',
       'django.middleware.locale.LocaleMiddleware',  # Add this line
       'django.middleware.common.CommonMiddleware',
       # ... rest of your middleware
   ]

   # Define available languages
   from django.utils.translation import gettext_lazy as _
   LANGUAGES = [
       ('en', _('English')),
       ('es', _('Spanish')),
   ]

   # Set the default language
   LANGUAGE_CODE = 'en'

   # Enable internationalization
   USE_I18N = True

   # Enable localization
   USE_L10N = True

   # Define where Django should look for translation files
   LOCALE_PATHS = [
       BASE_DIR / 'locale',
   ]
   ```

2. **Create the locale directory structure**

   Run these commands in your project root:

   ```bash
   mkdir -p locale/es/LC_MESSAGES
   ```

## Step 2: Mark Strings for Translation in Templates

1. **Load the translation tags in your templates**

   At the top of each template file (e.g., `templates/benefit/base.html`), add:

   ```html
   {% load i18n %}
   ```

2. **Mark strings for translation**

   Replace hardcoded text with translation tags:

   ```html
   <!-- Before -->
   <h1>Apply for TrumpCoin Benefits</h1>

   <!-- After -->
   <h1>{% translate "Apply for TrumpCoin Benefits" %}</h1>
   ```

   For variable content:

   ```html
   <!-- Before -->
   <p>Hello, {{ user.username }}</p>

   <!-- After -->
   <p>{% blocktranslate with username=user.username %}Hello, {{ username }}{% endblocktranslate %}</p>
   ```

## Step 3: Mark Strings for Translation in Python Code

1. **Import the translation function**

   At the top of your Python files (views, forms, etc.):

   ```python
   from django.utils.translation import gettext_lazy as _
   ```

2. **Mark strings for translation**

   ```python
   # Before
   title = "Application Status"

   # After
   title = _("Application Status")
   ```

   For form fields:

   ```python
   class ContactForm(forms.Form):
       name = forms.CharField(label=_("Name"), max_length=100)
       email = forms.EmailField(label=_("Email"))
       message = forms.CharField(label=_("Message"), widget=forms.Textarea)
   ```

## Step 4: Create Translation Files

1. **Generate message files**

   Run this command to extract all marked strings:

   ```bash
   django-admin makemessages -l es
   ```

2. **Edit the translation file**

   Open `locale/es/LC_MESSAGES/django.po` in a text editor. You'll see entries like:

   ```
   #: templates/benefit/home.html:12
   msgid "Apply for TrumpCoin Benefits"
   msgstr ""
   ```

   Add the Spanish translation:

   ```
   #: templates/benefit/home.html:12
   msgid "Apply for TrumpCoin Benefits"
   msgstr "Solicitar Beneficios de TrumpCoin"
   ```

3. **Compile the translation files**

   After translating all strings, compile the files:

   ```bash
   django-admin compilemessages
   ```

## Step 5: Add Language Switcher to Templates

1. **Add a language switcher to your base template**

   In `templates/benefit/base.html`, add:

   ```html
   <div class="language-switcher">
       <form action="{% url 'set_language' %}" method="post">
           {% csrf_token %}
           <input name="next" type="hidden" value="{{ request.path }}">
           <select name="language" onchange="this.form.submit()">
               {% get_current_language as CURRENT_LANGUAGE %}
               {% get_available_languages as LANGUAGES %}
               {% for lang_code, lang_name in LANGUAGES %}
                   <option value="{{ lang_code }}" {% if lang_code == CURRENT_LANGUAGE %}selected{% endif %}>
                       {{ lang_name }}
                   </option>
               {% endfor %}
           </select>
       </form>
   </div>
   ```

2. **Add the language URL pattern**

   In `trumpcoin_benefit/urls.py`, add:

   ```python
   from django.conf.urls.i18n import i18n_patterns
   from django.urls import path, include

   urlpatterns = [
       path('i18n/', include('django.conf.urls.i18n')),  # Add this line
   ]

   # Wrap your URL patterns with i18n_patterns
   urlpatterns += i18n_patterns(
       path('admin/', admin.site.urls),
       path('', include('benefit.urls')),
       prefix_default_language=False,  # Set to True if you want /en/ prefix for English
   )
   ```

## Step 6: Update Your Render Settings

1. **Update render_settings.py**

   Make sure your Render settings include the internationalization settings:

   ```python
   # In trumpcoin_benefit/render_settings.py
   
   # Keep the internationalization settings from settings.py
   USE_I18N = True
   USE_L10N = True
   LANGUAGES = [
       ('en', 'English'),
       ('es', 'Spanish'),
   ]
   LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]
   ```

## Step 7: Deploy and Test

1. **Commit and push your changes**

   ```bash
   git add .
   git commit -m "Add Spanish language support"
   git push
   ```

2. **Deploy to Render.com**

   Use the deployment script:

   ```bash
   # On Windows
   deployment\render_deploy.bat

   # On Linux/macOS
   ./deployment/render_deploy.sh
   ```

3. **Test the language switcher**

   - Visit your website
   - Use the language switcher to change to Spanish
   - Verify that the text changes to Spanish

## Common Issues and Solutions

1. **Missing translations**
   - Run `django-admin makemessages -l es` again to update the translation files
   - Add the missing translations and run `django-admin compilemessages`

2. **Language switcher not working**
   - Make sure the `LocaleMiddleware` is in the correct position in `MIDDLEWARE`
   - Check that the URL patterns are correctly wrapped with `i18n_patterns`

3. **Translation not showing up**
   - Verify that the translation files are compiled (`django-admin compilemessages`)
   - Check that the browser's language preference is set correctly
   - Clear your browser cache

## Additional Resources

- [Django Translation Documentation](https://docs.djangoproject.com/en/5.2/topics/i18n/translation/)
- [Django Internationalization Documentation](https://docs.djangoproject.com/en/5.2/topics/i18n/)
