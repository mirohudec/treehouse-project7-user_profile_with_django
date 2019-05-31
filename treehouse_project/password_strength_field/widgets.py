from django.forms import widgets
from django.utils.safestring import mark_safe


class PasswordStrengthMeter(widgets.PasswordInput):
    # https://andrearobertson.com/2017/06/17/django-example-creating-a-custom-form-field-widget/
    class Media:
        js = (
            'password_strength_field/js/password_meter.js',
        )
        css = {
            'all':
            ('password_strength_field/css/style.css',)
        }

    def render(self, name, value, attrs=None, **kwargs):
        final_attrs = self.build_attrs(self.attrs, attrs)

        final_attrs['strength-value'] = '80'
        output = super(PasswordStrengthMeter, self).render(
            name, value, final_attrs, **kwargs)
        output += """
        <div id="container">
        <span id="strength-meter">
        Password Strength: <span id="meter-value"> </span> </span>
        </div>
        """
        return mark_safe(output)
