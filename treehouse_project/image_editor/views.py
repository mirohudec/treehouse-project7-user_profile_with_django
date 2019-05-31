import re
from io import BytesIO
import base64
from PIL import Image
import uuid
from user_profile.models import UserProfile
from .forms import ImageUploadForm
from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect


def image_edit(request):
    if not request.user.is_authenticated:
        return redirect('accounts:sign_in')
    form = ImageUploadForm()
    if request.method == 'POST':
        form = ImageUploadForm(request.POST)
        crop = request.POST['hidden']
        if not crop:
            return render(request, 'image_editor/editor.html', {'form': form})
        image_data = re.sub('^data:image/.+;base64,', '', crop)
        image = Image.open(BytesIO(base64.b64decode(image_data)))
        # create unique name
        unique_id = str(uuid.uuid4())
        image.save(
            f'{settings.MEDIA_ROOT}/images/' +
            f'{unique_id}.png', 'PNG')
        user = UserProfile.objects.get(user_id=request.user.id)
        user.avatar = f'images/{unique_id}.png'
        user.save()
        return redirect('user_profile:home')
    return render(request, 'image_editor/editor.html', {'form': form})
