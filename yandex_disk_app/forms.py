from django import forms

class PublicLinkForm(forms.Form):
    """
    Форма для ввода публичной ссылки на Яндекс.Диск.

    Позволяет пользователям ввести публичную ссылку на папку в Яндекс.Диске.
    """
    public_key = forms.CharField(
        label="Публичная ссылка",
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'Введите публичную ссылку'}),
    )