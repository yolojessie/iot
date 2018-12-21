from populate import base
from map.models import Light
import random
import datetime
from django.utils import timezone

test = type('測試')
print(test)
addresses = ['85大樓', '中興大學', '太魯閣國家公園', '安平古堡', '新竹都城隍廟', '桃園國際棒球場', '溪頭自然教育園區', '礁溪溫泉公園', '蘭潭水庫', '西門町', '黃金博物館']


def populate():
    print('Populating light values ... ', end='')
    Light.objects.all().delete()

    for address in addresses:
        for j in range(30): 
            Light.objects.create(time=timezone.make_aware(datetime.datetime(2018, 12, 20, 12, random.randrange(1, 60), random.randrange(1, 60))), value=random.randrange(1, 1000), address=address)

    print('done')

if __name__ == '__main__':
    populate()